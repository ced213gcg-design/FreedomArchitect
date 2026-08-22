(function(global){
  const palette={
    DORMANT:'#667483',SEED:'#8ea1b2',INCUBATE:'#b8a1ff',BUILD:'#62d7ff',VERIFY:'#f3c86a',READY:'#71e6b5',THRIVE:'#8ff0c8',SCALE:'#f7e3a0',HOLD:'#ff9f72',ISOLATE:'#ff7b88',RETIRE:'#65707b'
  };

  function colorFor(state){return palette[String(state||'').toUpperCase()]||'#93a4b5';}
  function clamp(v,min,max){return Math.max(min,Math.min(max,v));}
  function hash(text){let h=2166136261;for(const c of String(text||'')){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;}

  function draw(canvas,payload){
    if(!canvas||!canvas.getContext)return false;
    const ctx=canvas.getContext('2d');
    if(!ctx)return false;

    const width=canvas.width,height=canvas.height,cx=width/2,cy=height/2;
    const nodes=(payload&&payload.nodes)||[],edges=(payload&&payload.edges)||[];
    const pos={};
    ctx.clearRect(0,0,width,height);

    const bg=ctx.createRadialGradient(cx,cy,20,cx,cy,Math.max(width,height)*.58);
    bg.addColorStop(0,'rgba(98,215,255,.065)');
    bg.addColorStop(.34,'rgba(24,48,68,.035)');
    bg.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=bg;ctx.fillRect(0,0,width,height);

    ctx.save();
    ctx.translate(cx,cy);
    [82,142,214,296].forEach((r,i)=>{
      ctx.beginPath();
      ctx.ellipse(0,0,r,r*.47,0,0,Math.PI*2);
      ctx.strokeStyle=i===1?'rgba(98,215,255,.16)':'rgba(201,215,226,.085)';
      ctx.lineWidth=i===1?1.35:1;
      ctx.setLineDash(i%2?[3,7]:[]);
      ctx.stroke();
    });
    ctx.setLineDash([]);
    ctx.restore();

    const cross='rgba(201,215,226,.075)';
    ctx.strokeStyle=cross;ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(38,cy);ctx.lineTo(width-38,cy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx,34);ctx.lineTo(cx,height-34);ctx.stroke();

    nodes.forEach((n,i)=>{
      const seed=hash(n.id||i);
      const angle=(i/Math.max(1,nodes.length))*Math.PI*2+((seed%37)/37)*.24;
      const capability=Number(n.x||0), productive=Number(n.y||0), confidence=Number(n.s||n.confidence||0);
      const ring=118+(i%4)*58+clamp(productive,0,100)*.58;
      const x=cx+Math.cos(angle)*ring;
      const y=cy+Math.sin(angle)*ring*.46-(capability*.14)+(confidence-50)*.08;
      pos[n.id]={x,y};
    });

    edges.forEach((e)=>{
      const a=pos[e.source],b=pos[e.target];if(!a||!b)return;
      const mx=(a.x+b.x)/2,my=(a.y+b.y)/2-26;
      ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.quadraticCurveTo(mx,my,b.x,b.y);
      ctx.strokeStyle='rgba(98,215,255,.12)';
      ctx.lineWidth=clamp(1+Number(e.volume||0)/42,1,4);
      ctx.stroke();
    });

    const coreGlow=ctx.createRadialGradient(cx,cy,4,cx,cy,62);
    coreGlow.addColorStop(0,'rgba(243,200,106,.95)');
    coreGlow.addColorStop(.12,'rgba(98,215,255,.6)');
    coreGlow.addColorStop(.42,'rgba(98,215,255,.13)');
    coreGlow.addColorStop(1,'rgba(98,215,255,0)');
    ctx.fillStyle=coreGlow;ctx.beginPath();ctx.arc(cx,cy,62,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='rgba(243,200,106,.36)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(cx,cy,31,0,Math.PI*2);ctx.stroke();
    ctx.fillStyle='#edf5fb';ctx.textAlign='center';ctx.font='600 17px system-ui, sans-serif';ctx.fillText('CCC',cx,cy-1);
    ctx.fillStyle='rgba(201,215,226,.58)';ctx.font='9px ui-monospace, monospace';ctx.fillText('FACT · EVIDENCE · EXECUTION',cx,cy+16);

    nodes.forEach((n)=>{
      const p=pos[n.id];if(!p)return;
      const importance=clamp(Number(n.w||n.importance||45),0,100);
      const confidence=clamp(Number(n.s||n.confidence||35),0,100);
      const activity=clamp(Number(n.activity||0),0,100);
      const radius=5.5+importance*.075;
      const color=colorFor(n.state);

      const glow=ctx.createRadialGradient(p.x,p.y,1,p.x,p.y,radius*2.8);
      glow.addColorStop(0,color);
      glow.addColorStop(.24,color+'cc');
      glow.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=glow;ctx.beginPath();ctx.arc(p.x,p.y,radius*2.8,0,Math.PI*2);ctx.fill();

      ctx.globalAlpha=.45+.5*(confidence/100);
      ctx.fillStyle=color;ctx.beginPath();ctx.arc(p.x,p.y,radius+activity*.02,0,Math.PI*2);ctx.fill();
      ctx.globalAlpha=1;
      ctx.strokeStyle='rgba(237,245,251,.38)';ctx.lineWidth=.8;ctx.beginPath();ctx.arc(p.x,p.y,radius+2.2,0,Math.PI*2);ctx.stroke();

      const label=String(n.label||n.id||'ORGAN');
      const left=p.x>cx;
      ctx.textAlign=left?'left':'right';
      ctx.fillStyle='rgba(237,245,251,.92)';ctx.font='600 11px system-ui, sans-serif';
      ctx.fillText(label,p.x+(left?radius+9:-(radius+9)),p.y-1);
      ctx.fillStyle='rgba(132,151,168,.8)';ctx.font='9px ui-monospace, monospace';
      ctx.fillText(`${String(n.state||'UNKNOWN').toUpperCase()} · ${Math.round(confidence)}% EVIDENCE`,p.x+(left?radius+9:-(radius+9)),p.y+12);
    });

    ctx.textAlign='left';ctx.fillStyle='rgba(132,151,168,.62)';ctx.font='9px ui-monospace, monospace';
    ctx.fillText('X CAPABILITY',22,height-18);
    ctx.fillText('Y PRODUCTIVE VALUE',118,height-18);
    ctx.fillText('W AUTHORIZATION',270,height-18);
    ctx.fillText('S VERIFIED STATE',390,height-18);
    return true;
  }

  global.CCCSphere={draw};
})(typeof window!=='undefined'?window:globalThis);
