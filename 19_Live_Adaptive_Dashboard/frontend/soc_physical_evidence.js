(function(global){
  const get=async path=>{const r=await fetch(path,{headers:{Accept:'application/json'}}); if(!r.ok) throw new Error(`${path} -> ${r.status}`); return r.json();};
  const text=v=>v===null||v===undefined||v===''?'UNKNOWN':String(v);
  const age=v=>{if(v===null||v===undefined)return'UNKNOWN';const s=Number(v);if(!Number.isFinite(s))return'UNKNOWN';if(s<60)return`${Math.round(s)}s`;if(s<3600)return`${Math.round(s/60)}m`;return`${(s/3600).toFixed(1)}h`;};
  const stateClass=s=>`state-${text(s).toLowerCase().replace(/[^a-z0-9]+/g,'-')}`;

  function injectStyle(){
    if(document.getElementById('cccPhysicalEvidenceStyle')) return;
    const st=document.createElement('style'); st.id='cccPhysicalEvidenceStyle'; st.textContent=`
      .physical-ops-strip{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:14px 0}
      .physical-kpi{border:1px solid rgba(135,170,200,.22);background:rgba(8,14,23,.78);padding:12px;border-radius:12px;min-width:0}
      .physical-kpi span{display:block;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#8294a8}.physical-kpi strong{display:block;margin-top:6px;font-size:.92rem;overflow-wrap:anywhere}
      .scenario-stage{margin-top:14px}.scenario-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
      .scenario-card{appearance:none;text-align:left;border:1px solid rgba(135,170,200,.22);border-radius:14px;background:linear-gradient(180deg,rgba(12,21,34,.96),rgba(5,10,18,.96));padding:14px;color:inherit;min-height:190px;display:flex;flex-direction:column;gap:9px}
      .scenario-card:focus-visible{outline:3px solid #7bdcff;outline-offset:3px}.scenario-card:hover{border-color:rgba(123,220,255,.55)}
      .scenario-top{display:flex;justify-content:space-between;gap:10px}.scenario-id{font-family:ui-monospace,monospace;font-size:.75rem;color:#83dfff}.scenario-state{font-size:.7rem;font-weight:800;letter-spacing:.08em}
      .scenario-card h3{margin:0;font-size:1rem}.scenario-metrics{display:grid;grid-template-columns:1fr 1fr;gap:7px;font-size:.72rem}.scenario-metrics span{color:#8294a8}.scenario-metrics strong{display:block;color:#e8f1fb;margin-top:2px}
      .scenario-actions{margin-top:auto;display:flex;gap:8px}.scenario-actions button{flex:1;border:1px solid rgba(123,220,255,.35);background:rgba(20,40,58,.7);color:#dff6ff;border-radius:8px;padding:8px;font-weight:700}
      .scenario-actions button:focus-visible{outline:3px solid #7bdcff;outline-offset:2px}
      .scenario-trace{margin-top:12px;border-top:1px solid rgba(135,170,200,.18);padding-top:10px;font-family:ui-monospace,monospace;font-size:.72rem;color:#9cb0c3;white-space:pre-wrap}
      .state-pass{color:#55e6a5}.state-partial,.state-verify-clock-skew{color:#f5c76e}.state-hold,.state-hold-missing-sensor,.state-hold-missing-monitored-path,.state-fail{color:#ff7d76}.state-unknown{color:#8da2b6}
      @media(max-width:1050px){.scenario-grid,.physical-ops-strip{grid-template-columns:repeat(2,minmax(0,1fr))}}
      @media(max-width:640px){.scenario-grid,.physical-ops-strip{grid-template-columns:1fr}}
      @media(prefers-reduced-motion:reduce){.scenario-card{transition:none!important}}
    `; document.head.appendChild(st);
  }

  function ensureStage(){
    injectStyle();
    const theater=document.getElementById('socMissionTheater'); if(!theater) return null;
    const title=document.getElementById('socMissionTitle'); if(title) title.textContent='SOC Control Gates';
    const kicker=theater.querySelector('.panel-kicker'); if(kicker) kicker.textContent='SOC Control Gates / Infrastructure Truth';
    const intro=theater.querySelector('.stage-title-row p:last-child'); if(intro) intro.textContent='Control Gates prove the SOC pipeline can carry trustworthy evidence. They do not substitute for real detection scenarios.';
    if(document.getElementById('socDetectionStage')) return document.getElementById('socDetectionStage');
    const section=document.createElement('section'); section.id='socDetectionStage'; section.className='soc-mission-theater scenario-stage'; section.tabIndex=-1; section.setAttribute('aria-labelledby','socDetectionTitle');
    section.innerHTML=`<div class="mission-stage-shell"><div class="stage-title-row"><div><p class="panel-kicker">Operational Detection / Real Source Telemetry</p><h2 id="socDetectionTitle">SOC Detection Scenarios</h2><p>Five bounded behaviors prove whether registered sensors can feel something real. No real source evidence means no PASS.</p></div><span class="truth-chip">Authorized CCC lab only</span></div><div class="physical-ops-strip" id="physicalOpsStrip"></div><div class="scenario-grid" id="socDetectionCards" aria-live="polite"></div><div class="scenario-trace" id="socDetectionTrace">No real scenario trace yet.</div></div>`;
    theater.insertAdjacentElement('afterend',section); return section;
  }

  function kpi(label,value,cls=''){return `<div class="physical-kpi"><span>${label}</span><strong class="${cls}">${text(value)}</strong></div>`;}

  function card(s){
    const el=document.createElement('article'); el.className='scenario-card'; el.tabIndex=0; el.dataset.scenarioId=s.id;
    el.innerHTML=`<div class="scenario-top"><span class="scenario-id">${text(s.id)}</span><span class="scenario-state ${stateClass(s.state)}">${text(s.state)}</span></div><h3>${text(s.name)}</h3><div class="scenario-metrics"><div><span>Runs</span><strong>${text(s.runs_real)} / ${text(s.runs_required)}</strong></div><div><span>Sensor</span><strong>${text(s.sensor)}</strong></div><div><span>Detection age</span><strong>${age(s.last_detection_age_seconds)}</strong></div><div><span>Latency</span><strong>${s.latency_ms==null?'UNKNOWN':`${s.latency_ms} ms`}</strong></div><div><span>Evidence</span><strong>${text(s.evidence_count)}</strong></div><div><span>Next</span><strong>${text(s.next_action)}</strong></div></div><div class="scenario-actions"><button type="button" data-view>TRACE</button><button type="button" data-request>REQUEST RUN</button></div>`;
    const open=()=>global.CCCContextLens&&global.CCCContextLens.open({...s,plain_function:`Bounded ${s.trigger_class} detection scenario`,fact:`${s.runs_real}/${s.runs_required} real evidence-backed runs`,risk:s.state==='UNKNOWN'?'No real source evidence has been reconciled.':'Review sensor/evidence lineage.',owner:'soc',source:'sanitized physical evidence bridge',approval_requirement:'Human/operator action inside registered guest'});
    el.addEventListener('keydown',e=>{if(e.key==='Enter')open();});
    el.querySelector('[data-view]').addEventListener('click',e=>{e.stopPropagation();open();});
    el.querySelector('[data-request]').addEventListener('click',e=>{e.stopPropagation(); if(global.CCCContextLens) global.CCCContextLens.previewAction({action_type:'REQUEST_SOC_TEST',source_context:'SOC_DETECTION_SCENARIOS',target_object:s.id,requested_effect:`Prepare one bounded ${s.name} run inside the registered guest. No remote execution.`,risk:'Execution remains guest-local and evidence-gated.',run_id:(s.run_records&&s.run_records[0]&&s.run_records[0].run_id)||null,evidence_ref:null});});
    return el;
  }

  function renderTrace(payload){
    const target=document.getElementById('socDetectionTrace'); if(!target)return;
    const rows=(payload&&payload.events)||[]; if(!rows.length){target.textContent='No real scenario trace yet. Trigger → Source → Target → Sensor → Detection → Ledger → Dashboard remains unproven.';return;}
    target.textContent=rows.slice(0,15).map(r=>`${text(r.scenario_id)} / ${text(r.run_id)}\nTRIGGER ${text(r.trigger)} → SOURCE ${text(r.source)} → TARGET ${text(r.target)} → SENSOR ${text(r.sensor)} → DETECTION ${text(r.detection)} → LEDGER ${text(r.ledger)} → DASHBOARD ${text(r.dashboard)}\nSTATE ${text(r.state)} · LATENCY ${r.latency_ms==null?'UNKNOWN':r.latency_ms+' ms'}`).join('\n\n');
  }

  async function refresh(){
    ensureStage();
    try{
      const [summary,trace,bridge,sensors]=await Promise.all(['/api/soc/scenarios','/api/soc/scenario-trace','/api/soc/bridge','/api/sensors'].map(get));
      const strip=document.getElementById('physicalOpsStrip');
      const latency=(summary.scenarios||[]).map(s=>s.latency_ms).filter(v=>typeof v==='number');
      const avg=latency.length?`${(latency.reduce((a,b)=>a+b,0)/latency.length).toFixed(1)} ms`:'UNKNOWN';
      strip.innerHTML=kpi('Live Bridge State',bridge.mode,stateClass(bridge.state))+kpi('Sensor Inventory',`${sensors.state} · ${sensors.count}`)+kpi('Current Run',bridge.current_run)+kpi('Last Real Event',bridge.last_real_event)+kpi('End-to-End Latency',avg);
      const cards=document.getElementById('socDetectionCards'); cards.replaceChildren(...(summary.scenarios||[]).map(card));
      renderTrace(trace);
      const exec=document.getElementById('execTests'); if(exec) exec.textContent=`${summary.real_scenario_count} / 5 real scenarios`;
    }catch(err){
      const cards=document.getElementById('socDetectionCards'); if(cards) cards.innerHTML='<div class="physical-kpi"><span>Detection Scenarios</span><strong class="state-unknown">UNKNOWN · physical evidence unavailable</strong></div>';
    }
  }

  document.addEventListener('DOMContentLoaded',()=>{ensureStage();refresh();setInterval(refresh,5000);});
})(window);
