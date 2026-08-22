(function(global){
  const panel = () => document.getElementById('contextLens');
  const title = () => document.getElementById('contextLensTitle');
  const body = () => document.getElementById('contextLensBody');
  const raw = () => document.getElementById('contextLensRaw');
  let active = null;

  function text(value){ return value === null || value === undefined || value === '' ? 'UNKNOWN' : String(value); }
  function row(label,value){
    const wrap=document.createElement('div'); wrap.className='lens-row';
    const key=document.createElement('span'); key.className='lens-key'; key.textContent=label;
    const val=document.createElement('span'); val.className='lens-value'; val.textContent=text(value);
    wrap.append(key,val); return wrap;
  }

  function open(data={}){
    active=data;
    title().textContent=data.name || data.title || data.id || 'CCC Object';
    body().replaceChildren(
      row('PLAIN FUNCTION', data.plain_function || data.objective || data.role),
      row('STATE', data.state),
      row('FACT', data.fact || data.result || data.validation),
      row('RISK', data.risk || (data.state==='UNKNOWN' ? 'Evidence incomplete' : 'See evidence')), 
      row('NEXT ACTION', data.next_action),
      row('OWNER', data.owner),
      row('SOURCE', data.source || data.source_state),
      row('TIME', data.last_verified || data.timestamp),
      row('VALIDATION', data.validation),
      row('APPROVAL', data.approval_requirement || (data.authority_required ? 'REQUIRED' : 'NOT REQUIRED FOR VIEW'))
    );
    raw().textContent=JSON.stringify(data,null,2);
    panel().hidden=false;
    panel().setAttribute('aria-hidden','false');
    document.body.classList.add('lens-open');
    const close=panel().querySelector('[data-close-lens]'); if(close) close.focus();
    if(global.CCCInteraction) global.CCCInteraction.emit('OPEN_CONTEXT_LENS',{target_object:data.id || data.name || 'object'});
  }

  function close(){
    panel().hidden=true; panel().setAttribute('aria-hidden','true'); document.body.classList.remove('lens-open');
    if(active && global.CCCInteraction) global.CCCInteraction.emit('CLOSE_CONTEXT_LENS',{target_object:active.id || active.name || 'object'});
    active=null;
  }

  function previewAction(action={}){
    open({
      id: action.target_object,
      name: 'REQUEST PREVIEW',
      plain_function: action.requested_effect,
      state: 'HOLD',
      fact: `Request only: ${action.action_type}`,
      risk: action.risk || 'Consequential execution requires authority validation.',
      next_action: 'Confirm request or cancel. Confirmation does not execute the underlying action.',
      owner: 'human-operator',
      source: action.source_context || 'dashboard',
      validation: 'PREVIEW_NOT_EXECUTION',
      approval_requirement: 'REQUIRED',
      authority_required: true,
      action_preview: action
    });
    const confirm=document.getElementById('contextLensConfirm');
    confirm.hidden=false;
    confirm.onclick=async()=>{
      const result=await global.CCCInteraction.emit(action.action_type,{
        source_context:action.source_context || 'dashboard',
        target_object:action.target_object,
        requested_effect:action.requested_effect,
        authority_required:true,
        run_id:action.run_id,
        evidence_ref:action.evidence_ref
      });
      confirm.hidden=true;
      if(global.CCCUI && global.CCCUI.toast) global.CCCUI.toast('Request recorded', `${result.route || result.reason || 'PENDING'} · no direct execution.`);
    };
  }

  document.addEventListener('click',event=>{
    if(event.target.closest('[data-close-lens]')) close();
  });
  document.addEventListener('keydown',event=>{ if(event.key==='Escape' && panel() && !panel().hidden) close(); });

  global.CCCContextLens={open,close,previewAction};
})(window);
