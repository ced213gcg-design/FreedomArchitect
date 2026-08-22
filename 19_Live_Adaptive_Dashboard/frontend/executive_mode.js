(function(global){
  let enabled=false;
  function setMode(on){
    enabled=Boolean(on);
    document.body.classList.toggle('executive-mode',enabled);
    const button=document.getElementById('executiveModeToggle');
    if(button){button.setAttribute('aria-pressed',String(enabled));button.textContent=enabled?'OPERATOR MODE':'EXECUTIVE MODE';}
    if(global.CCCInteraction) global.CCCInteraction.emit(enabled?'OPEN_EXECUTIVE_MODE':'OPEN_OPERATOR_MODE',{target_object:enabled?'executive-mode':'operator-mode'});
  }
  document.addEventListener('click',event=>{if(event.target.closest('#executiveModeToggle')) setMode(!enabled);});
  global.CCCExecutiveMode={setMode,get enabled(){return enabled;}};
})(window);
