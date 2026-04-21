
// ── Sample Data ───────────────────────────────────────────────────────────────
// Today = April 20, 2026

const CATEGORIES = ['Major Appliances', 'Kitchen Appliances', 'Laundry Systems', 'Plumbing & Water', 'Safety & Electrical'];

const INITIAL_DEVICES = [
  { id: 1, name: 'Main Fridge',        category: 'Major Appliances',      model: 'Whirlpool WRF535SWHZ', serial: 'WR2022-0041', purchase_date: '2022-03-15', warranty_expiry: '2027-03-15', notes: 'Water filter is internal — part # W10295370A', is_archived: false },
  { id: 2, name: 'Oven / Stove',       category: 'Major Appliances',      model: 'GE JBS86SPSS',         serial: null,          purchase_date: '2022-03-15', warranty_expiry: '2026-03-15', notes: 'Warranty expired — check service options', is_archived: false },
  { id: 3, name: 'Dishwasher',         category: 'Major Appliances',      model: 'Bosch SHPM88Z75N',     serial: 'BS2023-0187', purchase_date: '2023-01-10', warranty_expiry: '2028-01-10', notes: null, is_archived: false },
  { id: 4, name: 'Range Hood',         category: 'Kitchen Appliances',    model: 'Broan BCDF136SS',      serial: null,          purchase_date: '2022-03-15', warranty_expiry: null,         notes: 'Charcoal filter, non-ducted', is_archived: false },
  { id: 5, name: 'Washer',             category: 'Laundry Systems',       model: 'LG WM4000HBA',         serial: 'LG2023-0912', purchase_date: '2023-06-01', warranty_expiry: '2028-06-01', notes: null, is_archived: false },
  { id: 6, name: 'Dryer',              category: 'Laundry Systems',       model: 'LG DLGX4001B',         serial: 'LG2023-0913', purchase_date: '2023-06-01', warranty_expiry: '2028-06-01', notes: null, is_archived: false },
  { id: 7, name: 'Water Heater',       category: 'Plumbing & Water',      model: 'Rheem PROE50 T2 RH95', serial: 'RH2021-0432', purchase_date: '2021-08-20', warranty_expiry: '2027-08-20', notes: 'Flush annually, check anode rod every 2 years', is_archived: false },
  { id: 8, name: 'Furnace / HVAC',     category: 'Safety & Electrical',   model: 'Lennox EL296V',        serial: 'LX2020-0201', purchase_date: '2020-11-01', warranty_expiry: '2030-11-01', notes: 'Annual service contract with AirPro Squamish', is_archived: false },
  { id: 9, name: 'Smoke Detectors',    category: 'Safety & Electrical',   model: 'Kidde i9080',          serial: null,          purchase_date: '2022-03-15', warranty_expiry: null,         notes: '3 units — hallway, bedroom, kitchen', is_archived: false },
  { id: 10, name: 'CO Alarm',          category: 'Safety & Electrical',   model: 'Kidde KN-COSM-IB',    serial: null,          purchase_date: '2022-03-15', warranty_expiry: null,         notes: 'Near furnace room', is_archived: false },
];

const INITIAL_SERVICE_TYPES = [
  { id: 1, device_id: 1, name: 'Water Filter Replacement', frequency_days: 180, part_numbers: ['W10295370A'], tutorial_url: null, purchase_url: null, notes: 'Push-in filter inside fridge' },
  { id: 2, device_id: 1, name: 'Condenser Coil Cleaning', frequency_days: 365, part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Vacuum coils at back/bottom' },
  { id: 3, device_id: 2, name: 'Deep Clean Oven',          frequency_days: 90,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Use self-clean or manual scrub' },
  { id: 4, device_id: 3, name: 'Filter Cleaning',          frequency_days: 30,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Rinse mesh filter under hot water' },
  { id: 5, device_id: 3, name: 'Descaling',                frequency_days: 90,  part_numbers: ['311268'], tutorial_url: null, purchase_url: null, notes: 'Use Bosch descaler tablet' },
  { id: 6, device_id: 4, name: 'Charcoal Filter Replace',  frequency_days: 180, part_numbers: ['97007696'], tutorial_url: null, purchase_url: null, notes: 'Non-ducted — charcoal only' },
  { id: 7, device_id: 5, name: 'Drum Cleaning',            frequency_days: 30,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Tub clean cycle + wipe seal' },
  { id: 8, device_id: 5, name: 'Door Seal Wipe',           frequency_days: 14,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Check for mould, wipe dry' },
  { id: 9, device_id: 6, name: 'Lint Trap Clean',          frequency_days: 7,   part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'After every use ideally' },
  { id: 10, device_id: 6, name: 'Vent Duct Cleaning',      frequency_days: 365, part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Hire duct cleaner or DIY with kit' },
  { id: 11, device_id: 7, name: 'Tank Flush',              frequency_days: 365, part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Flush sediment from bottom drain' },
  { id: 12, device_id: 7, name: 'Anode Rod Inspection',    frequency_days: 730, part_numbers: ['SP11553'], tutorial_url: null, purchase_url: null, notes: 'Replace if <50% coating remains' },
  { id: 13, device_id: 8, name: 'Filter Replacement',      frequency_days: 90,  part_numbers: ['X8790'], tutorial_url: null, purchase_url: null, notes: 'Lennox MERV-11 filter' },
  { id: 14, device_id: 8, name: 'Annual Service',          frequency_days: 365, part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Book with AirPro — include AC check' },
  { id: 15, device_id: 9, name: 'Monthly Test',            frequency_days: 30,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Press test button on each unit' },
  { id: 16, device_id: 10, name: 'Monthly Test',           frequency_days: 30,  part_numbers: [], tutorial_url: null, purchase_url: null, notes: 'Press test button' },
];

const INITIAL_SCHEDULES = [
  { id: 1,  device_id: 1,  service_type_id: 1,  task_description: 'Water Filter Replacement',  next_due_date: '2026-04-08', frequency_days: 180, is_active: true,  calendar_event_id: null },
  { id: 2,  device_id: 1,  service_type_id: 2,  task_description: 'Condenser Coil Cleaning',   next_due_date: '2026-07-20', frequency_days: 365, is_active: true,  calendar_event_id: 'cal_001' },
  { id: 3,  device_id: 2,  service_type_id: 3,  task_description: 'Deep Clean Oven',            next_due_date: '2026-05-20', frequency_days: 90,  is_active: true,  calendar_event_id: null },
  { id: 4,  device_id: 3,  service_type_id: 4,  task_description: 'Filter Cleaning',            next_due_date: '2026-04-20', frequency_days: 30,  is_active: true,  calendar_event_id: null },
  { id: 5,  device_id: 3,  service_type_id: 5,  task_description: 'Descaling',                  next_due_date: '2026-06-10', frequency_days: 90,  is_active: true,  calendar_event_id: null },
  { id: 6,  device_id: 4,  service_type_id: 6,  task_description: 'Charcoal Filter Replace',   next_due_date: '2026-05-04', frequency_days: 180, is_active: true,  calendar_event_id: null },
  { id: 7,  device_id: 5,  service_type_id: 7,  task_description: 'Drum Cleaning',              next_due_date: '2026-04-23', frequency_days: 30,  is_active: true,  calendar_event_id: null },
  { id: 8,  device_id: 5,  service_type_id: 8,  task_description: 'Door Seal Wipe',             next_due_date: '2026-04-15', frequency_days: 14,  is_active: true,  calendar_event_id: null },
  { id: 9,  device_id: 6,  service_type_id: 9,  task_description: 'Lint Trap Clean',            next_due_date: '2026-04-27', frequency_days: 7,   is_active: true,  calendar_event_id: null },
  { id: 10, device_id: 6,  service_type_id: 10, task_description: 'Vent Duct Cleaning',         next_due_date: '2026-09-15', frequency_days: 365, is_active: true,  calendar_event_id: 'cal_002' },
  { id: 11, device_id: 7,  service_type_id: 11, task_description: 'Tank Flush',                 next_due_date: '2026-08-20', frequency_days: 365, is_active: true,  calendar_event_id: null },
  { id: 12, device_id: 7,  service_type_id: 12, task_description: 'Anode Rod Inspection',       next_due_date: '2027-08-20', frequency_days: 730, is_active: true,  calendar_event_id: null },
  { id: 13, device_id: 8,  service_type_id: 13, task_description: 'Filter Replacement',         next_due_date: '2026-04-26', frequency_days: 90,  is_active: true,  calendar_event_id: null },
  { id: 14, device_id: 8,  service_type_id: 14, task_description: 'Annual Service',             next_due_date: '2026-10-01', frequency_days: 365, is_active: true,  calendar_event_id: 'cal_003' },
  { id: 15, device_id: 9,  service_type_id: 15, task_description: 'Monthly Test',               next_due_date: '2026-04-15', frequency_days: 30,  is_active: true,  calendar_event_id: null },
  { id: 16, device_id: 10, service_type_id: 16, task_description: 'Monthly Test',               next_due_date: '2026-04-30', frequency_days: 30,  is_active: true,  calendar_event_id: null },
];

const INITIAL_LOGS = [
  { id: 1, device_id: 1, service_type_id: 1,  task_performed: 'Water Filter Replacement', completion_date: '2025-10-08', cost_cad: 42.99, sourcing_info: 'Home Depot', notes: null },
  { id: 2, device_id: 8, service_type_id: 13, task_performed: 'Filter Replacement',       completion_date: '2026-01-26', cost_cad: 28.50, sourcing_info: 'Amazon',     notes: 'Lennox X8790, MERV-11' },
  { id: 3, device_id: 5, service_type_id: 7,  task_performed: 'Drum Cleaning',            completion_date: '2026-03-23', cost_cad: 0,     sourcing_info: null,         notes: 'Tub clean cycle x2' },
  { id: 4, device_id: 3, service_type_id: 4,  task_performed: 'Filter Cleaning',          completion_date: '2026-03-20', cost_cad: 0,     sourcing_info: null,         notes: null },
  { id: 5, device_id: 6, service_type_id: 9,  task_performed: 'Lint Trap Clean',          completion_date: '2026-04-13', cost_cad: 0,     sourcing_info: null,         notes: null },
  { id: 6, device_id: 7, service_type_id: 11, task_performed: 'Tank Flush',               completion_date: '2025-08-20', cost_cad: 0,     sourcing_info: null,         notes: 'Light sediment, normal' },
  { id: 7, device_id: 8, service_type_id: 14, task_performed: 'Annual HVAC Service',      completion_date: '2025-10-01', cost_cad: 189.0, sourcing_info: 'AirPro Squamish', notes: 'All good, no issues' },
  { id: 8, device_id: 2, service_type_id: 3,  task_performed: 'Deep Clean Oven',          completion_date: '2026-02-20', cost_cad: 0,     sourcing_info: null,         notes: null },
];

// ── Helpers ───────────────────────────────────────────────────────────────────

const { useState, useEffect, useRef, useCallback } = React;

function deviceName(devices, id) {
  return (devices.find(d => d.id === id) || {}).name || '—';
}
function serviceTypeName(serviceTypes, id) {
  return (serviceTypes.find(s => s.id === id) || {}).name || null;
}
function advanceDate(dateStr, days) {
  const d = new Date(dateStr + 'T12:00:00');
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

// ── Category color ────────────────────────────────────────────────────────────
const DEVICE_IMAGES = {
  1:  'https://source.unsplash.com/300x180/?refrigerator,whirlpool',
  2:  'https://source.unsplash.com/300x180/?oven,stove,kitchen',
  3:  'https://source.unsplash.com/300x180/?dishwasher,kitchen',
  4:  'https://source.unsplash.com/300x180/?range+hood,kitchen',
  5:  'https://source.unsplash.com/300x180/?washing+machine,laundry',
  6:  'https://source.unsplash.com/300x180/?dryer,laundry',
  7:  'https://source.unsplash.com/300x180/?water+heater,boiler',
  8:  'https://source.unsplash.com/300x180/?furnace,hvac,mechanical',
  9:  'https://source.unsplash.com/300x180/?smoke+detector,safety',
  10: 'https://source.unsplash.com/300x180/?carbon+monoxide+alarm',
};

const CAT_COLORS = {
  'Major Appliances':    '#3b82f6',
  'Kitchen Appliances':  '#8b5cf6',
  'Laundry Systems':     '#06b6d4',
  'Plumbing & Water':    '#0ea5e9',
  'Safety & Electrical': '#f59e0b',
};

// ── AI Chat Widget ────────────────────────────────────────────────────────────
function AIChatWidget({ devices, schedules, logs }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hi! I know your home — ask me anything about maintenance, parts, or upcoming tasks.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const context = `You are a home maintenance assistant for a 1-bedroom home in Squamish, BC. 
Devices: ${devices.map(d => `${d.name} (${d.model || d.category})`).join(', ')}.
Overdue schedules: ${schedules.filter(s => daysUntil(s.next_due_date) < 0).map(s => s.task_description + ' for ' + (devices.find(d=>d.id===s.device_id)||{}).name).join(', ') || 'none'}.
Due this week: ${schedules.filter(s => daysUntil(s.next_due_date) >= 0 && daysUntil(s.next_due_date) <= 7).map(s => s.task_description).join(', ') || 'none'}.
Be concise and practical.`;

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setMessages(m => [...m, { role: 'user', text: userMsg }]);
    setInput('');
    setLoading(true);
    try {
      const result = await window.claude.complete({
        messages: [
          { role: 'user', content: context + '\n\nUser question: ' + userMsg }
        ]
      });
      setMessages(m => [...m, { role: 'assistant', text: result }]);
    } catch(e) {
      setMessages(m => [...m, { role: 'assistant', text: 'Sorry, I had trouble answering that.' }]);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (bottomRef.current) bottomRef.current.scrollTop = bottomRef.current.scrollHeight;
  }, [messages]);

  return (
    <Card style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '12px 16px', borderBottom: '1px solid #f5f5f3', display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ width: 24, height: 24, borderRadius: 6, background: '#f5f3ff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12 }}>✦</div>
        <span style={{ fontSize: 13, fontWeight: 700, color: '#1c1c1e' }}>AI Assistant</span>
        <Badge type="purple">Beta</Badge>
      </div>
      <div ref={bottomRef} style={{ height: 180, overflowY: 'auto', padding: '12px 16px', display: 'flex', flexDirection: 'column', gap: 8 }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '85%',
            background: m.role === 'user' ? '#e8823a' : '#f8f7f5',
            color: m.role === 'user' ? '#fff' : '#374151',
            borderRadius: m.role === 'user' ? '12px 12px 2px 12px' : '12px 12px 12px 2px',
            padding: '8px 12px', fontSize: 12, lineHeight: 1.5,
          }}>{m.text}</div>
        ))}
        {loading && (
          <div style={{ alignSelf: 'flex-start', background: '#f8f7f5', borderRadius: '12px 12px 12px 2px', padding: '8px 12px' }}>
            <Spinner size={14} color="#8b5cf6" />
          </div>
        )}
      </div>
      <div style={{ padding: '10px 12px', borderTop: '1px solid #f5f5f3', display: 'flex', gap: 8 }}>
        <input
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="Ask about your home…"
          style={{ flex: 1, padding: '7px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit', outline: 'none' }}
        />
        <Btn size="sm" onClick={send} disabled={!input.trim() || loading}>Send</Btn>
      </div>
    </Card>
  );
}

function QuickComplete({ schedule, devices, serviceTypes, onDone, onCancel }) {
  const dev = devices.find(d => d.id === schedule.device_id) || {};
  const [cost, setCost] = useState('');
  const [notes, setNotes] = useState('');
  return (
    <div style={{ background: '#f8f7f5', borderRadius: 8, padding: '12px 14px', marginTop: 10, border: '1px solid #e5e5e3' }}>
      <div style={{ fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 10 }}>
        Log: {schedule.task_description} — {dev.name}
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <input
          placeholder="Cost (CAD) — optional"
          value={cost} onChange={e => setCost(e.target.value)}
          type="number" min="0" step="0.01"
          style={{ flex: 1, padding: '6px 10px', borderRadius: 6, border: '1px solid #d1d5db', fontSize: 12, fontFamily: 'inherit' }}
        />
        <input
          placeholder="Notes — optional"
          value={notes} onChange={e => setNotes(e.target.value)}
          style={{ flex: 2, padding: '6px 10px', borderRadius: 6, border: '1px solid #d1d5db', fontSize: 12, fontFamily: 'inherit' }}
        />
      </div>
      <div style={{ display: 'flex', gap: 6 }}>
        <Btn size="sm" variant="primary" onClick={() => onDone(schedule, parseFloat(cost) || 0, notes)}>
          ✓ Mark Done
        </Btn>
        <Btn size="sm" variant="ghost" onClick={onCancel}>Cancel</Btn>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// VIEW: DASHBOARD
// ══════════════════════════════════════════════════════════════════════════════

function Dashboard({ devices, schedules, logs, serviceTypes, onCompleteTask, onNavigate }) {
  const [completing, setCompleting] = useState(null);

  const overdue   = schedules.filter(s => s.is_active && daysUntil(s.next_due_date) < 0);
  const today     = schedules.filter(s => s.is_active && daysUntil(s.next_due_date) === 0);
  const thisWeek  = schedules.filter(s => s.is_active && daysUntil(s.next_due_date) > 0 && daysUntil(s.next_due_date) <= 7);
  const thisMonth = schedules.filter(s => s.is_active && daysUntil(s.next_due_date) > 7 && daysUntil(s.next_due_date) <= 30);
  const actionItems = [...overdue, ...today];
  const ytdSpend = logs.filter(l => l.completion_date >= '2026-01-01').reduce((a, l) => a + (l.cost_cad || 0), 0);
  const totalSpend = logs.reduce((a, l) => a + (l.cost_cad || 0), 0);

  const handleDone = (sched, cost, notes) => {
    onCompleteTask(sched, cost, notes);
    setCompleting(null);
  };

  const TaskRow = ({ sched, urgent }) => {
    const si = statusInfo(daysUntil(sched.next_due_date));
    const dev = devices.find(d => d.id === sched.device_id) || {};
    return (
      <div>
        <Card style={{ padding: '12px 16px' }} accent={urgent ? si.dot : undefined}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                <span style={{ fontSize: 14, fontWeight: 600, color: '#1c1c1e' }}>{sched.task_description}</span>
                <Badge type={si.status}>{si.label}</Badge>
              </div>
              <div style={{ fontSize: 12, color: '#6b7280', marginTop: 2 }}>{dev.name} · {dev.model || dev.category}</div>
            </div>
            <div style={{ display: 'flex', gap: 6 }}>
              <Btn size="sm" variant="primary" onClick={() => setCompleting(completing === sched.id ? null : sched.id)}>
                ✓ Done
              </Btn>
              <Btn size="sm" variant="ghost" onClick={() => {}}>⏭ Skip</Btn>
            </div>
          </div>
          {completing === sched.id && (
            <QuickComplete
              schedule={sched} devices={devices} serviceTypes={serviceTypes}
              onDone={handleDone} onCancel={() => setCompleting(null)}
            />
          )}
        </Card>
      </div>
    );
  };

  return (
    <div>
      {/* Stats row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 28 }}>
        {[
          { label: 'Active Devices', val: devices.filter(d => !d.is_archived).length, color: '#1c1c1e' },
          { label: 'Overdue',        val: overdue.length,  color: overdue.length > 0 ? '#dc2626' : '#1c1c1e', bg: overdue.length > 0 ? '#fef2f2' : '#fff' },
          { label: 'Due This Week',  val: thisWeek.length, color: thisWeek.length > 0 ? '#b45309' : '#1c1c1e', bg: thisWeek.length > 0 ? '#fffbeb' : '#fff' },
          { label: 'YTD Spend',      val: `$${ytdSpend.toFixed(0)}`, color: '#1c1c1e' },
        ].map(s => (
          <Card key={s.label} style={{ padding: '16px 20px', background: s.bg }}>
            <div style={{ fontSize: 11, fontWeight: 600, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>{s.label}</div>
            <div style={{ fontSize: 28, fontWeight: 800, color: s.color, letterSpacing: '-0.02em' }}>{s.val}</div>
          </Card>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 20 }}>
        {/* Left column */}
        <div>
          {actionItems.length > 0 ? (
            <>
              <Divider label="Needs Attention" />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {actionItems.map(s => <TaskRow key={s.id} sched={s} urgent />)}
              </div>
            </>
          ) : (
            <Card style={{ padding: '20px 24px', marginBottom: 16, background: '#f0fdf4', borderColor: '#bbf7d0' }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: '#15803d' }}>✓ Nothing overdue — great job!</div>
            </Card>
          )}

          {thisWeek.length > 0 && (
            <>
              <Divider label="Due This Week" />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {thisWeek.map(s => <TaskRow key={s.id} sched={s} />)}
              </div>
            </>
          )}

          {thisMonth.length > 0 && (
            <>
              <Divider label="Later This Month" />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {thisMonth.map(s => <TaskRow key={s.id} sched={s} />)}
              </div>
            </>
          )}
        </div>

        {/* Right column */}
        <div>
          <Divider label="AI Assistant" />
          <AIChatWidget devices={devices} schedules={schedules} logs={logs} />

          <Divider label="Recent Activity" />
          <Card style={{ padding: 0, overflow: 'hidden' }}>
            {logs.slice(0, 5).map((l, i) => {
              const dev = devices.find(d => d.id === l.device_id) || {};
              return (
                <div key={l.id} style={{
                  padding: '11px 16px', display: 'flex', alignItems: 'center', gap: 12,
                  borderBottom: i < Math.min(logs.length, 5) - 1 ? '1px solid #f5f5f3' : 'none',
                }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{dev.name}</div>
                    <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{l.task_performed}</div>
                  </div>
                  <div style={{ textAlign: 'right', flexShrink: 0 }}>
                    <div style={{ fontSize: 11, color: '#6b7280' }}>{l.completion_date.slice(5)}</div>
                    {l.cost_cad > 0 && <div style={{ fontSize: 12, fontWeight: 600, color: '#374151' }}>${l.cost_cad.toFixed(0)}</div>}
                  </div>
                </div>
              );
            })}
            {logs.length === 0 && <div style={{ padding: 20, fontSize: 13, color: '#9ca3af', textAlign: 'center' }}>No maintenance logged yet.</div>}
          </Card>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// VIEW: DEVICES
// ══════════════════════════════════════════════════════════════════════════════

// ── Service Type Detail Panel ─────────────────────────────────────────────────
function ServiceTypePanel({ st, device, logs, schedules, open, onClose, onDelete, onUpdate }) {
  if (!st) return null;
  const stLogs = logs.filter(l => l.service_type_id === st.id);
  const sched = schedules.find(s => s.service_type_id === st.id);
  const [editName, setEditName] = useState(st.name);
  const [editFreq, setEditFreq] = useState(st.frequency_days);
  const [editParts, setEditParts] = useState((st.part_numbers || []).join(', '));
  const [editNotes, setEditNotes] = useState(st.notes || '');
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    setEditName(st.name); setEditFreq(st.frequency_days);
    setEditParts((st.part_numbers || []).join(', ')); setEditNotes(st.notes || '');
    setConfirmDelete(false);
  }, [st.id]);

  return (
    <SidePanel open={open} onClose={onClose} title={st.name} subtitle={device?.name + ' · ' + freqLabel(st.frequency_days)}>
      {sched && (
        <div style={{ background: '#f8f7f5', borderRadius: 8, padding: '10px 14px', marginBottom: 16 }}>
          <div style={{ display: 'flex', gap: 20 }}>
            {[
              { label: 'Next Due', val: formatDate(sched.next_due_date) },
              { label: 'Status',   val: <Badge type={statusInfo(daysUntil(sched.next_due_date)).status}>{statusInfo(daysUntil(sched.next_due_date)).label}</Badge> },
              { label: 'Times Done', val: stLogs.length },
            ].map(r => (
              <div key={r.label}>
                <div style={{ fontSize: 10, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{r.label}</div>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e', marginTop: 2 }}>{r.val}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <Divider label="Edit" />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
        <div>
          <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Name <span style={{ color: '#ef4444' }}>*</span></div>
          <input value={editName} onChange={e => setEditName(e.target.value)}
            style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
          <div>
            <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Repeat every (days) <span style={{ color: '#ef4444' }}>*</span></div>
            <input type="number" value={editFreq} onChange={e => setEditFreq(e.target.value)}
              style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
          <div>
            <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Part numbers <span style={{ color: '#9ca3af', fontWeight: 400 }}>(optional)</span></div>
            <input placeholder="Comma-separated" value={editParts} onChange={e => setEditParts(e.target.value)}
              style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
        </div>
        <div>
          <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Notes <span style={{ color: '#9ca3af', fontWeight: 400 }}>(optional)</span></div>
          <input value={editNotes} onChange={e => setEditNotes(e.target.value)}
            style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
        </div>
        <Btn style={{ alignSelf: 'flex-start' }} onClick={() => {
          onUpdate({ ...st, name: editName, frequency_days: parseInt(editFreq), part_numbers: editParts.split(',').map(p=>p.trim()).filter(Boolean), notes: editNotes || null });
          onClose();
        }}>Save Changes</Btn>
      </div>

      {/* AI helpers */}
      <Divider label="AI Tools" />
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 20 }}>
        <AIBlock label="Find Parts" icon="✦"
          prompt={`For "${st.name}" on a ${device?.model || device?.name}: list exact part numbers, best Amazon.ca links, and CAD prices. Be concise.`} />
        <AIBlock label="Find Tutorial" icon="▶"
          prompt={`How to do "${st.name}" on a ${device?.model || device?.name}? Best YouTube search terms, 4-5 steps, tools needed.`} />
      </div>

      {/* History */}
      {stLogs.length > 0 && (
        <>
          <Divider label={`History (${stLogs.length})`} />
          {stLogs.map(l => (
            <div key={l.id} style={{ display: 'flex', gap: 10, padding: '8px 0', borderBottom: '1px solid #f5f5f3', fontSize: 12 }}>
              <div style={{ color: '#9ca3af', width: 80, flexShrink: 0 }}>{l.completion_date}</div>
              <div style={{ flex: 1, color: '#374151' }}>{l.task_performed}</div>
              <div style={{ color: '#6b7280', flexShrink: 0 }}>{l.cost_cad > 0 ? formatMoney(l.cost_cad) : '—'}</div>
            </div>
          ))}
        </>
      )}

      {/* Delete */}
      <div style={{ marginTop: 24, paddingTop: 16, borderTop: '1px solid #f0f0ee' }}>
        {!confirmDelete ? (
          <Btn variant="ghost" size="sm" onClick={() => setConfirmDelete(true)} style={{ color: '#ef4444' }}>Delete service type…</Btn>
        ) : (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, padding: '12px 14px' }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#dc2626', marginBottom: 8 }}>Delete "{st.name}"?</div>
            <div style={{ display: 'flex', gap: 8 }}>
              <Btn size="sm" variant="danger" onClick={() => { onDelete(st.id); onClose(); }}>Yes, delete</Btn>
              <Btn size="sm" variant="ghost" onClick={() => setConfirmDelete(false)}>Cancel</Btn>
            </div>
          </div>
        )}
      </div>
    </SidePanel>
  );
}

function DevicePanel({ device, schedules, logs, serviceTypes, onClose, open, onDeleteDevice, onAddServiceType, onDeleteServiceType }) {
  if (!device) return null;
  const devScheds   = schedules.filter(s => s.device_id === device.id);
  const devLogs     = logs.filter(l => l.device_id === device.id);
  const devServices = serviceTypes.filter(s => s.device_id === device.id);
  const devSpend    = devLogs.reduce((a, l) => a + (l.cost_cad || 0), 0);
  const nextDue     = devScheds.filter(s => s.is_active).sort((a, b) => a.next_due_date.localeCompare(b.next_due_date))[0];
  const catColor    = CAT_COLORS[device.category] || '#6b7280';
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [showAddST, setShowAddST] = useState(false);
  const [newSTName, setNewSTName] = useState('');
  const [newSTFreq, setNewSTFreq] = useState(90);
  const [newSTDue, setNewSTDue] = useState('2026-07-20');
  const [newSTParts, setNewSTParts] = useState('');
  const [newSTNotes, setNewSTNotes] = useState('');
  const [deletingST, setDeletingST] = useState(null);
  const [selectedST, setSelectedST] = useState(null);

  const submitST = () => {
    if (!newSTName) return;
    onAddServiceType({
      device_id: device.id,
      name: newSTName,
      frequency_days: parseInt(newSTFreq),
      part_numbers: newSTParts ? newSTParts.split(',').map(p => p.trim()).filter(Boolean) : [],
      notes: newSTNotes || null,
      tutorial_url: null, purchase_url: null,
    }, newSTDue);
    setNewSTName(''); setNewSTFreq(90); setNewSTParts(''); setNewSTNotes(''); setShowAddST(false);
  };

  return (
    <>
    <SidePanel open={open} onClose={onClose} title={device.name} subtitle={device.category}>
      {/* Device image */}
      <div style={{ height: 140, borderRadius: 10, overflow: 'hidden', background: '#f0f0ee', marginBottom: 16, position: 'relative' }}>
        <img src={DEVICE_IMAGES[device.id]} alt={device.name}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          onError={e => { e.target.style.display = 'none'; }} />
        <div style={{ position: 'absolute', bottom: 8, right: 8 }}>
          <Btn size="sm" variant="secondary" disabled style={{ fontSize: 11, opacity: 0.8 }}>
            📸 Update photo
          </Btn>
        </div>
      </div>
      {/* Specs */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 16 }}>
        {[
          { label: 'Model',      val: device.model },
          { label: 'Serial',     val: device.serial },
          { label: 'Purchased',  val: formatDate(device.purchase_date) },
          { label: 'Warranty',   val: formatDate(device.warranty_expiry) },
          { label: 'Total Spend', val: devSpend > 0 ? formatMoney(devSpend) : '—' },
          { label: 'YTD Spend',  val: formatMoney(devLogs.filter(l => l.completion_date >= '2026-01-01').reduce((a,l) => a + (l.cost_cad||0), 0)) || '—' },
          { label: 'Next Due',   val: nextDue ? formatDate(nextDue.next_due_date) : '—' },
          { label: 'Last Service', val: devLogs.length > 0 ? formatDate(devLogs.sort((a,b) => b.completion_date.localeCompare(a.completion_date))[0].completion_date) : '—' },
        ].map(row => (
          <div key={row.label} style={{ background: '#f8f7f5', borderRadius: 8, padding: '8px 12px' }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{row.label}</div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e', marginTop: 2 }}>{row.val || '—'}</div>
          </div>
        ))}
      </div>

      {device.notes && (
        <div style={{ background: '#fffbeb', border: '1px solid #fde68a', borderRadius: 8, padding: '8px 12px', fontSize: 12, color: '#92400e', marginBottom: 20 }}>
          💡 {device.notes}
        </div>
      )}



      {/* Service types */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', margin: '20px 0 10px' }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Service Types</span>
        <Btn size="sm" variant="secondary" onClick={() => setShowAddST(s => !s)}>+ Add</Btn>
      </div>

      {/* Add service type form */}
      {showAddST && (
        <Card style={{ padding: '14px 16px', marginBottom: 12, borderColor: '#e8823a' }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 10 }}>New Service Type</div>
          <input placeholder="Name *" value={newSTName} onChange={e => setNewSTName(e.target.value)}
            style={{ width: '100%', padding: '7px 10px', borderRadius: 7, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit', marginBottom: 8 }} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 8 }}>
            <div>
              <div style={{ fontSize: 11, color: '#9ca3af', marginBottom: 3 }}>Repeat every (days)</div>
              <input type="number" value={newSTFreq} onChange={e => setNewSTFreq(e.target.value)}
                style={{ width: '100%', padding: '7px 10px', borderRadius: 7, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit' }} />
            </div>
            <div>
              <div style={{ fontSize: 11, color: '#9ca3af', marginBottom: 3 }}>First due date</div>
              <input type="date" value={newSTDue} onChange={e => setNewSTDue(e.target.value)}
                style={{ width: '100%', padding: '7px 10px', borderRadius: 7, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit' }} />
            </div>
          </div>
          <input placeholder="Part numbers (comma-separated)" value={newSTParts} onChange={e => setNewSTParts(e.target.value)}
            style={{ width: '100%', padding: '7px 10px', borderRadius: 7, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit', marginBottom: 8 }} />
          <input placeholder="Notes" value={newSTNotes} onChange={e => setNewSTNotes(e.target.value)}
            style={{ width: '100%', padding: '7px 10px', borderRadius: 7, border: '1px solid #e5e5e3', fontSize: 12, fontFamily: 'inherit', marginBottom: 10 }} />
          <div style={{ display: 'flex', gap: 8 }}>
            <Btn size="sm" onClick={submitST} disabled={!newSTName}>Save</Btn>
            <Btn size="sm" variant="ghost" onClick={() => setShowAddST(false)}>Cancel</Btn>
          </div>
        </Card>
      )}

      {devServices.length === 0 && !showAddST && (
        <div style={{ fontSize: 13, color: '#9ca3af', marginBottom: 16 }}>No service types yet — add one above.</div>
      )}
      {devServices.map(st => {
        const sched = devScheds.find(s => s.service_type_id === st.id);
        const days  = sched ? daysUntil(sched.next_due_date) : null;
        const si    = statusInfo(days);
        const isDeleting = deletingST === st.id;
        return (
          <Card key={st.id} style={{ padding: '12px 14px', marginBottom: 10, cursor: 'pointer' }} accent={days !== null && days <= 7 ? si.dot : undefined} onClick={() => setSelectedST(st)}>
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 8 }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                  <span style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e' }}>{st.name}</span>
                  <Badge type="neutral">{freqLabel(st.frequency_days)}</Badge>
                  {sched && <Badge type={si.status}>{si.label}</Badge>}
                </div>
                {st.part_numbers.length > 0 && (
                  <div style={{ fontSize: 11, color: '#6b7280', marginTop: 4 }}>Parts: {st.part_numbers.join(', ')}</div>
                )}
                {st.notes && <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 2 }}>{st.notes}</div>}
              </div>
              {!isDeleting ? (
                <button onClick={() => setDeletingST(st.id)} title="Delete service type"
                  style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#d1d5db', fontSize: 14, padding: '2px 4px', lineHeight: 1 }}
                  onMouseEnter={e => e.currentTarget.style.color = '#ef4444'}
                  onMouseLeave={e => e.currentTarget.style.color = '#d1d5db'}>✕</button>
              ) : (
                <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                  <span style={{ fontSize: 11, color: '#6b7280' }}>Delete?</span>
                  <Btn size="sm" variant="danger" onClick={() => { onDeleteServiceType(st.id); setDeletingST(null); }}>Yes</Btn>
                  <Btn size="sm" variant="ghost" onClick={() => setDeletingST(null)}>No</Btn>
                </div>
              )}
            </div>
            <div style={{ display: 'flex', gap: 8, marginTop: 10, flexWrap: 'wrap', alignItems: 'center' }}>
              <AIBlock label="Find Parts" icon="✦"
                prompt={`I need to do "${st.name}" on a ${device.model || device.name}. What exact replacement parts do I need? For each part: 1) Part name and number, 2) Direct Amazon.ca search link or ASIN if known, 3) Price estimate in CAD. Format as a short list. Prioritize Amazon.ca links.`} />
              <AIBlock label="Find Tutorial" icon="▶"
                prompt={`How do I do "${st.name}" on a ${device.model || device.name}? Give me: 1) Best YouTube search terms to find a tutorial, 2) Step-by-step overview in 4-5 steps, 3) Tools needed. Keep it brief and practical.`} />
              <span style={{ fontSize: 10, color: '#d1d5db', display: 'flex', alignItems: 'center', gap: 3 }}>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="#f90"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>
                <span style={{ color: '#9ca3af' }}>Parts will link to Amazon.ca</span>
              </span>
            </div>
          </Card>
        );
      })}

      {/* Maintenance history */}
      {devLogs.length > 0 && (
        <>
          <Divider label={`History (${devLogs.length})`} />
          {devLogs.slice(0, 6).map(l => (
            <div key={l.id} style={{
              display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0',
              borderBottom: '1px solid #f5f5f3', fontSize: 12,
            }}>
              <div style={{ color: '#9ca3af', width: 75, flexShrink: 0 }}>{l.completion_date.slice(5)}/{l.completion_date.slice(0,4)}</div>
              <div style={{ flex: 1, color: '#374151' }}>{l.task_performed}</div>
              <div style={{ color: '#6b7280', flexShrink: 0 }}>{l.cost_cad > 0 ? formatMoney(l.cost_cad) : '—'}</div>
            </div>
          ))}
        </>
      )}

      {/* Delete device */}
      <div style={{ marginTop: 32, paddingTop: 16, borderTop: '1px solid #f0f0ee' }}>
        {!confirmDelete ? (
          <Btn variant="ghost" size="sm" onClick={() => setConfirmDelete(true)}
            style={{ color: '#ef4444' }}>
            Delete device…
          </Btn>
        ) : (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, padding: '12px 14px' }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#dc2626', marginBottom: 8 }}>
              Delete {device.name}?
            </div>
            <div style={{ fontSize: 12, color: '#6b7280', marginBottom: 12 }}>
              All linked service types, schedules, and maintenance history will also be deleted.
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <Btn size="sm" variant="danger" onClick={() => { onDeleteDevice(device.id); onClose(); }}>Yes, delete</Btn>
              <Btn size="sm" variant="ghost" onClick={() => setConfirmDelete(false)}>Cancel</Btn>
            </div>
          </div>
        )}
      </div>
    </SidePanel>

    <ServiceTypePanel
      st={selectedST}
      device={device}
      logs={logs}
      schedules={schedules}
      open={!!selectedST}
      onClose={() => setSelectedST(null)}
      onDelete={(id) => { onDeleteServiceType(id); setSelectedST(null); }}
      onUpdate={(updated) => { setSelectedST(null); }}
    />
    </>
  );
}

function Devices({ devices, schedules, logs, serviceTypes, onDeleteDevice, onAddServiceType, onDeleteServiceType }) {
  const [search, setSearch] = useState('');
  const [catFilter, setCatFilter] = useState('All');
  const [showArchived, setShowArchived] = useState(false);
  const [selectedId, setSelectedId] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);

  const open = (id) => { setSelectedId(id); setPanelOpen(true); };
  const close = () => setPanelOpen(false);

  const filtered = devices.filter(d => {
    if (!showArchived && d.is_archived) return false;
    if (catFilter !== 'All' && d.category !== catFilter) return false;
    if (search && !d.name.toLowerCase().includes(search.toLowerCase()) && !(d.model || '').toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const getDevStatus = (dev) => {
    const devScheds = schedules.filter(s => s.device_id === dev.id && s.is_active);
    if (devScheds.length === 0) return null;
    const minDays = Math.min(...devScheds.map(s => daysUntil(s.next_due_date)));
    return minDays;
  };

  const selectedDevice = devices.find(d => d.id === selectedId);

  return (
    <div>
      <SectionHead
        title="Devices"
        action={<Btn size="sm" onClick={() => {}}>+ Add Device</Btn>}
      />

      {/* Filters */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 20, flexWrap: 'wrap' }}>
        <input
          placeholder="Search devices…"
          value={search} onChange={e => setSearch(e.target.value)}
          style={{
            flex: 1, minWidth: 200, padding: '8px 12px', borderRadius: 8,
            border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit',
            background: '#fff', outline: 'none',
          }}
        />
        <select value={catFilter} onChange={e => setCatFilter(e.target.value)}
          style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', cursor: 'pointer' }}>
          <option value="All">All categories</option>
          {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: '#6b7280', cursor: 'pointer' }}>
          <input type="checkbox" checked={showArchived} onChange={e => setShowArchived(e.target.checked)} />
          Show archived
        </label>
      </div>

      {/* Device grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(dev => {
          const days = getDevStatus(dev);
          const si = statusInfo(days);
          const devLogs = logs.filter(l => l.device_id === dev.id);
          const lastLog = devLogs.sort((a, b) => b.completion_date.localeCompare(a.completion_date))[0];
          const catColor = CAT_COLORS[dev.category] || '#6b7280';
          return (
            <Card key={dev.id} onClick={() => open(dev.id)} accent={si.dot} style={{ padding: '12px 16px', overflow: 'hidden' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 8, marginBottom: 6 }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: dev.is_archived ? '#9ca3af' : '#1c1c1e' }}>
                    {dev.is_archived ? '🗄 ' : ''}{dev.name}
                  </div>
                  <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 1 }}>{dev.model || '—'}</div>
                </div>
                <Badge type={si.status}>{si.label}</Badge>
              </div>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8 }}>
                <span style={{
                  fontSize: 10, fontWeight: 600, padding: '2px 8px', borderRadius: 20,
                  background: catColor + '18', color: catColor, border: `1px solid ${catColor}30`,
                }}>{dev.category}</span>
                {dev.warranty_expiry && new Date(dev.warranty_expiry) < new Date('2026-12-31') && (
                  <Badge type="soon" small>Warranty expiring</Badge>
                )}
              </div>
              <div style={{ fontSize: 11, color: '#9ca3af', borderTop: '1px solid #f5f5f3', paddingTop: 8, display: 'flex', justifyContent: 'space-between' }}>
                <span>Last: {lastLog ? lastLog.completion_date.slice(5) + '/' + lastLog.completion_date.slice(2,4) : 'Never'}</span>
                <span style={{ color: '#e8823a', fontWeight: 600 }}>Open ↗</span>
              </div>
            </Card>
          );
        })}
        {/* Add device card */}
        <div onClick={() => {}} style={{
          border: '1.5px dashed #d1d5db', borderRadius: 12, padding: '32px 16px',
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          gap: 8, cursor: 'pointer', color: '#9ca3af', transition: 'all 0.15s',
          minHeight: 130,
        }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = '#e8823a'; e.currentTarget.style.color = '#e8823a'; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = '#d1d5db'; e.currentTarget.style.color = '#9ca3af'; }}>
          <span style={{ fontSize: 24 }}>+</span>
          <span style={{ fontSize: 13, fontWeight: 600 }}>Add Device</span>
        </div>
      </div>

      <DevicePanel
        device={selectedDevice} schedules={schedules} logs={logs}
        serviceTypes={serviceTypes} open={panelOpen} onClose={close}
        onDeleteDevice={onDeleteDevice} onAddServiceType={onAddServiceType} onDeleteServiceType={onDeleteServiceType}
      />
    </div>
  );
}

// ── Log Detail Panel ──────────────────────────────────────────────────────────
function LogDetailPanel({ log, device, open, onClose }) {
  if (!log) return null;
  return (
    <SidePanel open={open} onClose={onClose}
      title={device?.name || '—'}
      subtitle={log.completion_date}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 20 }}>
        {[
          { label: 'Date',         val: log.completion_date },
          { label: 'Cost',         val: log.cost_cad > 0 ? formatMoney(log.cost_cad) : 'No cost' },
          { label: 'Category',     val: device?.category },
          { label: 'Sourcing',     val: log.sourcing_info },
        ].map(r => (
          <div key={r.label} style={{ background: '#f8f7f5', borderRadius: 8, padding: '8px 12px' }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{r.label}</div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e', marginTop: 2 }}>{r.val || '—'}</div>
          </div>
        ))}
      </div>
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 6 }}>Task Performed</div>
        <div style={{ fontSize: 15, fontWeight: 600, color: '#1c1c1e' }}>{log.task_performed}</div>
      </div>
      {log.notes && (
        <div style={{ background: '#fffbeb', border: '1px solid #fde68a', borderRadius: 8, padding: '10px 12px', fontSize: 13, color: '#92400e' }}>
          💡 {log.notes}
        </div>
      )}
    </SidePanel>
  );
}

function Maintenance({ devices, logs, schedules, serviceTypes, onAddLog }) {
  const [showForm, setShowForm] = useState(false);
  const [devFilter, setDevFilter] = useState('all');
  const [catFilter, setCatFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [task, setTask] = useState('');
  const [selDev, setSelDev] = useState(devices[0]?.id || null);
  const [cost, setCost] = useState('');
  const [notes, setNotes] = useState('');
  const [date, setDate] = useState('2026-04-20');
  const [selectedLog, setSelectedLog] = useState(null);

  const filtered = logs.filter(l => {
    if (devFilter !== 'all' && l.device_id !== parseInt(devFilter)) return false;
    const dev = devices.find(d => d.id === l.device_id);
    if (catFilter !== 'all' && dev?.category !== catFilter) return false;
    if (search && !l.task_performed.toLowerCase().includes(search.toLowerCase()) &&
        !(dev?.name || '').toLowerCase().includes(search.toLowerCase())) return false;
    if (dateFrom && l.completion_date < dateFrom) return false;
    if (dateTo && l.completion_date > dateTo) return false;
    return true;
  });

  const submit = () => {
    if (!task || !selDev) return;
    onAddLog({ device_id: selDev, task_performed: task, completion_date: date, cost_cad: parseFloat(cost) || 0, notes: notes || null, sourcing_info: null, service_type_id: null });
    setTask(''); setCost(''); setNotes(''); setShowForm(false);
  };

  const actionItems = schedules.filter(s => s.is_active && daysUntil(s.next_due_date) <= 7);

  return (
    <div>
      <SectionHead
        title="Maintenance"
        action={<Btn size="sm" onClick={() => setShowForm(f => !f)}>+ Log Entry</Btn>}
      />

      {/* Due tasks prompt */}
      {actionItems.length > 0 && !showForm && (
        <Card style={{ padding: '12px 16px', background: '#fffbeb', borderColor: '#fde68a', marginBottom: 20 }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: '#b45309', marginBottom: 8 }}>⚠ {actionItems.length} task(s) due — log them below</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {actionItems.slice(0, 5).map(s => {
              const dev = devices.find(d => d.id === s.device_id) || {};
              return (
                <Btn key={s.id} size="sm" variant="secondary" onClick={() => {
                  setSelDev(s.device_id);
                  setTask(s.task_description);
                  setShowForm(true);
                }}>
                  {dev.name}: {s.task_description}
                </Btn>
              );
            })}
          </div>
        </Card>
      )}

      {/* Log form */}
      {showForm && (
        <Card style={{ padding: '16px 20px', marginBottom: 20, borderColor: '#e8823a' }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: '#1c1c1e', marginBottom: 14 }}>New Entry</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
            <select value={selDev || ''} onChange={e => setSelDev(parseInt(e.target.value))}
              style={{ padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }}>
              {devices.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
            </select>
            <input type="date" value={date} onChange={e => setDate(e.target.value)}
              style={{ padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
          <input placeholder="Task performed *" value={task} onChange={e => setTask(e.target.value)}
            style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', marginBottom: 10, boxSizing: 'border-box' }} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 10, marginBottom: 14 }}>
            <input placeholder="Cost (CAD)" type="number" value={cost} onChange={e => setCost(e.target.value)}
              style={{ padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
            <input placeholder="Notes (optional)" value={notes} onChange={e => setNotes(e.target.value)}
              style={{ padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Btn onClick={submit} disabled={!task}>Save Entry</Btn>
            <Btn variant="ghost" onClick={() => setShowForm(false)}>Cancel</Btn>
          </div>
        </Card>
      )}

      {/* Filters */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap', alignItems: 'center' }}>
        <input
          placeholder="Search tasks or devices…"
          value={search} onChange={e => setSearch(e.target.value)}
          style={{ flex: '1 1 180px', padding: '7px 12px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', outline: 'none' }}
        />
        <select value={devFilter} onChange={e => setDevFilter(e.target.value)}
          style={{ padding: '7px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', cursor: 'pointer' }}>
          <option value="all">All devices</option>
          {devices.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <select value={catFilter} onChange={e => setCatFilter(e.target.value)}
          style={{ padding: '7px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', cursor: 'pointer' }}>
          <option value="all">All categories</option>
          {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)}
          title="From date"
          style={{ padding: '7px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', color: dateFrom ? '#1c1c1e' : '#9ca3af' }} />
        <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)}
          title="To date"
          style={{ padding: '7px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit', background: '#fff', color: dateTo ? '#1c1c1e' : '#9ca3af' }} />
        {(search || devFilter !== 'all' || catFilter !== 'all' || dateFrom || dateTo) && (
          <Btn size="sm" variant="ghost" onClick={() => { setSearch(''); setDevFilter('all'); setCatFilter('all'); setDateFrom(''); setDateTo(''); }}>
            Clear
          </Btn>
        )}
        <div style={{ fontSize: 13, color: '#6b7280', marginLeft: 4 }}>
          {filtered.length} {filtered.length === 1 ? 'entry' : 'entries'}
          {filtered.length > 0 && ` · ${formatMoney(filtered.reduce((a, l) => a + (l.cost_cad || 0), 0))}`}
        </div>
      </div>

      {filtered.length === 0 ? (
        <EmptyState icon="📋" title="No entries yet" sub="Log your first maintenance task above." />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {filtered.map(l => {
            const dev = devices.find(d => d.id === l.device_id) || {};
            const stName = serviceTypeName(serviceTypes, l.service_type_id);
            return (
              <Card key={l.id} style={{ padding: '11px 16px' }} onClick={() => setSelectedLog(l)}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{ width: 70, flexShrink: 0, fontSize: 12, color: '#9ca3af' }}>{l.completion_date}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e' }}>{l.task_performed}</div>
                    <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 1 }}>{dev.name}{stName ? ` · ${stName}` : ''}{l.notes ? ` · ${l.notes}` : ''}</div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: l.cost_cad > 0 ? '#374151' : '#d1d5db' }}>
                      {l.cost_cad > 0 ? formatMoney(l.cost_cad) : '—'}
                    </div>
                    <span style={{ fontSize: 11, color: '#d1d5db' }}>↗</span>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <LogDetailPanel
        log={selectedLog}
        device={selectedLog ? devices.find(d => d.id === selectedLog.device_id) : null}
        open={!!selectedLog}
        onClose={() => setSelectedLog(null)}
      />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// VIEW: SCHEDULES
// ══════════════════════════════════════════════════════════════════════════════

function SchedulePanel({ schedule, device, open, onClose, onSave, onDelete, onToggle }) {
  if (!schedule) return null;
  const si = statusInfo(daysUntil(schedule.next_due_date));
  const [task, setTask] = useState(schedule.task_description);
  const [dueDate, setDueDate] = useState(schedule.next_due_date);
  const [freq, setFreq] = useState(schedule.frequency_days);
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    setTask(schedule.task_description);
    setDueDate(schedule.next_due_date);
    setFreq(schedule.frequency_days);
    setConfirmDelete(false);
  }, [schedule.id]);

  return (
    <SidePanel open={open} onClose={onClose}
      title={schedule.task_description}
      subtitle={device?.name}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 20 }}>
        {[
          { label: 'Status',    val: <Badge type={si.status}>{si.label}</Badge> },
          { label: 'Frequency', val: freqLabel(schedule.frequency_days) },
          { label: 'Next Due',  val: schedule.next_due_date },
          { label: 'Active',    val: schedule.is_active ? 'Yes' : 'Paused' },
        ].map(r => (
          <div key={r.label} style={{ background: '#f8f7f5', borderRadius: 8, padding: '8px 12px' }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{r.label}</div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#1c1c1e', marginTop: 3 }}>{r.val}</div>
          </div>
        ))}
      </div>

      <Divider label="Edit" />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
        <div>
          <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Task description</div>
          <input value={task} onChange={e => setTask(e.target.value)}
            style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
          <div>
            <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Next due date</div>
            <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)}
              style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
          <div>
            <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Repeat every (days)</div>
            <input type="number" value={freq} onChange={e => setFreq(e.target.value)}
              style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <Btn onClick={() => { onSave(schedule.id, task, dueDate, parseInt(freq)); onClose(); }}>Save Changes</Btn>
          <Btn variant="secondary" onClick={() => { onToggle(schedule.id); onClose(); }}>
            {schedule.is_active ? '⏸ Pause' : '▶ Resume'}
          </Btn>
        </div>
      </div>

      <div style={{ paddingTop: 16, borderTop: '1px solid #f0f0ee' }}>
        {!confirmDelete ? (
          <Btn variant="ghost" size="sm" onClick={() => setConfirmDelete(true)} style={{ color: '#ef4444' }}>Delete schedule…</Btn>
        ) : (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, padding: '12px 14px' }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#dc2626', marginBottom: 8 }}>Delete this schedule?</div>
            <div style={{ display: 'flex', gap: 8 }}>
              <Btn size="sm" variant="danger" onClick={() => { onDelete(schedule.id); onClose(); }}>Yes, delete</Btn>
              <Btn size="sm" variant="ghost" onClick={() => setConfirmDelete(false)}>Cancel</Btn>
            </div>
          </div>
        )}
      </div>
    </SidePanel>
  );
}

function Schedules({ devices, schedules, onToggle, onSave, onDelete }) {
  const [showInactive, setShowInactive] = useState(false);
  const [selectedSched, setSelectedSched] = useState(null);
  const active = schedules.filter(s => s.is_active || showInactive);

  const groups = [
    { label: 'Overdue',    items: active.filter(s => daysUntil(s.next_due_date) < 0),                                          color: '#dc2626' },
    { label: 'This Week',  items: active.filter(s => daysUntil(s.next_due_date) >= 0 && daysUntil(s.next_due_date) <= 7),      color: '#d97706' },
    { label: 'This Month', items: active.filter(s => daysUntil(s.next_due_date) > 7  && daysUntil(s.next_due_date) <= 30),     color: '#2563eb' },
    { label: 'Later',      items: active.filter(s => daysUntil(s.next_due_date) > 30),                                         color: '#16a34a' },
  ].filter(g => g.items.length > 0);

  return (
    <div>
      <SectionHead
        title="Schedules"
        action={
          <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: '#6b7280', cursor: 'pointer' }}>
              <input type="checkbox" checked={showInactive} onChange={e => setShowInactive(e.target.checked)} />
              Show paused
            </label>
            <Btn size="sm" variant="secondary">+ Manual</Btn>
          </div>
        }
      />

      {groups.map(g => (
        <div key={g.label} style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: g.color, display: 'inline-block' }} />
            <span style={{ fontSize: 12, fontWeight: 700, color: g.color, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{g.label}</span>
            <span style={{ fontSize: 12, color: '#9ca3af' }}>({g.items.length})</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {g.items.map(s => {
              const dev = devices.find(d => d.id === s.device_id) || {};
              const si = statusInfo(daysUntil(s.next_due_date));
              return (
                <Card key={s.id} style={{ padding: '11px 16px' }} accent={si.dot} onClick={() => setSelectedSched(s)}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ fontSize: 13, fontWeight: 600, color: s.is_active ? '#1c1c1e' : '#9ca3af' }}>
                          {!s.is_active && '⏸ '}{s.task_description}
                        </span>
                        <Badge type={si.status}>{si.label}</Badge>
                        {s.calendar_event_id && <Badge type="blue">🗓 Synced</Badge>}
                      </div>
                      <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 2 }}>
                        {dev.name} · {freqLabel(s.frequency_days)} · Due {s.next_due_date}
                      </div>
                    </div>
                    <span style={{ fontSize: 11, color: '#d1d5db' }}>↗</span>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      ))}

      <SchedulePanel
        schedule={selectedSched}
        device={selectedSched ? devices.find(d => d.id === selectedSched.device_id) : null}
        open={!!selectedSched} onClose={() => setSelectedSched(null)}
        onSave={onSave} onDelete={onDelete} onToggle={onToggle}
      />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// VIEW: NOTIFICATIONS
// ══════════════════════════════════════════════════════════════════════════════

function Notifications({ schedules, devices }) {
  const linked = schedules.filter(s => s.calendar_event_id);
  const unlinked = schedules.filter(s => !s.calendar_event_id);
  const [calConnected, setCalConnected] = useState(true);
  const [calEmail, setCalEmail] = useState('sergey.pochikovskiy@gmail.com');

  return (
    <div>
      <SectionHead title="Integrations" />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 640 }}>

        {/* Google Calendar */}
        <Card style={{ padding: '20px 24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ width: 36, height: 36, borderRadius: 8, background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#2563eb" strokeWidth="1.5"/><path d="M3 9h18M8 2v4M16 2v4" stroke="#2563eb" strokeWidth="1.5" strokeLinecap="round"/></svg>
              </div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: '#1c1c1e' }}>Google Calendar</div>
                <div style={{ fontSize: 11, color: '#9ca3af' }}>Push schedules as recurring all-day events</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 12, color: calConnected ? '#15803d' : '#9ca3af', fontWeight: 600 }}>
                {calConnected ? '● Connected' : '○ Not connected'}
              </span>
              <Btn size="sm" variant={calConnected ? 'secondary' : 'primary'} onClick={() => setCalConnected(c => !c)}>
                {calConnected ? 'Disconnect' : 'Connect'}
              </Btn>
            </div>
          </div>
          {calConnected && (
            <>
              <div style={{ display: 'flex', gap: 10, marginBottom: 12 }}>
                <div style={{ background: '#f0fdf4', borderRadius: 8, padding: '8px 14px', flex: 1, textAlign: 'center' }}>
                  <div style={{ fontSize: 20, fontWeight: 800, color: '#15803d' }}>{linked.length}</div>
                  <div style={{ fontSize: 11, color: '#6b7280' }}>Synced</div>
                </div>
                <div style={{ background: '#f8f7f5', borderRadius: 8, padding: '8px 14px', flex: 1, textAlign: 'center' }}>
                  <div style={{ fontSize: 20, fontWeight: 800, color: '#374151' }}>{unlinked.length}</div>
                  <div style={{ fontSize: 11, color: '#6b7280' }}>Unsynced</div>
                </div>
              </div>
              <div style={{ fontSize: 12, color: '#6b7280' }}>
                Push individual schedules to calendar from the <strong>Schedules</strong> view or from a device's schedule panel.
              </div>
            </>
          )}
        </Card>

        {/* Account */}
        <Card style={{ padding: '20px 24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <div style={{ width: 36, height: 36, borderRadius: 8, background: '#f5f3ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="#7c3aed" strokeWidth="1.5"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#7c3aed" strokeWidth="1.5" strokeLinecap="round"/></svg>
            </div>
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: '#1c1c1e' }}>Account</div>
              <div style={{ fontSize: 11, color: '#9ca3af' }}>Profile and notification preferences</div>
            </div>
          </div>
          <div style={{ display: 'grid', gap: 10 }}>
            <div>
              <div style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>Email</div>
              <input value={calEmail} onChange={e => setCalEmail(e.target.value)}
                style={{ width: '100%', padding: '8px 10px', borderRadius: 8, border: '1px solid #e5e5e3', fontSize: 13, fontFamily: 'inherit' }} />
            </div>
            <Btn size="sm" variant="secondary" style={{ alignSelf: 'flex-start' }}>Save</Btn>
          </div>
        </Card>

      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// VIEW: ROADMAP
// ══════════════════════════════════════════════════════════════════════════════

function Roadmap() {
  const items = [
    { phase: 'Phase 1 — Now', status: 'live', features: [
      { label: 'Device inventory with service types', done: true },
      { label: 'Maintenance history log', done: true },
      { label: 'Schedule management', done: true },
      { label: 'Google Calendar sync', done: true },
      { label: 'AI-powered parts finder', done: true },
      { label: 'AI-powered tutorial finder', done: true },
    ]},
    { phase: 'Phase 2 — Next', status: 'next', features: [
      { label: 'Photo upload → AI device identification', done: false },
      { label: 'Spend analytics & cost projections', done: false },
      { label: 'Amazon.ca parts linking (with referral)', done: false },
      { label: 'Mobile-optimized view', done: false },
    ]},
    { phase: 'Phase 3 — Future', status: 'future', features: [
      { label: 'Multi-unit / building manager mode', done: false },
      { label: 'Shared maintenance templates per building type', done: false },
      { label: 'Individual unit owner accounts', done: false },
      { label: 'AI maintenance assistant (chat)', done: false },
      { label: 'Service provider booking', done: false },
    ]},
  ];

  const statusColors = { live: '#15803d', next: '#2563eb', future: '#7c3aed' };
  const statusBg     = { live: '#f0fdf4', next: '#eff6ff', future: '#f5f3ff' };

  return (
    <div>
      <SectionHead title="Roadmap" />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 600 }}>
        {items.map(group => (
          <Card key={group.phase} style={{ padding: '18px 22px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
              <span style={{ fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 20, background: statusBg[group.status], color: statusColors[group.status] }}>
                {group.phase}
              </span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {group.features.map(f => (
                <div key={f.label} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <div style={{
                    width: 16, height: 16, borderRadius: '50%', flexShrink: 0,
                    background: f.done ? statusColors[group.status] : 'transparent',
                    border: `1.5px solid ${f.done ? statusColors[group.status] : '#d1d5db'}`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}>
                    {f.done && <svg width="8" height="8" viewBox="0 0 8 8"><path d="M1.5 4L3.5 6L6.5 2" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>}
                  </div>
                  <span style={{ fontSize: 13, color: f.done ? '#1c1c1e' : '#6b7280', fontWeight: f.done ? 500 : 400 }}>{f.label}</span>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// MAIN APP
// ══════════════════════════════════════════════════════════════════════════════

function App() {
  const [nav, setNav] = useState('dashboard');
  const [devices, setDevices] = useState(INITIAL_DEVICES);
  const [serviceTypes, setServiceTypes] = useState(INITIAL_SERVICE_TYPES);
  const [schedules, setSchedules] = useState(INITIAL_SCHEDULES);
  const [logs, setLogs] = useState(INITIAL_LOGS);
  const [toast, setToast] = useState(null);

  // Persist nav
  useEffect(() => {
    const saved = localStorage.getItem('hmt_nav');
    if (saved) setNav(saved);
  }, []);
  useEffect(() => { localStorage.setItem('hmt_nav', nav); }, [nav]);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  const handleCompleteTask = (sched, cost, notes) => {
    const newLog = {
      id: logs.length + 1,
      device_id: sched.device_id,
      service_type_id: sched.service_type_id,
      task_performed: sched.task_description,
      completion_date: '2026-04-20',
      cost_cad: cost,
      notes: notes || null,
      sourcing_info: null,
    };
    setLogs(l => [newLog, ...l]);
    setSchedules(ss => ss.map(s => s.id === sched.id
      ? { ...s, next_due_date: advanceDate(s.next_due_date, s.frequency_days) }
      : s
    ));
    showToast('✓ Task logged and schedule advanced.');
  };

  const handleAddLog = (log) => {
    setLogs(l => [{ ...log, id: logs.length + 1 }, ...l]);
    showToast('✓ Entry saved.');
  };

  const handleDeleteDevice = (id) => {
    setDevices(ds => ds.filter(d => d.id !== id));
    setSchedules(ss => ss.filter(s => s.device_id !== id));
    setLogs(ls => ls.filter(l => l.device_id !== id));
    setServiceTypes(st => st.filter(s => s.device_id !== id));
    showToast('Device deleted.');
  };

  const handleAddServiceType = (st, firstDueDate) => {
    const newId = serviceTypes.length + 100;
    const newST = { ...st, id: newId };
    setServiceTypes(s => [...s, newST]);
    setSchedules(ss => [...ss, {
      id: schedules.length + 100, device_id: st.device_id, service_type_id: newId,
      task_description: st.name, next_due_date: firstDueDate,
      frequency_days: st.frequency_days, is_active: true, calendar_event_id: null,
    }]);
    showToast('Service type added.');
  };

  const handleDeleteServiceType = (stId) => {
    setServiceTypes(s => s.filter(st => st.id !== stId));
    setSchedules(ss => ss.filter(s => s.service_type_id !== stId));
    showToast('Service type deleted.');
  };

  const handleToggleSchedule = (id) => {
    setSchedules(ss => ss.map(s => s.id === id ? { ...s, is_active: !s.is_active } : s));
  };

  const handleSaveSchedule = (id, task, dueDate, freq) => {
    setSchedules(ss => ss.map(s => s.id === id ? { ...s, task_description: task, next_due_date: dueDate, frequency_days: freq } : s));
    showToast('Schedule updated.');
  };

  const handleDeleteSchedule = (id) => {
    setSchedules(ss => ss.filter(s => s.id !== id));
    showToast('Schedule deleted.');
  };

  const stats = {
    deviceCount: devices.filter(d => !d.is_archived).length,
    overdue:     schedules.filter(s => s.is_active && daysUntil(s.next_due_date) < 0).length,
    dueSoon:     schedules.filter(s => s.is_active && daysUntil(s.next_due_date) >= 0 && daysUntil(s.next_due_date) <= 7).length,
    ytdSpend:    logs.filter(l => l.completion_date >= '2026-01-01').reduce((a, l) => a + (l.cost_cad || 0), 0),
  };

  const views = {
    dashboard:     <Dashboard devices={devices} schedules={schedules} logs={logs} serviceTypes={serviceTypes} onCompleteTask={handleCompleteTask} onNavigate={setNav} />,
    devices:       <Devices devices={devices} schedules={schedules} logs={logs} serviceTypes={serviceTypes} onDeleteDevice={handleDeleteDevice} onAddServiceType={handleAddServiceType} onDeleteServiceType={handleDeleteServiceType} />,
    maintenance:   <Maintenance devices={devices} logs={logs} schedules={schedules} serviceTypes={serviceTypes} onAddLog={handleAddLog} />,
    schedules:     <Schedules devices={devices} schedules={schedules} onToggle={handleToggleSchedule} onSave={handleSaveSchedule} onDelete={handleDeleteSchedule} />,
    notifications: <Notifications schedules={schedules} devices={devices} />,
    roadmap:       <Roadmap />,
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: "'DM Sans', sans-serif", background: '#f8f7f5' }}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        * { box-sizing: border-box; }
        input, select, button, textarea { font-family: inherit; }
        ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 99px; }
      `}</style>

      <Sidebar active={nav} onNav={setNav} stats={stats} />

      <main style={{ flex: 1, padding: '32px 36px', overflowY: 'auto', maxWidth: 1100 }}>
        {views[nav]}
      </main>

      {/* Toast */}
      {toast && (
        <div style={{
          position: 'fixed', bottom: 28, left: '50%', transform: 'translateX(-50%)',
          background: '#1c1c1e', color: '#fff', fontSize: 13, fontWeight: 600,
          padding: '10px 20px', borderRadius: 99, zIndex: 999,
          boxShadow: '0 4px 20px rgba(0,0,0,0.25)',
        }}>{toast}</div>
      )}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
