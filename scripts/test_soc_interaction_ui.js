const fs=require('fs');
const path='19_Live_Adaptive_Dashboard/frontend/';
const html=fs.readFileSync(path+'index.html','utf8');
const app=fs.readFileSync(path+'app.js','utf8');
const css=fs.readFileSync(path+'ccc_multiverse.css','utf8');
const requiredIds=['horizon','commandDeck','contextLens','socMissionTheater','socMissionCards','socTrace','vmPortal','vmPortalCards','evidenceDrawer','evidenceRecent','executiveMode'];
for(const id of requiredIds){if(!html.includes(`id="${id}"`)){console.error(`missing ${id}`);process.exit(1)}}
for(const endpoint of ['/api/soc/missions','/api/soc/trace','/api/vms','/api/evidence/recent']){if(!app.includes(endpoint)){console.error(`missing endpoint ${endpoint}`);process.exit(1)}}
if(!css.includes(':focus-visible')||!css.includes('prefers-reduced-motion:reduce')){console.error('accessibility contract missing');process.exit(1)}
if(/https:\/\/(fonts\.googleapis\.com|cdn\.jsdelivr\.net|unpkg\.com)/i.test(html)){console.error('remote UI dependency detected');process.exit(1)}
console.log('SOC interaction UI smoke PASS');
