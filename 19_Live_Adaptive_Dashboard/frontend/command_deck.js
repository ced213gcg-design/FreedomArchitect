(function(global){
  const deck=()=>document.getElementById('commandDeck');
  const toggle=()=>document.getElementById('commandDeckToggle');
  let lastFocus=null;

  function open(){
    lastFocus=document.activeElement;
    deck().hidden=false; deck().setAttribute('aria-hidden','false'); document.body.classList.add('deck-open');
    const first=deck().querySelector('button,[href],[tabindex]:not([tabindex="-1"])'); if(first) first.focus();
    if(global.CCCInteraction) global.CCCInteraction.emit('OPEN_COMMAND_DECK',{target_object:'command-deck'});
  }
  function close(){
    deck().hidden=true; deck().setAttribute('aria-hidden','true'); document.body.classList.remove('deck-open');
    if(lastFocus && lastFocus.focus) lastFocus.focus();
    if(global.CCCInteraction) global.CCCInteraction.emit('CLOSE_COMMAND_DECK',{target_object:'command-deck'});
  }
  function flip(){ deck().hidden ? open() : close(); }

  document.addEventListener('click',event=>{
    if(event.target.closest('#commandDeckToggle')) flip();
    if(event.target.closest('[data-close-deck]')) close();
    const action=event.target.closest('[data-deck-target]');
    if(action){
      const id=action.dataset.deckTarget;
      close();
      if(id==='home' && global.CCCHorizon) return global.CCCHorizon.home();
      const target=document.getElementById(id); if(target){target.scrollIntoView({behavior:'smooth',block:'start'}); target.focus?.({preventScroll:true});}
    }
  });

  document.addEventListener('keydown',event=>{
    const tag=(event.target && event.target.tagName || '').toLowerCase();
    const typing=['input','textarea','select'].includes(tag) || (event.target && event.target.isContentEditable);
    if(!typing && event.key.toLowerCase()==='d'){event.preventDefault();flip();}
    if(event.key==='Escape' && deck() && !deck().hidden){event.preventDefault();close();}
  });

  global.CCCCommandDeck={open,close,toggle:flip};
})(window);
