const fs=require('fs');
const html=fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/index.html','utf8');
const css=fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/styles.css','utf8');
const app=fs.readFileSync('19_Live_Adaptive_Dashboard/frontend/app.js','utf8');

const requiredIds=['mission','pressure','soc','exceptions','revenueFlywheel','sphere','exceptionConstellation','sphereStatus','exceptionStatus','systemState','localClock','toast'];
for(const id of requiredIds){if(!html.includes(`id="${id}"`)){console.error(`missing required UI id: ${id}`);process.exit(1)}}

const requiredModes=['COACH','PLAN','SIMULATE','DIVE','PROCEED','PAUSE','HALT'];
for(const mode of requiredModes){if(!html.includes(`data-mode="${mode}"`)){console.error(`missing control mode: ${mode}`);process.exit(1)}}

if(!html.includes('V10.1 // VANGUARD')){console.error('Vanguard identity missing');process.exit(1)}
if(!html.includes('Human authority required for consequential action')){console.error('human authority boundary missing');process.exit(1)}
if(!css.includes('@media (prefers-reduced-motion: reduce)')){console.error('reduced-motion accessibility rule missing');process.exit(1)}
if(!css.includes('--ion:')||!css.includes('--gold:')||!css.includes('--danger:')){console.error('semantic visual tokens missing');process.exit(1)}
if(!app.includes('DATA UNAVAILABLE · NO GREEN STATE INVENTED')){console.error('honest telemetry failure state missing');process.exit(1)}
if(/https?:\/\//.test(html)){console.error('unexpected external frontend dependency');process.exit(1)}

console.log('CCC Vanguard UI contract PASS');
