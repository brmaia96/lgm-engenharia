// Grava os quadros do filme. uso: node cap.js <w|m> [still t1 t2 ...] | node cap.js <w|m> [quadro inicial] [quadro final]
// w = 1920x1080 (computador, entra na coluna do site); m = 1080x1350 (celular).
const { chromium } = require('playwright');
(async () => {
  const [fmt, ...a] = process.argv.slice(2);
  const vp = fmt === 'm' ? { width: 1080, height: 1350 } : { width: 1920, height: 1080 };
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/film.html' + (fmt === 'm' ? '?m' : ''));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1500);
  const dir = __dirname + '/frames-' + fmt; require('fs').mkdirSync(dir, { recursive: true });
  if (a[0] === 'still') {
    for (const t of a.slice(1)) { await p.evaluate(v => setT(v), +t); await p.screenshot({ path: `${__dirname}/still-${fmt}-${t}.jpg`, type: 'jpeg', quality: 82 }); }
    await b.close(); return;
  }
  const D = await p.evaluate(() => DUR), N = Math.round(D * 30), f0 = a[0] ? +a[0] : 0, f1 = a[1] ? +a[1] : N - 1, t0 = Date.now();
  for (let f = f0; f <= f1; f++) { await p.evaluate(v => setT(v), f / 30); await p.screenshot({ path: dir + '/f' + String(f).padStart(5, '0') + '.jpg', type: 'jpeg', quality: 92 }); }
  console.log(fmt, 'frames', f0, f1, Math.round((Date.now() - t0) / 1000) + 's'); await b.close();
})();
