(() => {
  'use strict';

  const q = (s, r=document) => r.querySelector(s);
  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const get = async (path) => {
    const r = await fetch(path, {headers:{'Accept':'application/json'}});
    if (!r.ok) throw new Error(`${path}:${r.status}`);
    return r.json();
  };

  function mount() {
    if (q('#infinityComposition')) return q('#infinityComposition');
    const anchor = q('#executiveMode') || q('main');
    const section = document.createElement('section');
    section.id='infinityComposition';
    section.className='infinity-composition';
    section.setAttribute('aria-labelledby','infinityTitle');
    section.innerHTML=`
      <div class="infinity-overture">
        <div>
          <p class="panel-kicker">Infinity Composition / Constitutional Overture</p>
          <h2 id="infinityTitle">Where are we? What matters? What is proven?</h2>
          <p class="infinity-thesis">Doctrine appears when the decision needs it. Evidence establishes truth; symbolism shapes meaning and cadence.</p>
        </div>
        <span class="infinity-cadence" title="Symbolic cadence only. Operational telemetry uses evidence-grounded timing.">0011 · 0110 · 1001 · 963</span>
      </div>
      <div class="infinity-arrival" id="infinityArrival" aria-live="polite">
        <div><span>WHERE</span><strong>Loading…</strong></div>
        <div><span>PROVEN</span><strong>Loading…</strong></div>
        <div><span>WEAKEST</span><strong>Loading…</strong></div>
        <div><span>HUMAN ACTION</span><strong>Loading…</strong></div>
      </div>
      <div class="infinity-flow" id="infinityFlow" aria-label="Infinity lifecycle"></div>
      <div class="infinity-context" id="infinityContext" aria-live="polite">
        <p class="infinity-context-hint">Select a meaningful CCC world or object. Infinity will reveal only the doctrine relevant to that context.</p>
      </div>
      <details class="infinity-constitution">
        <summary>Constitutional reference</summary>
        <div id="infinityConstitution"></div>
      </details>`;
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(section, anchor.nextSibling);
    return section;
  }

  function stateClass(state) {
    const s=String(state||'UNKNOWN').toUpperCase();
    if (['PASS','READY','VERIFIED'].includes(s)) return 'state-earned';
    if (['HOLD','FAIL','STALE','ISOLATE'].includes(s)) return 'state-risk';
    if (['BUILD','VERIFY','PARTIAL'].includes(s)) return 'state-attention';
    return 'state-unknown';
  }

  function renderFlow(lifecycle) {
    const flow=q('#infinityFlow');
    if (!flow) return;
    const seq=lifecycle.infinity||[];
    flow.innerHTML=seq.map((x,i)=>`<div class="infinity-stage ${x==='GAMMA'?'gamma-stage':''}"><span>${String(i+1).padStart(2,'0')}</span><strong>${esc(x)}</strong>${x==='GAMMA'?'<small>reconcile micro ↔ macro</small>':''}</div>`).join('<i aria-hidden="true">→</i>');
  }

  function renderConstitution(s) {
    const el=q('#infinityConstitution');
    if (!el) return;
    const align=(s.creator_alignment||[]).map(x=>`<span>${esc(x)}</span>`).join('');
    const triad=(s.decision_triad||[]).join(' · ');
    const sextet=(s.evidence_sextet||[]).join(' · ');
    const nonet=(s.completion_nonet||[]).map((x,i)=>`${i+1}. ${x}`).join(' · ');
    el.innerHTML=`
      <div class="constitution-row"><strong>Creator Alignment</strong><div class="value-cloud">${align}</div></div>
      <div class="constitution-row"><strong>3</strong><p>${esc(triad)}</p></div>
      <div class="constitution-row"><strong>6</strong><p>${esc(sextet)}</p></div>
      <div class="constitution-row"><strong>9</strong><p>${esc(nonet)}</p></div>
      <div class="constitution-row"><strong>Cadence boundary</strong><p>${esc((s.symbolic_cadence||{}).operator_notice||'Symbolic cadence only.')}</p></div>`;
  }

  function workerChorus(workers, object='selected object') {
    return `<div class="worker-chorus">
      <div class="context-head"><span>Five-worker chorus</span><strong>${esc(object)}</strong></div>
      ${(workers.workers||[]).map(w=>`<article><span>${esc(w.id)}</span><p>${esc(w.question)}</p><small>${esc(w.authority)}</small></article>`).join('')}
      <p class="context-law">Consensus does not create truth. Ledger evidence and hard controls remain authoritative.</p>
    </div>`;
  }

  function contextual(world, data) {
    const el=q('#infinityContext'); if(!el) return;
    const w=String(world||'').toUpperCase();
    const gamma=data.lifecycle.gamma||{};
    const common=`<div class="context-head"><span>Context Lens · Infinity</span><strong>${esc(w||'CCC')}</strong></div>
      <div class="context-triad"><div><span>FACT</span><strong>Context selected</strong></div><div><span>RISK</span><strong>Do not infer beyond evidence</strong></div><div><span>ACTION</span><strong>Inspect the relevant gate</strong></div></div>`;
    if (w.includes('WORKFORCE')) {
      el.innerHTML=common+workerChorus(data.workers,w);
    } else if (w.includes('REVENUE') || w.includes('LEDGER')) {
      el.innerHTML=common+`<div class="context-panel"><h3>MIT Mechanism Gate</h3><p>Fourteen independent dimensions apply only when a real economic, settlement, multi-party-state, token, blockchain, or irreversible automation question exists.</p><p class="context-law">Default: simplest architecture satisfying verified requirements. Blockchain is not visual branding.</p></div>`;
    } else if (w.includes('INTELLIGENCE')) {
      el.innerHTML=common+`<div class="context-panel"><h3>CRAYOLA</h3><p>${(data.crayola.stages||[]).map(x=>esc(x)).join(' → ')}</p><p class="context-law">Unvalidated research remains ADVISORY. Every cycle terminates in evidence, capability, memory, seed, or documented rejection.</p></div>`;
    } else if (w.includes('MISSION') || w.includes('SOC')) {
      el.innerHTML=common+`<div class="context-panel"><h3>Gamma reconciliation</h3><p>${esc(gamma.purpose||'Field integration before Omega.')}</p><p>Outcome options: ${(gamma.outcomes||[]).map(esc).join(' · ')}</p><p class="context-law">Local PASS does not become complete PASS if the wider organism is harmed or contradictory.</p></div>`;
    } else {
      el.innerHTML=common+`<div class="context-panel"><h3>Lifecycle</h3><p>ALPHA → BETA → GAMMA → OMEGA → REINJECTION → NEXT ALPHA</p><p class="context-law">A capability that cannot be proved, repeated, measured and safely reinjected has not earned Omega.</p></div>`;
    }
  }

  async function load() {
    mount();
    try {
      const [s,l,w,c,r,p,soc] = await Promise.all([
        get('/api/infinity/state'), get('/api/infinity/lifecycle'), get('/api/workers/constitutional'),
        get('/api/crayola/current'), get('/api/infinity/reinjection'), get('/api/pressure-loss'), get('/api/soc/state')
      ]);
      const weakest=p.system_weakest||{};
      const arrival=q('#infinityArrival');
      if(arrival) arrival.innerHTML=`
        <div><span>WHERE</span><strong>Infinity · ${esc(s.state)}</strong></div>
        <div><span>PROVEN</span><strong class="${stateClass(soc.state)}">SOC ${esc(soc.state||'UNKNOWN')}</strong></div>
        <div><span>WEAKEST</span><strong>${esc(weakest.organ||weakest.weakest_dimension||'UNKNOWN')}</strong></div>
        <div><span>HUMAN ACTION</span><strong>${(s.physical_candidate||{}).runtime_state==='VERIFY'?'Physical evidence still required':'Review current gate'}</strong></div>`;
      renderFlow(l); renderConstitution(s);
      const data={state:s,lifecycle:l,workers:w,crayola:c,reinjection:r};
      document.querySelectorAll('.world-tile').forEach(btn=>btn.addEventListener('click',()=>contextual(btn.dataset.world,data)));
      contextual('CCC_HORIZON',data);
      const hb=q('#heartbeat'); if(hb) hb.title=(s.symbolic_cadence||{}).operator_notice||hb.title;
    } catch(err) {
      const a=q('#infinityArrival'); if(a) a.innerHTML=`<div><span>STATE</span><strong class="state-risk">HOLD</strong></div><div><span>ERROR</span><strong>${esc(err.message)}</strong></div>`;
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',load,{once:true}); else load();
})();
