// teste funcional da calculadora e do formulário de contato: node test_inss.js <dir>
const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.route(/wa\.me|whatsapp/, r => r.fulfill({ status: 200, contentType: 'text/html', body: 'ok' }));
  await p.goto('file://' + dir + '/inss.html');
  await p.waitForTimeout(400);
  const read = () => p.evaluate(() => ({ sem: document.getElementById('v-sem').textContent, eco: document.getElementById('v-eco').textContent,
    leco: document.getElementById('l-eco').textContent, ufh: document.getElementById('uf-h').textContent, h: document.getElementById('capt-h').textContent }));
  console.log('inicial', JSON.stringify(await read()));
  // troca de estado
  const ufs = await p.evaluate(() => [...document.getElementById('uf').options].map(o => o.value));
  console.log('estados', ufs.length, ufs.join(' '));
  for (const u of ['MT', 'RJ', 'AC']) { if (ufs.includes(u)) { await p.selectOption('#uf', u); console.log(u, JSON.stringify(await read())); } }
  await p.selectOption('#uf', 'SP');
  // área e sistema
  await p.fill('#area', '250'); console.log('250 m²', JSON.stringify(await read()));
  await p.click('#sis button[data-v="wf"]'); console.log('wood', JSON.stringify(await read()));
  await p.click('#sis button[data-v="alv"]'); console.log('alvenaria', JSON.stringify(await read()));
  await p.click('#sis button[data-v="mod"]'); console.log('modular', JSON.stringify(await read()));
  await p.fill('#area', ''); console.log('vazio', await p.evaluate(() => document.getElementById('area-h').textContent));
  await p.fill('#area', '150'); await p.click('#sis button[data-v="sf"]');
  // formulário: validação
  await p.click('#lead button[type=submit]');
  console.log('erro 1:', await p.evaluate(() => document.getElementById('lead-h').textContent));
  await p.fill('#l-nome', 'Visitante de Teste'); await p.fill('#l-fone', '14 9'); await p.click('#lead button[type=submit]');
  console.log('erro 2:', await p.evaluate(() => document.getElementById('lead-h').textContent));
  await p.fill('#l-fone', '(14) 90000-0000'); await p.fill('#l-mail', 'teste@'); await p.click('#lead button[type=submit]');
  console.log('erro 3:', await p.evaluate(() => document.getElementById('lead-h').textContent));
  await p.fill('#l-mail', 'teste@exemplo.com.br'); await p.fill('#l-cid', 'Marília'); await p.selectOption('#l-fase', 'obra em andamento'); await p.check('#l-av');
  const [pop] = await Promise.all([ctx.waitForEvent('page'), p.click('#lead button[type=submit]')]);
  await p.waitForTimeout(600);
  const u = new URL(await p.evaluate(() => document.getElementById('lead-a').href));
  console.log('janela nova:', pop.url().slice(0, 60));
  console.log('abriu:', u.origin + u.pathname);
  console.log('mensagem:\n' + u.searchParams.get('text'));
  console.log('aviso:', await p.evaluate(() => document.getElementById('lead-ok').hidden ? '(oculto)' : document.getElementById('lead-ok').textContent));
  // contadores
  await p.evaluate(() => document.getElementById('obras-aferidas').scrollIntoView()); await p.waitForTimeout(2000);
  console.log('contadores:', await p.evaluate(() => [...document.querySelectorAll('[data-count]')].map(e => e.textContent).join(' | ')));
  console.log('erros de script:', errs.length ? errs : 'nenhum');
  await b.close();
})();
