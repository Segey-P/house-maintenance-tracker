"""Google Calendar and Gmail notification integration."""
import base64
import json
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

CREDS_PATH = Path(__file__).parent.parent / "config" / "credentials" / "token.json"
CLIENT_SECRET_PATH = Path(__file__).parent.parent / "config" / "credentials" / "client_secret.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
]


def _get_google_creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    if not CREDS_PATH.exists():
        raise FileNotFoundError(
            f"No token found at {CREDS_PATH}. Run: python3 setup_auth.py"
        )
    creds = Credentials.from_authorized_user_file(str(CREDS_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        CREDS_PATH.write_text(creds.to_json())
    return creds


def _calendar_service():
    from googleapiclient.discovery import build
    return build("calendar", "v3", credentials=_get_google_creds())


def _gmail_service():
    from googleapiclient.discovery import build
    return build("gmail", "v1", credentials=_get_google_creds())


def _load_settings() -> dict:
    settings_path = Path(__file__).parent.parent / "config" / "settings.json"
    return json.loads(settings_path.read_text())


def create_calendar_event(
    device_name: str,
    task_description: str,
    due_date: str,
    frequency_days: int,
    part_numbers: list,
    resource_links: dict,
    notes: Optional[str],
) -> str:
    settings = _load_settings()
    calendar_id = settings.get("calendar_id", "primary")
    timezone = settings.get("timezone", "America/Vancouver")

    parts_text = ", ".join(part_numbers) if part_numbers else "See device profile"
    tutorial = resource_links.get("tutorial", "")
    purchase = resource_links.get("purchase", "")

    description_lines = [
        f"Device: {device_name}",
        f"Task: {task_description}",
        f"Required Parts: {parts_text}",
    ]
    if purchase:
        description_lines.append(f"Purchase: {purchase}")
    if tutorial:
        description_lines.append(f"Tutorial: {tutorial}")
    if notes:
        description_lines.append(f"Notes: {notes}")

    # Convert frequency_days to an RFC 5545 RRULE
    if frequency_days % 365 == 0:
        rrule = f"RRULE:FREQ=YEARLY"
    elif frequency_days % 30 == 0:
        months = frequency_days // 30
        rrule = f"RRULE:FREQ=MONTHLY;INTERVAL={months}"
    elif frequency_days % 7 == 0:
        weeks = frequency_days // 7
        rrule = f"RRULE:FREQ=WEEKLY;INTERVAL={weeks}"
    else:
        rrule = f"RRULE:FREQ=DAILY;INTERVAL={frequency_days}"

    event_body = {
        "summary": f"[Maintenance] {device_name} — {task_description}",
        "description": "\n".join(description_lines),
        "start": {"date": due_date},
        "end": {"date": due_date},
        "recurrence": [rrule],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 120},
            ],
        },
    }

    svc = _calendar_service()
    event = svc.events().insert(calendarId=calendar_id, body=event_body).execute()
    return event["id"]


def send_email_alert(
    device_name: str,
    category: str,
    task_description: str,
    due_date: str,
    part_numbers: list,
    resource_links: dict,
    notes: Optional[str],
) -> None:
    settings = _load_settings()
    recipient = settings.get("user_email", "")
    if not recipient:
        raise ValueError("user_email not set in config/settings.json")

    parts_html = (
        "<ul>" + "".join(f"<li>{p}</li>" for p in part_numbers) + "</ul>"
        if part_numbers
        else "<p>See device profile for part details.</p>"
    )

    tutorial = resource_links.get("tutorial", "")
    purchase = resource_links.get("purchase", "")
    days_left = (date.fromisoformat(due_date) - date.today()).days

    due_label = (
        "<span style='color:red;font-weight:bold'>OVERDUE</span>"
        if days_left < 0
        else f"<span style='color:orange;font-weight:bold'>Due in {days_left} day(s)</span>"
        if days_left <= 3
        else f"Due in {days_left} day(s)"
    )

    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
    <h2 style="color:#2c5282">🔧 House Maintenance Reminder</h2>
    <table style="width:100%;border-collapse:collapse">
      <tr><td style="padding:8px;background:#edf2f7;font-weight:bold">Device</td>
          <td style="padding:8px">{device_name}</td></tr>
      <tr><td style="padding:8px;background:#edf2f7;font-weight:bold">Category</td>
          <td style="padding:8px">{category}</td></tr>
      <tr><td style="padding:8px;background:#edf2f7;font-weight:bold">Task</td>
          <td style="padding:8px">{task_description}</td></tr>
      <tr><td style="padding:8px;background:#edf2f7;font-weight:bold">Due Date</td>
          <td style="padding:8px">{due_date} &nbsp; {due_label}</td></tr>
    </table>
    <h3>Required Parts</h3>
    {parts_html}
    {"<h3>Purchase Link</h3><p><a href='" + purchase + "'>" + purchase + "</a></p>" if purchase else ""}
    {"<h3>Tutorial</h3><p><a href='" + tutorial + "'>" + tutorial + "</a></p>" if tutorial else ""}
    {"<h3>Notes</h3><p>" + notes + "</p>" if notes else ""}
    <hr>
    <p style="color:#718096;font-size:12px">House Maintenance Tracker &mdash; Squamish, BC</p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["To"] = recipient
    msg["From"] = recipient
    msg["Subject"] = f"[HMT] {device_name} — {task_description} ({due_date})"
    msg.attach(MIMEText(html, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    svc = _gmail_service()
    svc.users().messages().send(userId="me", body={"raw": raw}).execute()
