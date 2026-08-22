const get = async (path) => {
  const response = await fetch(path, {headers: {'Accept': 'application/json'}});
  if (!response.ok) throw new Error(`${path} -> HTTP ${response.status}`);
  return response.json();
};

const humanKey = (key) => String(key || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
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
  if (['HOLD','FAIL','STALE','ISOLATE','REJECTED','ERROR','CRITICAL'].some(x => v.includes(x))) return 'is-danger';
  if (['VERIFY','AGING','PENDING'].some(x => v.includes(x))) return 'is-gold';
  if (['BUILD','INCUBATE','SEED'].some(x => v.includes(x))) return 'is-ion';
  return '';
}

function makeValue(value, key='') {
  if (Array.isArray(value)) {
    const wrap = document.createElement('span'); wrap.className = 'badge-list';
    value.slice(0, 8).forEach(item => { const badge=document.createElement('span'); badge.className='data-badge'; badge.textContent=scalar(item); wrap.appendChild(badge); });
    if (value.length > 8) { const more=document.createElement('span'); more.className='data-badge'; more.textContent=`+${value.length - 8} more`; wrap.appendChild(more); }
    return wrap;
  }
  const span=document.createElement('span'); const text=scalar(value); span.className=`data-value ${toneFor(text)}`.trim();
  if (['state','status','organ','title','branch','next_action'].includes(key)) span.classList.add('is-strong');
  span.textContent=text.length>280?`${text.slice(0,277)}…`:text; return span;
}

function renderPanel(target, data, keys) {
  target.replaceChildren(); const source=data||{}; const chosen=keys&&keys.length?keys:Object.keys(source).slice(0,8);
  chosen.forEach(key=>{
    if (!(key in source)) return;
    const row=document.createElement('div'); row.className='data-row'; const label=document.createElement('span'); label.className='data-key'; label.textContent=humanKey(key);
    row.append(label,makeValue(source[key],key)); target.appendChild(row);
  });
  if (!target.children.length) { const row=document.createElement('div'); row.className='data-row'; const label=document.createElement('span'); label.className='data-key'; label.textContent='State'; const value=document.createElement('span'); value.className='data-value'; value.textContent='UNKNOWN'; row.append(label,value); target.appendChild(row); }
}

function flywheelView(f={}) { return {state:f.state,stream_count:f.stream_count,realized_revenue_status:f.realized_revenue_status,realized_revenue_total:f.realized_revenue_total,customer_success_gate:Boolean(f.customer_success_gate&&f.customer_success_gate.rule),diversification_gate:Boolean(f.diversification_gate&&f.diversification_gate.rule),validation:f.realized_revenue_total_validation}; }
function exceptionView(x={}) { const rows=x.exceptions||[]; return {state:x.state,source_state:x.source_state,high_priority_count:x.count??rows.length,leading_signals:rows.slice(0,4).map(e=>`${e.type}: ${e.title}`),validation:x.validation}; }
function pressureView(p={}) { if(!p)return{state:'UNKNOWN'}; return {organ:p.organ,pressure_loss:p.PressureLoss,weakest_dimension:p.weakest_dimension,blocker:p.blocker,owner:p.owner,next_action:p.next_action,evidence_basis:p.evidence_basis}; }
function socView(s={}) { return {state:s.state||s.status,connected:s.connected,stale:s.stale,run_id:s.run_id||s.last_validated_run_id||s.last_valid_run_id,validation:s.validation,reason:s.reason,next_action:s.next_action}; }

const missionEl=document.getElementById('mission'),pressureEl=document.getElementById('pressure'),socEl=document.getElementById('soc'),exceptionsEl=document.getElementById('exceptions'),revenueFlywheelEl=document.getElementById('revenueFlywheel');
const sphereStatus=document.getElementById('sphereStatus'),exceptionStatus=document.getElementById('exceptionStatus'),systemState=document.getElementById('systemState'),systemStateCapsule=document.getElementById('systemStateCapsule'),localClock=document.getElementById('localClock');
const toast=document.getElementById('toast'),toastTitle=document.getElementById('toastTitle'),toastBody=document.getElementById('toastBody'); let toastTimer;

function showToast(title,body){toastTitle.textContent=title;toastBody.textContent=body;toast.classList.add('is-visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove('is-visible'),4200);}
window.CCCUI={toast:showToast};
function setSystemState(state){const resolved=String(state||'UNKNOWN').toUpperCase();systemState.textContent=resolved;systemStateCapsule.dataset.state=resolved;}
function updateClock(){const now=new Date();localClock.dateTime=now.toISOString();localClock.textContent=now.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});}

function renderEventRows(container,events=[],empty='No verified events available.'){
  container.replaceChildren();
  if(!events.length){const e=document.createElement('div');e.className='empty-state';e.textContent=empty;container.appendChild(e);return;}
  events.slice(0,20).forEach(event=>{
    const row=document.createElement('div');row.className=container.id==='evidenceRecent'?'evidence-event':'trace-event';
    const time=document.createElement('span');time.textContent=scalar(event.timestamp);
    const source=document.createElement('span');source.textContent=scalar(event.source||event.owner);
    const type=document.createElement('strong');type.textContent=scalar(event.type||event.event_type||event.validation);
    const detail=document.createElement('span');detail.textContent=`${scalar(event.state||event.new_state)} · ${scalar(event.evidence_ref||event.provenance||event.change)}`;
    row.append(time,source,type,detail);container.appendChild(row);
  });
}

function updateExecutive(mission,pressure,soc,missions){
  const weak=pressure.system_weakest||{};
  document.getElementById('execMission').textContent=scalar(mission.state);
  document.getElementById('execMissionNext').textContent=scalar(mission.next_action);
  document.getElementById('execPressure').textContent=weak.PressureLoss===undefined?'UNKNOWN':scalar(weak.PressureLoss);
  document.getElementById('execPressureOrgan').textContent=weak.organ?`${weak.organ} · ${scalar(weak.weakest_dimension)}`:'No verified weakest organ';
  document.getElementById('execSoc').textContent=scalar(soc.state||soc.status);
  document.getElementById('execSocRun').textContent=`Run: ${scalar(soc.last_valid_run_id||soc.run_id)}`;
  document.getElementById('execTests').textContent=`${missions.proven_count||0} / ${missions.count||5} proven`;
  document.getElementById('execAction').textContent=scalar(mission.next_action||soc.next_action||'COLLECT EVIDENCE');
  document.getElementById('execEvidenceConfidence').textContent=`SOC source: ${scalar(missions.source_state||soc.validation)}`;
}

function updateHorizon(mission,soc,missions,vms){
  document.getElementById('worldMissionState').textContent=scalar(mission.state).toUpperCase();
  document.getElementById('worldMissionFreshness').textContent=scalar(mission.validation);
  document.getElementById('worldSocState').textContent=scalar(soc.state||soc.status).toUpperCase();
  document.getElementById('worldSocEvidence').textContent=`${missions.proven_count||0}/${missions.count||5} PROVEN`;
  document.getElementById('worldInfraState').textContent=scalar(vms.state).toUpperCase();
}

async function refresh(){
  try{
    const [mission,pressure,soc,sphere,flywheel,exceptions,missions,trace,vms,evidence]=await Promise.all([
      '/api/mission','/api/pressure-loss','/api/soc/state','/api/sphere','/api/economics/revenue-flywheel','/api/exceptions/high-priority','/api/soc/missions','/api/soc/trace','/api/vms','/api/evidence/recent'
    ].map(get));

    renderPanel(missionEl,mission,['state','branch','next_action','validation']);
    renderPanel(pressureEl,pressureView(pressure.system_weakest),['organ','pressure_loss','weakest_dimension','owner','next_action','evidence_basis']);
    renderPanel(socEl,socView(soc),['state','connected','stale','run_id','validation','reason','next_action']);
    renderPanel(exceptionsEl,exceptionView(exceptions),['state','source_state','high_priority_count','leading_signals','validation']);
    renderPanel(revenueFlywheelEl,flywheelView(flywheel),['state','stream_count','realized_revenue_status','realized_revenue_total','customer_success_gate','diversification_gate','validation']);

    CCCObjectCards.renderMissions(document.getElementById('socMissionCards'),missions);
    CCCObjectCards.renderVMs(document.getElementById('vmPortalCards'),vms);
    renderEventRows(document.getElementById('socTrace'),trace.events,'No bound live SOC mission evidence yet. This is UNKNOWN, not failure and not PASS.');
    renderEventRows(document.getElementById('evidenceRecent'),evidence.events,'Ledger contains no recent evidence at this runtime path.');
    updateExecutive(mission,pressure,soc,missions); updateHorizon(mission,soc,missions,vms);

    setSystemState(mission.state||mission.status||'VERIFY');
    const sphereOK=CCCSphere.draw(document.getElementById('sphere'),sphere); sphereStatus.textContent=sphereOK?'LIVE MODEL · DATA-BOUND CANVAS FALLBACK':'CANVAS UNAVAILABLE';
    const exceptionOK=CCCExceptionConstellation.draw(document.getElementById('exceptionConstellation'),exceptions); exceptionStatus.textContent=exceptionOK?'VERIFIED SIGNAL FIELD · PRIVATE DATA EXCLUDED':'EXCEPTION CANVAS UNAVAILABLE';
  }catch(error){
    setSystemState('HOLD');[missionEl,pressureEl,socEl,exceptionsEl,revenueFlywheelEl].forEach(el=>renderPanel(el,{state:'UNKNOWN',reason:'Dashboard data unavailable'}));
    sphereStatus.textContent='DATA UNAVAILABLE · NO GREEN STATE INVENTED';exceptionStatus.textContent='DATA UNAVAILABLE · EXCEPTION FIELD HELD';showToast('Telemetry held',error.message);
  }
}

document.querySelectorAll('button[data-mode]').forEach(button=>{
  button.addEventListener('click',async()=>{
    const mode=button.dataset.mode;
    if(mode!=='PROCEED'){showToast(`Mode: ${mode}`,'Non-destructive control mode selected. No consequential action executed.');return;}
    try{
      const response=await fetch('/api/action-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action_type:'PROCEED_REQUEST',requester:'dashboard-agent',payload:{mode}})});
      const result=await response.json();showToast('Proceed request recorded',`${result.status||'PENDING_APPROVAL'} · consequential execution remains human-gated.`);
    }catch(error){showToast('Proceed request failed',error.message);}
  });
});

document.addEventListener('keydown',event=>{
  const tag=(event.target&&event.target.tagName||'').toLowerCase();const typing=['input','textarea','select'].includes(tag)||(event.target&&event.target.isContentEditable);
  if(!typing&&event.key.toLowerCase()==='e'){event.preventDefault();document.getElementById('evidenceDrawer').scrollIntoView({behavior:'smooth',block:'start'});CCCInteraction.emit('OPEN_EVIDENCE',{target_object:'evidenceDrawer'});}
});

updateClock();setInterval(updateClock,1000);refresh();setInterval(refresh,5000);
