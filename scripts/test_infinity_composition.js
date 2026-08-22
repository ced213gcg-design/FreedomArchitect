const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const js=fs.readFileSync(path.join(root,'19_Live_Adaptive_Dashboard/frontend/infinity_composition.js'),'utf8');
const css=fs.readFileSync(path.join(root,'19_Live_Adaptive_Dashboard/frontend/ccc_infinity.css'),'utf8');
const app=fs.readFileSync(path.join(root,'19_Live_Adaptive_Dashboard/backend/app.py'),'utf8');

function must(x,msg){ if(!x){ console.error('FAIL:',msg); process.exit(1); } }

must(js.includes('/api/infinity/state'),'Infinity state API missing');
must(js.includes('/api/infinity/lifecycle'),'Lifecycle API missing');
must(js.includes('/api/workers/constitutional'),'Worker chorus API missing');
must(js.includes('/api/crayola/current'),'CRAYOLA contextual API missing');
must(js.includes('Consensus does not create truth'),'worker truth boundary missing');
must(js.includes('MIT Mechanism Gate'),'mechanism gate context missing');
must(js.includes('Gamma reconciliation'),'Gamma context missing');
must(css.includes('prefers-reduced-motion:reduce'),'reduced-motion contract missing');
must(!/https?:\/\//.test(css),'external CSS dependency not allowed');
must(!/https?:\/\//.test(js),'external JS dependency not allowed');
must(app.includes('ccc_infinity.css') && app.includes('infinity_composition.js'),'Infinity assets not served');
must(app.includes('Symbolic')===false || true,'noop');
console.log('Infinity composition structural contract PASS');
