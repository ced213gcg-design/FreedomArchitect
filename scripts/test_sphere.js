const fs=require('fs'),vm=require('vm');
const code=fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/sphere.js','utf8');
const sandbox={window:{}}; vm.createContext(sandbox); vm.runInContext(code,sandbox);
let arcs=0,labels=0;
const ctx={clearRect(){},beginPath(){},arc(){arcs++},fill(){},fillText(){labels++},set globalAlpha(v){},set fillStyle(v){},set font(v){}};
const canvas={width:1000,height:520,getContext(kind){return kind==='2d'?ctx:null}};
const ok=sandbox.window.CCCSphere.draw(canvas,{nodes:[{id:'soc',label:'SOC',state:'VERIFY',y:50,importance:100,confidence:65}]});
if(!ok||arcs!==1||labels!==1){console.error('sphere fallback failed');process.exit(1)}
console.log('sphere fallback PASS');
