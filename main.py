"""House Maintenance Tracker — CLI entry point."""
import sys
from datetime import date
from pathlib import Path

import click
from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parent))

from src.db import init_db
from src import history as hist_module
from src import inventory as inv_module
from src import scheduler as sched_module
from src.models import Device, MaintenanceLog, Schedule
from src.seed_data import SEED_DEVICES, get_seed_schedules
from src.scheduler import days_until_due


@click.group()
def cli():
    """House Maintenance Tracker — Squamish, BC."""


# ── seed ──────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--force", is_flag=True, help="Re-seed even if devices already exist.")
def seed(force):
    """Init DB and load the default 10-device catalog."""
    init_db()
    existing = inv_module.list_devices()
    if existing and not force:
        click.echo(f"{len(existing)} device(s) already exist. Use --force to re-seed.")
        return

    device_map: dict[str, int] = {}
    for d in SEED_DEVICES:
        dev = Device(
            name=d["name"],
            category=d["category"],
            model=d.get("model"),
            part_numbers=d.get("part_numbers", []),
            maintenance_frequency_days=d.get("maintenance_frequency_days"),
            resource_links=d.get("resource_links", {}),
            notes=d.get("notes"),
        )
        dev_id = inv_module.add_device(dev)
        device_map[d["name"]] = dev_id
        click.echo(f"  + [{d['category']}] {d['name']}")

    schedules = get_seed_schedules(device_map)
    for s in schedules:
        sched_module.add_schedule(Schedule(
            device_id=s["device_id"],
            task_description=s["task_description"],
            next_due_date=s["next_due_date"],
            frequency_days=s["frequency_days"],
        ))

    click.echo(f"\nSeeded {len(SEED_DEVICES)} devices and {len(schedules)} schedules.")


# ── devices ───────────────────────────────────────────────────────────────────

@cli.group()
def devices():
    """Manage device inventory."""


@devices.command("list")
@click.option("--category", "-c", default=None, help="Filter by category.")
def devices_list(category):
    """List all devices."""
    init_db()
    devs = inv_module.list_devices(category=category)
    if not devs:
        click.echo("No devices found. Run: python main.py seed")
        return
    rows = [
        [
            d.id,
            d.name,
            d.category,
            d.model or "—",
            f"{d.maintenance_frequency_days}d" if d.maintenance_frequency_days else "—",
        ]
        for d in devs
    ]
    click.echo(tabulate(rows, headers=["ID", "Name", "Category", "Model", "Interval"],
                        tablefmt="rounded_outline"))


@devices.command("show")
@click.argument("device_id", type=int)
def devices_show(device_id):
    """Show full details for a device."""
    init_db()
    dev = inv_module.get_device(device_id)
    if not dev:
        click.echo(f"Device {device_id} not found.")
        return
    rows = [
        ["ID", dev.id],
        ["Name", dev.name],
        ["Category", dev.category],
        ["Model", dev.model or "—"],
        ["Serial", dev.serial_number or "—"],
        ["Parts", ", ".join(dev.part_numbers) if dev.part_numbers else "—"],
        ["Interval", f"{dev.maintenance_frequency_days} days" if dev.maintenance_frequency_days else "—"],
        ["Purchase Date", dev.purchase_date or "—"],
        ["Warranty Expiry", dev.warranty_expiry or "—"],
        ["Notes", dev.notes or "—"],
        ["Tutorial", dev.resource_links.get("tutorial", "—")],
        ["Purchase Link", dev.resource_links.get("purchase", "—")],
    ]
    click.echo(tabulate(rows, tablefmt="rounded_outline"))
    click.echo(f"\nTotal maintenance spend: ${hist_module.total_cost(device_id):.2f} CAD")


@devices.command("add")
def devices_add():
    """Add a new device interactively."""
    init_db()
    name = click.prompt("Device name")
    category = click.prompt(
        "Category",
        type=click.Choice(["Major Appliances", "Laundry Systems", "Plumbing & Water", "Safety & Electrical"]),
        show_choices=True,
    )
    model = click.prompt("Model (Enter to skip)", default="")
    serial = click.prompt("Serial number (Enter to skip)", default="")
    parts_raw = click.prompt("Part numbers, comma-separated (Enter to skip)", default="")
    freq = click.prompt("Maintenance interval (days)", type=int, default=180)
    notes = click.prompt("Notes (Enter to skip)", default="")
    tutorial = click.prompt("Tutorial URL (Enter to skip)", default="")
    purchase = click.prompt("Purchase URL (Enter to skip)", default="")

    dev = Device(
        name=name,
        category=category,
        model=model or None,
        serial_number=serial or None,
        part_numbers=[p.strip() for p in parts_raw.split(",") if p.strip()],
        maintenance_frequency_days=freq,
        notes=notes or None,
        resource_links={k: v for k, v in [("tutorial", tutorial), ("purchase", purchase)] if v},
    )
    dev_id = inv_module.add_device(dev)
    click.echo(f"Device added (ID {dev_id}).")


@devices.command("edit")
@click.argument("device_id", type=int)
def devices_edit(device_id):
    """Edit a device's notes and resource links."""
    init_db()
    dev = inv_module.get_device(device_id)
    if not dev:
        click.echo(f"Device {device_id} not found.")
        return
    dev.model = click.prompt("Model", default=dev.model or "")
    dev.serial_number = click.prompt("Serial number", default=dev.serial_number or "")
    dev.maintenance_frequency_days = click.prompt(
        "Maintenance interval (days)", type=int, default=dev.maintenance_frequency_days or 180
    )
    dev.notes = click.prompt("Notes", default=dev.notes or "")
    dev.resource_links["tutorial"] = click.prompt(
        "Tutorial URL", default=dev.resource_links.get("tutorial", "")
    )
    dev.resource_links["purchase"] = click.prompt(
        "Purchase URL", default=dev.resource_links.get("purchase", "")
    )
    dev.resource_links = {k: v for k, v in dev.resource_links.items() if v}
    inv_module.update_device(dev)
    click.echo(f"Device {device_id} updated.")


# ── history ───────────────────────────────────────────────────────────────────

@cli.group()
def history():
    """View and record maintenance history."""


@history.command("list")
@click.option("--device", "-d", "device_id", type=int, default=None, help="Filter by device ID.")
@click.option("--limit", "-n", default=25, show_default=True)
def history_list(device_id, limit):
    """List maintenance log entries."""
    init_db()
    logs = hist_module.list_logs(device_id=device_id, limit=limit)
    if not logs:
        click.echo("No log entries found.")
        return
    rows = [
        [
            l.id,
            l.completion_date,
            l.device_name or l.device_id,
            l.task_performed,
            f"${l.cost_cad:.2f}" if l.cost_cad else "—",
        ]
        for l in logs
    ]
    click.echo(tabulate(rows, headers=["ID", "Date", "Device", "Task", "Cost (CAD)"],
                        tablefmt="rounded_outline"))
    click.echo(f"\nTotal spend: ${hist_module.total_cost(device_id):.2f} CAD")


@history.command("add")
def history_add():
    """Record a completed maintenance task."""
    init_db()
    devs = inv_module.list_devices()
    if not devs:
        click.echo("No devices found. Run: python main.py seed")
        return

    for d in devs:
        click.echo(f"  [{d.id:>2}] {d.name}")

    device_id = click.prompt("Device ID", type=int)
    dev = inv_module.get_device(device_id)
    if not dev:
        click.echo("Invalid device ID.")
        return

    task = click.prompt("Task performed")
    completion_date = click.prompt("Completion date (YYYY-MM-DD)", default=str(date.today()))
    cost = click.prompt("Cost in CAD", type=float, default=0.0)
    sourcing = click.prompt("Sourcing info (vendor / URL, or Enter to skip)", default="")
    notes = click.prompt("Notes (or Enter to skip)", default="")

    log = MaintenanceLog(
        device_id=device_id,
        task_performed=task,
        completion_date=completion_date,
        cost_cad=cost,
        sourcing_info=sourcing or None,
        notes=notes or None,
    )
    log_id = hist_module.add_log(log)
    click.echo(f"Log entry {log_id} recorded.")

    active_schedules = sched_module.list_schedules(device_id=device_id)
    for s in active_schedules:
        if click.confirm(f"Advance schedule '{s.task_description}' (currently due {s.next_due_date})?"):
            new_date = sched_module.advance_schedule(s.id)
            click.echo(f"  Next due: {new_date}")


# ── schedule ──────────────────────────────────────────────────────────────────

@cli.group()
def schedule():
    """View and manage maintenance schedules."""


@schedule.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include inactive schedules.")
def schedule_list(show_all):
    """List all maintenance schedules."""
    init_db()
    schedules = sched_module.list_schedules(active_only=not show_all)
    if not schedules:
        click.echo("No schedules found.")
        return
    rows = []
    for s in schedules:
        d = days_until_due(s.next_due_date)
        status = click.style("OVERDUE", fg="red") if d < 0 else (
            click.style(f"in {d}d", fg="yellow") if d <= 7 else f"in {d}d"
        )
        rows.append([s.id, s.device_name or s.device_id, s.task_description,
                     s.next_due_date, status, f"{s.frequency_days}d"])
    click.echo(tabulate(rows, headers=["ID", "Device", "Task", "Next Due", "Status", "Every"],
                        tablefmt="rounded_outline"))


@schedule.command("due")
@click.option("--days", "-d", default=7, show_default=True, help="Look-ahead window in days.")
def schedule_due(days):
    """Show schedules due within N days (default: 7)."""
    init_db()
    schedules = sched_module.get_due_schedules(days_ahead=days)
    if not schedules:
        click.echo(f"Nothing due in the next {days} day(s). All good.")
        return
    rows = []
    for s in schedules:
        d = days_until_due(s.next_due_date)
        status = click.style("OVERDUE", fg="red") if d < 0 else click.style(f"in {d}d", fg="yellow")
        rows.append([s.device_name or s.device_id, s.task_description, s.next_due_date, status])
    click.echo(tabulate(rows, headers=["Device", "Task", "Due Date", "Status"],
                        tablefmt="rounded_outline"))


# ── notify ────────────────────────────────────────────────────────────────────

@cli.group()
def notify():
    """Push Google Calendar events and send email alerts."""


@notify.command("push")
@click.option("--device", "-d", "device_id", type=int, default=None,
              help="Restrict to one device ID.")
@click.option("--force", is_flag=True, help="Re-push even if a calendar event is already linked.")
def notify_push(device_id, force):
    """Create recurring Google Calendar events for active schedules."""
    init_db()
    from src.notifications import create_calendar_event

    schedules = sched_module.list_schedules(device_id=device_id)
    pushed = 0
    for s in schedules:
        if s.calendar_event_id and not force:
            click.echo(f"  skip  [{s.device_name}] already linked")
            continue
        dev = inv_module.get_device(s.device_id)
        if not dev:
            continue
        try:
            event_id = create_calendar_event(
                device_name=dev.name,
                task_description=s.task_description,
                due_date=s.next_due_date,
                frequency_days=s.frequency_days,
                part_numbers=dev.part_numbers,
                resource_links=dev.resource_links,
                notes=dev.notes,
            )
            sched_module.set_calendar_event_id(s.id, event_id)
            click.echo(f"  pushed [{dev.name}] {s.task_description}")
            pushed += 1
        except Exception as e:
            click.echo(f"  ERROR [{dev.name}]: {e}", err=True)
    click.echo(f"\nPushed {pushed} event(s) to Google Calendar.")


@notify.command("check")
@click.option("--days", "-d", default=7, show_default=True, help="Alert window in days.")
def notify_check(days):
    """Email alerts for schedules due within N days."""
    init_db()
    from src.notifications import send_email_alert

    schedules = sched_module.get_due_schedules(days_ahead=days)
    if not schedules:
        click.echo(f"Nothing due in the next {days} day(s). No emails sent.")
        return
    sent = 0
    for s in schedules:
        dev = inv_module.get_device(s.device_id)
        if not dev:
            continue
        try:
            send_email_alert(
                device_name=dev.name,
                category=dev.category,
                task_description=s.task_description,
                due_date=s.next_due_date,
                part_numbers=dev.part_numbers,
                resource_links=dev.resource_links,
                notes=dev.notes,
            )
            click.echo(f"  sent  [{dev.name}] {s.task_description}")
            sent += 1
        except Exception as e:
            click.echo(f"  ERROR [{dev.name}]: {e}", err=True)
    click.echo(f"\nSent {sent} email alert(s).")


if __name__ == "__main__":
    cli()
