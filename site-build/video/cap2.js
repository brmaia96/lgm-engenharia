const { chromium } = require('playwright');
(async () => { const [a,b_]=process.argv.slice(2).map(Number);
  const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await p.goto('file://'+__dirname+'/film.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(1500);
  for (let f=a;f<b_;f++){ await p.evaluate(v=>setT(v),f/30); await p.screenshot({path:__dirname+'/frames/f'+String(f).padStart(5,'0')+'.jpg',type:'jpeg',quality:93}); }
  console.log('recaptured',a,b_); await b.close(); })();
