
// ── Shared UI primitives ────────────────────────────────────────────────────
// Exports to window: Badge, Card, Btn, SidePanel, Sidebar, EmptyState,
//                    formatDate, daysUntil, statusInfo, Spinner, Toast, useToast

const { useState, useEffect, useRef, useCallback, createContext, useContext } = React;

// ── Utilities ────────────────────────────────────────────────────────────────

function formatDate(d) {
  if (!d) return '—';
  const date = new Date(d + 'T12:00:00');
  return date.toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' });
}

function daysUntil(dateStr) {
  const today = new Date('2026-04-20T12:00:00');
  const due = new Date(dateStr + 'T12:00:00');
  return Math.round((due - today) / 86400000);
}

function statusInfo(days) {
  if (days === null || days === undefined) return { label: 'No schedule', status: 'neutral', color: '#9ca3af', dot: '#d1d5db' };
  if (days < 0)  return { label: `${Math.abs(days)}d overdue`, status: 'overdue', color: '#dc2626', dot: '#ef4444' };
  if (days === 0) return { label: 'Due today',   status: 'today',   color: '#c2410c', dot: '#f97316' };
  if (days <= 7)  return { label: `In ${days}d`, status: 'soon',    color: '#b45309', dot: '#f59e0b' };
  if (days <= 30) return { label: `In ${days}d`, status: 'upcoming',color: '#1d4ed8', dot: '#3b82f6' };
  return              { label: `In ${days}d`,    status: 'ok',      color: '#15803d', dot: '#22c55e' };
}

function formatMoney(v) {
  if (!v) return '—';
  return `$${v.toFixed(2)}`;
}

function freqLabel(days) {
  const map = { 7:'Weekly', 14:'Bi-weekly', 30:'Monthly', 60:'Every 2 mo', 90:'Quarterly', 180:'Semi-annual', 365:'Annual' };
  return map[days] || `Every ${days}d`;
}

// ── Badge ────────────────────────────────────────────────────────────────────

function Badge({ type = 'neutral', children, small }) {
  const s = {
    overdue:  { bg: '#fef2f2', color: '#dc2626', border: '#fecaca' },
    today:    { bg: '#fff7ed', color: '#c2410c', border: '#fed7aa' },
    soon:     { bg: '#fffbeb', color: '#b45309', border: '#fde68a' },
    upcoming: { bg: '#eff6ff', color: '#1d4ed8', border: '#bfdbfe' },
    ok:       { bg: '#f0fdf4', color: '#15803d', border: '#bbf7d0' },
    neutral:  { bg: '#f4f4f5', color: '#52525b', border: '#e4e4e7' },
    purple:   { bg: '#f5f3ff', color: '#6d28d9', border: '#ddd6fe' },
    blue:     { bg: '#eff6ff', color: '#1d4ed8', border: '#bfdbfe' },
  }[type] || { bg: '#f4f4f5', color: '#52525b', border: '#e4e4e7' };
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', whiteSpace: 'nowrap',
      fontSize: small ? 10 : 11, fontWeight: 600, letterSpacing: '0.03em',
      padding: small ? '1px 6px' : '2px 8px', borderRadius: 20,
      background: s.bg, color: s.color, border: `1px solid ${s.border}`,
    }}>{children}</span>
  );
}

// ── Spinner ──────────────────────────────────────────────────────────────────

function Spinner({ size = 16, color = '#e8823a' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" style={{ animation: 'spin 0.8s linear infinite' }}>
      <circle cx="8" cy="8" r="6" fill="none" stroke={color} strokeWidth="2" strokeDasharray="25 13" />
    </svg>
  );
}

// ── Button ───────────────────────────────────────────────────────────────────

function Btn({ variant = 'primary', size = 'md', onClick, children, disabled, full, style: extraStyle }) {
  const [hov, setHov] = useState(false);
  const base = {
    display: 'inline-flex', alignItems: 'center', gap: 6, cursor: disabled ? 'not-allowed' : 'pointer',
    fontFamily: 'inherit', fontWeight: 600, borderRadius: 8, border: 'none',
    transition: 'all 0.15s', opacity: disabled ? 0.5 : 1,
    width: full ? '100%' : undefined, justifyContent: full ? 'center' : undefined,
  };
  const sizes = { sm: { fontSize: 12, padding: '5px 12px' }, md: { fontSize: 13, padding: '8px 16px' }, lg: { fontSize: 14, padding: '10px 20px' } };
  const variants = {
    primary: { background: hov ? '#d4722f' : '#e8823a', color: '#fff' },
    secondary: { background: hov ? '#f0f0ee' : '#f8f7f5', color: '#374151', border: '1px solid #e5e5e3' },
    ghost: { background: hov ? '#f3f4f6' : 'transparent', color: '#374151' },
    danger: { background: hov ? '#dc2626' : '#ef4444', color: '#fff' },
    ai: { background: hov ? '#7c3aed' : '#8b5cf6', color: '#fff' },
  };
  return (
    <button
      style={{ ...base, ...sizes[size], ...variants[variant], ...extraStyle }}
      onClick={onClick} disabled={disabled}
      onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
    >{children}</button>
  );
}

// ── Card ─────────────────────────────────────────────────────────────────────

function Card({ children, style: extra, onClick, accent }) {
  const [hov, setHov] = useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
      style={{
        background: '#fff', borderRadius: 12, border: '1px solid #e5e5e3',
        boxShadow: hov && onClick ? '0 4px 16px rgba(0,0,0,0.08)' : '0 1px 4px rgba(0,0,0,0.04)',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.15s',
        borderLeft: accent ? `3px solid ${accent}` : undefined,
        ...extra,
      }}
    >{children}</div>
  );
}

// ── EmptyState ───────────────────────────────────────────────────────────────

function EmptyState({ icon, title, sub, action }) {
  return (
    <div style={{ textAlign: 'center', padding: '48px 24px', color: '#9ca3af' }}>
      <div style={{ fontSize: 32, marginBottom: 12 }}>{icon || '📭'}</div>
      <div style={{ fontSize: 15, fontWeight: 600, color: '#6b7280', marginBottom: 6 }}>{title}</div>
      {sub && <div style={{ fontSize: 13, marginBottom: action ? 16 : 0 }}>{sub}</div>}
      {action}
    </div>
  );
}

// ── SidePanel ────────────────────────────────────────────────────────────────

function SidePanel({ open, onClose, title, subtitle, children, width = 520 }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose(); };
    if (open) document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [open, onClose]);

  return (
    <>
      {/* Overlay */}
      <div
        onClick={onClose}
        style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.3)',
          zIndex: 200, opacity: open ? 1 : 0,
          pointerEvents: open ? 'auto' : 'none', transition: 'opacity 0.2s',
        }}
      />
      {/* Panel */}
      <div style={{
        position: 'fixed', top: 0, right: 0, bottom: 0, width,
        background: '#fff', zIndex: 201, display: 'flex', flexDirection: 'column',
        transform: open ? 'translateX(0)' : `translateX(${width}px)`,
        transition: 'transform 0.25s cubic-bezier(0.4,0,0.2,1)',
        boxShadow: '-4px 0 32px rgba(0,0,0,0.12)',
      }}>
        {/* Header */}
        <div style={{ padding: '20px 24px 16px', borderBottom: '1px solid #f0f0ee', flexShrink: 0 }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontSize: 17, fontWeight: 700, color: '#1c1c1e' }}>{title}</div>
              {subtitle && <div style={{ fontSize: 12, color: '#9ca3af', marginTop: 2 }}>{subtitle}</div>}
            </div>
            <button onClick={onClose} style={{
              background: '#f4f4f5', border: 'none', borderRadius: 8, width: 28, height: 28,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', fontSize: 16, color: '#6b7280', flexShrink: 0,
            }}>✕</button>
          </div>
        </div>
        {/* Body */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px 24px' }}>
          {children}
        </div>
      </div>
    </>
  );
}

// ── AI Block ─────────────────────────────────────────────────────────────────

function AIBlock({ prompt, label, icon = '✦' }) {
  const [state, setState] = useState({ status: 'idle', result: null, error: null });
  const run = async () => {
    setState({ status: 'loading', result: null, error: null });
    try {
      const result = await window.claude.complete(prompt);
      setState({ status: 'done', result, error: null });
    } catch(e) {
      setState({ status: 'error', result: null, error: e.message });
    }
  };
  return (
    <div style={{ marginTop: 8 }}>
      {state.status === 'idle' && (
        <Btn variant="ai" size="sm" onClick={run}>
          <span>{icon}</span> {label}
        </Btn>
      )}
      {state.status === 'loading' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: '#8b5cf6' }}>
          <Spinner size={14} color="#8b5cf6" /> Thinking…
        </div>
      )}
      {state.status === 'done' && (
        <div style={{
          background: '#faf5ff', border: '1px solid #e9d5ff', borderRadius: 8,
          padding: '10px 12px', fontSize: 12, color: '#374151', lineHeight: 1.6,
          whiteSpace: 'pre-wrap',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
            <span style={{ fontSize: 11, fontWeight: 700, color: '#7c3aed', letterSpacing: '0.05em' }}>✦ AI RESULT</span>
            <button onClick={() => setState({ status: 'idle', result: null, error: null })}
              style={{ background: 'none', border: 'none', fontSize: 11, color: '#9ca3af', cursor: 'pointer' }}>dismiss</button>
          </div>
          {state.result}
        </div>
      )}
      {state.status === 'error' && (
        <div style={{ fontSize: 12, color: '#dc2626' }}>Error: {state.error} <button onClick={() => setState({status:'idle',result:null,error:null})} style={{background:'none',border:'none',color:'#dc2626',cursor:'pointer',textDecoration:'underline'}}>retry</button></div>
      )}
    </div>
  );
}

// ── Sidebar ──────────────────────────────────────────────────────────────────

const NAV_ITEMS = [
  { id: 'dashboard',     icon: '⌂',  label: 'Dashboard'   },
  { id: 'devices',       icon: '⊞',  label: 'Devices'     },
  { id: 'maintenance',   icon: '⚙',  label: 'History'     },
  { id: 'schedules',     icon: '◷',  label: 'Schedules'   },
  { id: 'notifications', icon: '◉',  label: 'Integrations'},
  { id: 'roadmap',       icon: '◈',  label: 'Roadmap'     },
];

function Sidebar({ active, onNav, stats }) {
  return (
    <div style={{
      width: 220, flexShrink: 0, background: '#13192b',
      display: 'flex', flexDirection: 'column', height: '100vh',
      position: 'sticky', top: 0,
    }}>
      {/* Property switcher */}
      <div style={{
        margin: '16px 12px 12px', padding: '10px 12px', borderRadius: 10,
        background: '#1c2540', border: '1px solid #2a3659', cursor: 'pointer',
        display: 'flex', alignItems: 'center', gap: 10, transition: 'background 0.15s',
      }}
        onMouseEnter={e => e.currentTarget.style.background = '#243050'}
        onMouseLeave={e => e.currentTarget.style.background = '#1c2540'}
      >
        {/* Property icon */}
        <div style={{
          width: 32, height: 32, borderRadius: 8, background: '#e8823a',
          display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
        }}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M2 7L8 2L14 7V14H10V10H6V14H2V7Z" fill="white" />
          </svg>
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: '#f1f5f9', lineHeight: 1.2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>Squamish Home</div>
          <div style={{ fontSize: 10, color: '#64748b', marginTop: 1 }}>Squamish, BC</div>
        </div>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style={{ flexShrink: 0, color: '#475569' }}>
          <path d="M4 5.5L7 8.5L10 5.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>



      {/* Nav */}
      <nav style={{ flex: 1, padding: '0 8px' }}>
        {NAV_ITEMS.map(item => {
          const isActive = active === item.id;
          return (
            <button key={item.id} onClick={() => onNav(item.id)} style={{
              display: 'flex', alignItems: 'center', gap: 10, width: '100%',
              padding: '9px 12px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: isActive ? '#2a3659' : 'transparent',
              color: isActive ? '#fff' : '#94a3b8',
              fontSize: 13, fontWeight: isActive ? 600 : 400, fontFamily: 'inherit',
              marginBottom: 2, transition: 'all 0.1s', textAlign: 'left',
            }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = '#1c2540'; }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
            >
              <span style={{ fontSize: 14, width: 18, textAlign: 'center' }}>{item.icon}</span>
              {item.label}
              {item.id === 'dashboard' && stats.overdue > 0 && (
                <span style={{ marginLeft: 'auto', background: '#ef4444', color: '#fff', fontSize: 10, fontWeight: 700, borderRadius: 20, padding: '1px 6px', minWidth: 16, textAlign: 'center' }}>{stats.overdue}</span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom: user / settings */}
      <div style={{ padding: '12px 8px', borderTop: '1px solid #1e2a42' }}>
        <button style={{
          display: 'flex', alignItems: 'center', gap: 10, width: '100%',
          padding: '9px 12px', borderRadius: 8, border: 'none', cursor: 'pointer',
          background: 'transparent', color: '#94a3b8', fontSize: 13, fontFamily: 'inherit', textAlign: 'left',
          transition: 'background 0.1s',
        }}
          onMouseEnter={e => e.currentTarget.style.background = '#1c2540'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <div style={{
            width: 28, height: 28, borderRadius: '50%', background: '#2a3659',
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
            fontSize: 12, fontWeight: 700, color: '#94a3b8',
          }}>S</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: '#e2e8f0', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>Sergey P.</div>
            <div style={{ fontSize: 10, color: '#475569' }}>Owner</div>
          </div>
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" style={{ flexShrink: 0 }}>
            <circle cx="8" cy="8" r="2" stroke="#475569" strokeWidth="1.3"/>
            <path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.41 1.41M11.54 11.54l1.41 1.41M3.05 12.95l1.41-1.41M11.54 4.46l1.41-1.41" stroke="#475569" strokeWidth="1.3" strokeLinecap="round"/>
          </svg>
        </button>
        <button style={{
          display: 'flex', alignItems: 'center', gap: 10, width: '100%',
          padding: '7px 12px', borderRadius: 8, border: 'none', cursor: 'pointer',
          background: 'transparent', color: '#64748b', fontSize: 12, fontFamily: 'inherit', textAlign: 'left',
          transition: 'background 0.1s',
        }}
          onMouseEnter={e => e.currentTarget.style.background = '#1c2540'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" style={{ marginLeft: 7 }}>
            <path d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" stroke="#64748b" strokeWidth="1.3" strokeLinecap="round"/>
            <path d="M10 11l3-3-3-3" stroke="#64748b" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M13 8H6" stroke="#64748b" strokeWidth="1.3" strokeLinecap="round"/>
          </svg>
          Sign out
        </button>
      </div>
    </div>
  );
}

// ── Divider ──────────────────────────────────────────────────────────────────
function Divider({ label }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, margin: '20px 0 12px' }}>
      {label && <span style={{ fontSize: 11, fontWeight: 700, color: '#9ca3af', letterSpacing: '0.08em', textTransform: 'uppercase', whiteSpace: 'nowrap' }}>{label}</span>}
      <div style={{ flex: 1, height: 1, background: '#f0f0ee' }} />
    </div>
  );
}

// ── Section heading ──────────────────────────────────────────────────────────
function SectionHead({ title, action }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
      <h2 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: '#1c1c1e' }}>{title}</h2>
      {action}
    </div>
  );
}

// ── Export ────────────────────────────────────────────────────────────────────
Object.assign(window, {
  Badge, Card, Btn, SidePanel, AIBlock, EmptyState, Sidebar, Divider, SectionHead,
  Spinner, formatDate, daysUntil, statusInfo, formatMoney, freqLabel,
});
