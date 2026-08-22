const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const js=fs.readFileSync(path.join(root,'19_Live_Adaptive_Dashboard/frontend/soc_physical_evidence.js'),'utf8');
const required=['SOC Control Gates','SOC Detection Scenarios','Live Bridge State','Sensor Inventory','Current Run','Last Real Event','End-to-End Latency','REQUEST_SOC_TEST','Authorized CCC lab only','No real scenario trace yet'];
for(const token of required){if(!js.includes(token)){throw new Error(`missing physical UI contract token: ${token}`)}}
if(/eval\s*\(|new Function\s*\(/.test(js)) throw new Error('dynamic code execution prohibited');
console.log('SOC physical evidence UI contract PASS');
