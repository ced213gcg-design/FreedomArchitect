const fs=require('fs'),vm=require('vm');
vm.runInThisContext(fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/exception_constellation.js','utf8'));
let text=[],arcs=0;
const gradient=()=>({addColorStop(){}});
const ctx={
  clearRect(){},fillRect(){},beginPath(){},arc(){arcs++},fill(){},stroke(){},moveTo(){},lineTo(){},createLinearGradient:gradient,createRadialGradient:gradient,
  fillText(t){text.push(String(t))},set font(v){},set fillStyle(v){},set strokeStyle(v){},set lineWidth(v){},set textAlign(v){},set globalAlpha(v){}
};
const canvas={width:1200,height:360,getContext(){return ctx}};
const ok=CCCExceptionConstellation.draw(canvas,{exceptions:[{exception_id:'fixture',type:'EMPLOYMENT',title:'Fixture Role',freshness_state:'VERIFIED',exception_score:{score:88}}]});
if(!ok||arcs<45||!text.some(x=>x.includes('Fixture Role'))||!text.some(x=>x.includes('88/100'))){console.error('exception Vanguard constellation failed');process.exit(1)}
console.log('exception Vanguard constellation PASS');
