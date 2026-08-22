const get = async (path) => {
  const response = await fetch(path, {headers: {'Accept': 'application/json'}});
  if (!response.ok) throw new Error(`${path} -> HTTP ${response.status}`);
  return response.json();
};

const humanKey = (key) => String(key || '')
  .replace(/_/g, ' ')
  .replace(/\b\w/g, c => c.toUpperCase());

const scalar = (value) => {
  if (value === null || value === undefined || value === '') return 'UNKNOWN';
  if (typeof value === 'boolean') return value ? 'YES' : 'NO';
  if (typeof value === 'number') return Number.isInteger(value) ? String(value) : value.toFixed(2);
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
};

function toneFor(value) {
  const v = String(value || '').toUpperCase();
  if (['READY','PASS','VERIFIED','ACTIVE','RECONCILED'].some(x => v.includes(x))) return 'is-emerald';
  if (['HOLD','FAIL','STALE','ISOLATE','REJECTED','ERROR'].some(x => v.includes(x))) return 'is-danger';
  if (['VERIFY','AGING','PENDING','UNKNOWN'].some(x => v.includes(x))) return 'is-gold';
  if (['BUILD','INCUBATE','SEED'].some(x => v.includes(x))) return 'is-ion';
  return '';
}

function makeValue(value, key='') {
  if (Array.isArray(value)) {
    const wrap = document.createElement('span');
    wrap.className = 'badge-list';
    value.slice(0, 8).forEach(item => {
      const badge = document.createElement('span');
      badge.className = 'data-badge';
      badge.textContent = scalar(item);
      wrap.appendChild(badge);
    });
    if (value.length > 8) {
      const more = document.createElement('span');
      more.className = 'data-badge';
      more.textContent = `+${value.length - 8} more`;
      wrap.appendChild(more);
    }
    return wrap;
  }

  const span = document.createElement('span');
  const text = scalar(value);
  span.className = `data-value ${toneFor(text)}`.trim();
  if (['state','status','organ','title','branch','next_action'].includes(key)) span.classList.add('is-strong');
  span.textContent = text.length > 280 ? `${text.slice(0, 277)}…` : text;
  return span;
}

function renderPanel(target, data, keys) {
  target.replaceChildren();
  const source = data || {};
  const chosen = keys && keys.length ? keys : Object.keys(source).slice(0, 8);

  chosen.forEach(key => {
    if (!(key in source)) return;
    const row = document.createElement('div');
    row.className = 'data-row';
    const label = document.createElement('span');
    label.className = 'data-key';
    label.textContent = humanKey(key);
    row.append(label, makeValue(source[key], key));
    target.appendChild(row);
  });

  if (!target.children.length) {
    const row = document.createElement('div');
    row.className = 'data-row';
    const label = document.createElement('span');
    label.className = 'data-key';
    label.textContent = 'State';
    const value = document.createElement('span');
    value.className = 'data-value is-gold';
    value.textContent = 'UNKNOWN';
    row.append(label, value);
    target.appendChild(row);
  }
}

function flywheelView(f = {}) {
  return {
    state: f.state,
    stream_count: f.stream_count,
    realized_revenue_status: f.realized_revenue_status,
    realized_revenue_total: f.realized_revenue_total,
    customer_success_gate: Boolean(f.customer_success_gate && f.customer_success_gate.rule),
    diversification_gate: Boolean(f.diversification_gate && f.diversification_gate.rule),
    validation: f.realized_revenue_total_validation
  };
}

function exceptionView(x = {}) {
  const rows = x.exceptions || [];
  return {
    state: x.state,
    source_state: x.source_state,
    high_priority_count: x.count ?? rows.length,
    leading_signals: rows.slice(0, 4).map(e => `${e.type}: ${e.title}`),
    validation: x.validation
  };
}

function pressureView(p = {}) {
  if (!p) return {state: 'UNKNOWN'};
  return {
    organ: p.organ,
    pressure_loss: p.PressureLoss,
    weakest_dimension: p.weakest_dimension,
    blocker: p.blocker,
    owner: p.owner,
    next_action: p.next_action,
    evidence_basis: p.evidence_basis
  };
}

function socView(s = {}) {
  return {
    state: s.state || s.status,
    source_state: s.source_state,
    run_id: s.run_id || s.last_validated_run_id,
    range: s.range || s.authoritative_range,
    validation: s.validation,
    reason: s.reason
  };
}

const missionEl = document.getElementById('mission');
const pressureEl = document.getElementById('pressure');
const socEl = document.getElementById('soc');
const exceptionsEl = document.getElementById('exceptions');
const revenueFlywheelEl = document.getElementById('revenueFlywheel');
const sphereStatus = document.getElementById('sphereStatus');
const exceptionStatus = document.getElementById('exceptionStatus');
const systemState = document.getElementById('systemState');
const systemStateCapsule = document.getElementById('systemStateCapsule');
const localClock = document.getElementById('localClock');
const toast = document.getElementById('toast');
const toastTitle = document.getElementById('toastTitle');
const toastBody = document.getElementById('toastBody');
let toastTimer;

function showToast(title, body) {
  toastTitle.textContent = title;
  toastBody.textContent = body;
  toast.classList.add('is-visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 4200);
}

function setSystemState(state) {
  const resolved = String(state || 'UNKNOWN').toUpperCase();
  systemState.textContent = resolved;
  systemStateCapsule.dataset.state = resolved;
}

function updateClock() {
  const now = new Date();
  localClock.dateTime = now.toISOString();
  localClock.textContent = now.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
}

async function refresh() {
  try {
    const [mission, pressure, soc, sphere, flywheel, exceptions] = await Promise.all([
      '/api/mission',
      '/api/pressure-loss',
      '/api/soc/state',
      '/api/sphere',
      '/api/economics/revenue-flywheel',
      '/api/exceptions/high-priority'
    ].map(get));

    renderPanel(missionEl, mission, ['state','branch','next_action','validation']);
    renderPanel(pressureEl, pressureView(pressure.system_weakest), ['organ','pressure_loss','weakest_dimension','owner','next_action','evidence_basis']);
    renderPanel(socEl, socView(soc), ['state','source_state','run_id','range','validation','reason']);
    renderPanel(exceptionsEl, exceptionView(exceptions), ['state','source_state','high_priority_count','leading_signals','validation']);
    renderPanel(revenueFlywheelEl, flywheelView(flywheel), ['state','stream_count','realized_revenue_status','realized_revenue_total','customer_success_gate','diversification_gate','validation']);

    setSystemState(mission.state || mission.status || 'VERIFY');

    const sphereOK = CCCSphere.draw(document.getElementById('sphere'), sphere);
    sphereStatus.textContent = sphereOK ? 'LIVE MODEL · DATA-BOUND CANVAS FALLBACK' : 'CANVAS UNAVAILABLE';

    const exceptionOK = CCCExceptionConstellation.draw(document.getElementById('exceptionConstellation'), exceptions);
    exceptionStatus.textContent = exceptionOK ? 'VERIFIED SIGNAL FIELD · PRIVATE DATA EXCLUDED' : 'EXCEPTION CANVAS UNAVAILABLE';
  } catch (error) {
    setSystemState('HOLD');
    [missionEl, pressureEl, socEl, exceptionsEl, revenueFlywheelEl].forEach(el => renderPanel(el, {state:'UNKNOWN', reason:'Dashboard data unavailable'}));
    sphereStatus.textContent = 'DATA UNAVAILABLE · NO GREEN STATE INVENTED';
    exceptionStatus.textContent = 'DATA UNAVAILABLE · EXCEPTION FIELD HELD';
    showToast('Telemetry held', error.message);
  }
}

document.querySelectorAll('button[data-mode]').forEach(button => {
  button.addEventListener('click', async () => {
    const mode = button.dataset.mode;
    if (mode !== 'PROCEED') {
      showToast(`Mode: ${mode}`, 'Non-destructive control mode selected. No consequential action executed.');
      return;
    }

    try {
      const response = await fetch('/api/action-request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action_type:'PROCEED_REQUEST', requester:'dashboard-agent', payload:{mode}})
      });
      const result = await response.json();
      showToast('Proceed request recorded', `${result.status || 'PENDING_APPROVAL'} · consequential execution remains human-gated.`);
    } catch (error) {
      showToast('Proceed request failed', error.message);
    }
  });
});

updateClock();
setInterval(updateClock, 1000);
refresh();
setInterval(refresh, 5000);
