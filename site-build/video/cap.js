const { chromium } = require('playwright');
(async () => { const a=process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await p.goto('file://'+__dirname+'/film.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(1800);
  if (a[0]==='still') { for (const t of a.slice(1)) { await p.evaluate(v=>setT(v),+t); await p.screenshot({path:__dirname+`/still-${t}.jpg`,type:'jpeg',quality:80}); } await b.close(); return; }
  const D=await p.evaluate(()=>DUR), N=Math.round(D*30); const t0=Date.now();
  for (let f=0;f<N;f++){ await p.evaluate(v=>setT(v),f/30); await p.screenshot({path:__dirname+'/frames/f'+String(f).padStart(5,'0')+'.jpg',type:'jpeg',quality:92}); }
  console.log('frames',N,Math.round((Date.now()-t0)/1000)+'s'); await b.close(); })();
