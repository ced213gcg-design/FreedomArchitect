(function(global){
  const colors={VERIFIED:'#62d7ff',AGING:'#f3c86a',STALE:'#ff7b88',CLOSED:'#65707b',SUPERSEDED:'#65707b'};
  function scoreOf(e){return Number((e.exception_score||{}).score||0);}
  function hash(text){let h=0;for(const c of String(text||''))h=((h<<5)-h+c.charCodeAt(0))|0;return Math.abs(h);}
  function clamp(v,min,max){return Math.max(min,Math.min(max,v));}

  function draw(canvas,payload){
    if(!canvas||!canvas.getContext)return false;
    const ctx=canvas.getContext('2d');if(!ctx)return false;
    const rows=(payload&&payload.exceptions)||[];
    const width=canvas.width,height=canvas.height;
    ctx.clearRect(0,0,width,height);

    const wash=ctx.createLinearGradient(0,0,width,height);
    wash.addColorStop(0,'rgba(98,215,255,.025)');
    wash.addColorStop(.55,'rgba(184,161,255,.018)');
    wash.addColorStop(1,'rgba(243,200,106,.025)');
    ctx.fillStyle=wash;ctx.fillRect(0,0,width,height);

    for(let i=0;i<44;i++){
      const x=(i*173)%width,y=(i*97+41)%height,alpha=.08+(i%5)*.025;
      ctx.fillStyle=`rgba(201,215,226,${alpha})`;ctx.beginPath();ctx.arc(x,y,(i%3===0)?1.15:.65,0,Math.PI*2);ctx.fill();
    }

    ctx.strokeStyle='rgba(201,215,226,.09)';ctx.lineWidth=1;
    [25,50,70,80,90].forEach(score=>{
      const x=34+(score/100)*(width-68);
      ctx.beginPath();ctx.moveTo(x,26);ctx.lineTo(x,height-34);ctx.stroke();
      ctx.fillStyle='rgba(132,151,168,.48)';ctx.font='9px ui-monospace, monospace';ctx.textAlign='center';ctx.fillText(String(score),x,height-17);
    });

    if(!rows.length){
      ctx.textAlign='left';ctx.fillStyle='rgba(132,151,168,.72)';ctx.font='12px system-ui, sans-serif';
      ctx.fillText('No verified high-priority exceptions. Quiet is a valid signal.',26,42);
      return true;
    }

    rows.forEach((e,i)=>{
      const score=clamp(scoreOf(e),0,100),fresh=String(e.freshness_state||'VERIFIED').toUpperCase();
      const base=colors[fresh]||'#b8a1ff';
      const seed=hash(`${e.exception_id||''}${e.title||''}${i}`);
      const x=34+(score/100)*(width-68);
      const band=height-96;
      const y=48+(seed%Math.max(60,band));
      const radius=5+score*.055;

      if(score>=90){
        ctx.strokeStyle='rgba(243,200,106,.2)';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(Math.max(12,x-62),Math.min(height-26,y+32));ctx.lineTo(x,y);ctx.stroke();
      }

      const glow=ctx.createRadialGradient(x,y,1,x,y,radius*3.1);
      glow.addColorStop(0,base);glow.addColorStop(.24,base+'cc');glow.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=glow;ctx.beginPath();ctx.arc(x,y,radius*3.1,0,Math.PI*2);ctx.fill();
      ctx.fillStyle=base;ctx.globalAlpha=.9;ctx.beginPath();ctx.arc(x,y,radius,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
      ctx.strokeStyle='rgba(237,245,251,.34)';ctx.beginPath();ctx.arc(x,y,radius+2.2,0,Math.PI*2);ctx.stroke();

      const right=x<width*.68;
      ctx.textAlign=right?'left':'right';
      const tx=x+(right?radius+9:-(radius+9));
      ctx.fillStyle='rgba(237,245,251,.92)';ctx.font='600 11px system-ui, sans-serif';
      ctx.fillText(`${e.type||'OTHER'} · ${e.title||'Untitled signal'}`,tx,y-2);
      ctx.fillStyle='rgba(132,151,168,.78)';ctx.font='9px ui-monospace, monospace';
      ctx.fillText(`${Math.round(score)}/100 · ${fresh}`,tx,y+11);
    });

    ctx.textAlign='left';ctx.fillStyle='rgba(132,151,168,.52)';ctx.font='9px ui-monospace, monospace';
    ctx.fillText('EXCEPTION SCORE →',22,height-17);
    return true;
  }

  global.CCCExceptionConstellation={draw};
})(typeof window!=='undefined'?window:globalThis);
