(function(global){
  const WORLD_TARGETS={
    MISSION:'executiveMode', SOC:'socMissionTheater', WORKFORCE:'horizon', INTELLIGENCE:'exceptionStage',
    INFRASTRUCTURE:'vmPortal', 'LEDGER / EVIDENCE':'evidenceDrawer', 'REVENUE / FREEDOM ARCHITECT':'economicStage',
    'FOUNDRY / PRODUCTS':'horizon', 'SETTINGS / TRUST':'authorityFooter'
  };

  function home(){
    document.body.dataset.world='CCC_HORIZON';
    const target=document.getElementById('horizon');
    if(target){target.scrollIntoView({behavior:'smooth',block:'start'}); target.focus?.({preventScroll:true});}
    if(global.CCCInteraction) global.CCCInteraction.emit('RETURN_HOME',{target_object:'CCC_HORIZON'});
  }

  function openWorld(name){
    const targetId=WORLD_TARGETS[name] || 'horizon';
    document.body.dataset.world=name;
    const target=document.getElementById(targetId);
    if(target){target.scrollIntoView({behavior:'smooth',block:'start'});}
    if(global.CCCInteraction) global.CCCInteraction.emit('OPEN_WORLD',{source_context:'CCC_HORIZON',target_object:name});
  }

  document.addEventListener('click',event=>{
    if(event.target.closest('[data-ccc-home]')) home();
    const world=event.target.closest('[data-world]'); if(world) openWorld(world.dataset.world);
  });
  document.addEventListener('keydown',event=>{
    const tag=(event.target && event.target.tagName || '').toLowerCase();
    const typing=['input','textarea','select'].includes(tag) || (event.target && event.target.isContentEditable);
    if(!typing && event.key.toLowerCase()==='h'){event.preventDefault();home();}
  });

  global.CCCHorizon={home,openWorld};
})(window);
