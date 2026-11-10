const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await p.goto('file://'+__dirname+'/film.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(1500);
  const fonts = await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight+' '+f.style));
  console.log('fonts',JSON.stringify(fonts));
  const only = process.argv[2];
  if (only) { for (const t of only.split(',')) { await p.evaluate(v=>setT(v),+t); await p.screenshot({path:__dirname+`/still-${t}.jpg`,type:'jpeg',quality:88}); } await b.close(); return; }
  const N=46*30; const t0=Date.now();
  for (let f=0;f<N;f++){ await p.evaluate(v=>setT(v),f/30); await p.screenshot({path:__dirname+'/frames/f'+String(f).padStart(5,'0')+'.jpg',type:'jpeg',quality:93}); }
  console.log('frames',N,'in',Math.round((Date.now()-t0)/1000),'s'); await b.close();
})();
