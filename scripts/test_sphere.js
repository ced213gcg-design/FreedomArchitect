const fs=require('fs'),vm=require('vm');
const code=fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/sphere.js','utf8');
const sandbox={window:{}};vm.createContext(sandbox);vm.runInContext(code,sandbox);
let arcs=0,labels=[];
const gradient=()=>({addColorStop(){}});
const ctx={
  clearRect(){},fillRect(){},save(){},restore(){},translate(){},beginPath(){},arc(){arcs++},ellipse(){},moveTo(){},lineTo(){},quadraticCurveTo(){},stroke(){},fill(){},setLineDash(){},
  createRadialGradient:gradient,
  fillText(t){labels.push(String(t))},
  set globalAlpha(v){},set fillStyle(v){},set strokeStyle(v){},set lineWidth(v){},set font(v){},set textAlign(v){}
};
const canvas={width:1200,height:620,getContext(kind){return kind==='2d'?ctx:null}};
const ok=sandbox.window.CCCSphere.draw(canvas,{nodes:[{id:'soc',label:'SOC',state:'VERIFY',x:20,y:50,importance:100,confidence:65}],edges:[]});
if(!ok||arcs<3||!labels.some(x=>x.includes('SOC'))||!labels.some(x=>x.includes('FACT'))){console.error('sphere Vanguard render contract failed');process.exit(1)}
console.log('sphere Vanguard fallback PASS');
