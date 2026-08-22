(function(global){
  function stateClass(state){
    const s=String(state||'UNKNOWN').toUpperCase();
    if(['PASS','READY','VERIFIED'].includes(s)) return 'state-ready';
    if(['HOLD','FAIL','STALE','ISOLATE','CRITICAL'].includes(s)) return 'state-hold';
    if(['VERIFY','PENDING'].includes(s)) return 'state-verify';
    if(['BUILD','INCUBATE','SEED'].includes(s)) return 'state-build';
    return 'state-unknown';
  }

  function button(label,klass='secondary'){
    const b=document.createElement('button'); b.type='button'; b.className=`object-action ${klass}`; b.textContent=label; return b;
  }

  function card(object,{kind='OBJECT',requestable=false}={}){
    const article=document.createElement('article');
    article.className=`ccc-object-card ${stateClass(object.state)}`;
    article.tabIndex=0;
    article.dataset.cccObject=object.id || object.name || kind;
    const head=document.createElement('div'); head.className='object-card-head';
    const kicker=document.createElement('span'); kicker.className='object-type'; kicker.textContent=kind;
    const state=document.createElement('span'); state.className='object-state'; state.textContent=String(object.state||'UNKNOWN').toUpperCase();
    head.append(kicker,state);
    const title=document.createElement('h3'); title.textContent=object.name || object.id || 'CCC Object';
    const purpose=document.createElement('p'); purpose.className='object-purpose'; purpose.textContent=object.objective || object.role || object.plain_function || 'No verified plain-function description available.';
    const meta=document.createElement('div'); meta.className='object-meta';
    meta.innerHTML=`<span><b>Run</b>${object.run_id || '—'}</span><span><b>Evidence</b>${object.evidence_ref || 'UNBOUND'}</span><span><b>Validation</b>${object.validation || 'UNKNOWN'}</span>`;
    const actions=document.createElement('div'); actions.className='object-actions';
    const inspect=button('INSPECT','primary'); inspect.addEventListener('click',e=>{e.stopPropagation(); global.CCCContextLens.open(object);});
    actions.appendChild(inspect);
    if(requestable){
      const request=button('REQUEST RUN');
      request.addEventListener('click',e=>{
        e.stopPropagation();
        global.CCCContextLens.previewAction({
          action_type:'REQUEST_SOC_TEST',
          source_context:'SOC',
          target_object:object.id,
          requested_effect:`Request authorized execution of ${object.name}.`,
          risk:'Execution must remain on the registered CCC lab path and requires authority validation.',
          run_id:object.run_id,
          evidence_ref:object.evidence_ref
        });
      });
      actions.appendChild(request);
    }
    article.append(head,title,purpose,meta,actions);
    article.addEventListener('click',()=>global.CCCContextLens.open(object));
    article.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();global.CCCContextLens.open(object);}});
    return article;
  }

  function renderMissions(container,payload){
    container.replaceChildren();
    (payload.missions||[]).forEach(row=>container.appendChild(card(row,{kind:'SOC MISSION',requestable:true})));
    if(!container.children.length){
      container.appendChild(card({name:'SOC missions unavailable',state:'UNKNOWN',validation:'NO_MISSION_DATA',next_action:'VERIFY_SOC_MISSION_ADAPTER'},{kind:'SOC MISSION'}));
    }
  }

  function renderVMs(container,payload){
    container.replaceChildren();
    (payload.vms||[]).forEach(row=>container.appendChild(card({...row,objective:row.role,evidence_ref:row.validation},{kind:'VM PORTAL'})));
    if(!container.children.length){
      container.appendChild(card({name:'Dell VM state',state:'UNKNOWN',role:'Read-only VM portal awaiting verified Dell vm_health evidence.',validation:payload.validation||payload.source_state||payload.reason,next_action:payload.next_action},{kind:'VM PORTAL'}));
    }
  }

  global.CCCObjectCards={card,renderMissions,renderVMs};
})(window);
