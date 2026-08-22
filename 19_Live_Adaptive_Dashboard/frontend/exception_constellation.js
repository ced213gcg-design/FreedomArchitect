(function(global){
  function scoreOf(e){return Number((e.exception_score||{}).score||0);}
  function draw(canvas,payload){
    if(!canvas||!canvas.getContext)return false; const ctx=canvas.getContext('2d'); if(!ctx)return false; const rows=(payload&&payload.exceptions)||[]; ctx.clearRect(0,0,canvas.width,canvas.height); ctx.font='14px sans-serif';
    if(!rows.length){ctx.fillText('No verified high-priority exceptions.',18,30);return true;}
    rows.forEach((e,i)=>{const score=scoreOf(e),x=45+(i*137)%(canvas.width-90),y=55+((i*83)%Math.max(80,canvas.height-110)),r=Math.max(4,Math.min(12,score/10)); ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.fillText(`${e.type}: ${e.title} (${score})`,x+r+6,y+4);}); return true;
  }
  global.CCCExceptionConstellation={draw};
})(typeof window!=='undefined'?window:globalThis);
