// regrava só um intervalo de quadros do filme: node cap_range.js <quadro inicial> <quadro final>
const { chromium } = require('playwright');
(async () => {
  const f0 = +process.argv[2], f1 = +process.argv[3];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/film.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1800);
  for (let f = f0; f <= f1; f++) {
    await p.evaluate(v => setT(v), f / 30);
    await p.screenshot({ path: __dirname + '/frames/f' + String(f).padStart(5, '0') + '.jpg', type: 'jpeg', quality: 92 });
  }
  console.log('frames', f0, f1);
  await b.close();
})();
