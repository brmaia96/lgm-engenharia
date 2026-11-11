// teste funcional da calculadora de INSS e do cadastro: node test_inss.js <pasta do site>
// Fluxo: o visitante escolhe estado, área e sistema, identifica-se e só então vê o resultado.
const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.goto('file://' + dir + '/inss.html');
  await p.waitForTimeout(400);
  const g = id => p.evaluate(i => { const e = document.getElementById(i); return e.hidden ? '(oculto)' : e.textContent.trim(); }, id);
  const vis = () => p.evaluate(() => ({ resultado: !document.getElementById('out').hidden, cadastro: !document.getElementById('gate').hidden }));
  console.log('antes do cadastro:', JSON.stringify(await vis()), '|', await g('uf-h'));
  const ufs = await p.evaluate(() => [...document.getElementById('uf').options].map(o => o.value));
  console.log('estados:', ufs.length);
  // validação
  const sub = () => p.click('#lead-b');
  await sub(); console.log('erro 1:', await g('lead-h'));
  await p.fill('#l-nome', 'Visitante de Teste'); await p.fill('#l-fone', '14 9'); await sub(); console.log('erro 2:', await g('lead-h'));
  await p.fill('#l-fone', '(14) 90000-0000'); await p.fill('#l-mail', 'teste@'); await sub(); console.log('erro 3:', await g('lead-h'));
  await p.fill('#l-mail', 'teste@exemplo.com.br'); await sub(); console.log('erro 4:', await g('lead-h'));
  await p.fill('#l-cid', 'Marília'); await sub(); console.log('erro 5:', await g('lead-h'));
  console.log('ainda fechado:', JSON.stringify(await vis()));
  await p.selectOption('#l-fase', 'obra em andamento'); await p.check('#l-ok'); await p.check('#l-av');
  const [pop] = await Promise.all([ctx.waitForEvent('page'), sub()]);
  await p.waitForTimeout(500);
  console.log('depois do cadastro:', JSON.stringify(await vis()));
  console.log('SP 150 m² steel frame:', await g('v-sem'), '|', await g('v-eco'), '|', await g('lead-ok'));
  const u = new URL(await p.evaluate(() => document.getElementById('wa').href));
  console.log('conversa:', u.origin + u.pathname, '\n' + u.searchParams.get('text'));
  // resultado ao vivo depois de liberado
  for (const uf of ['MT', 'RJ']) { await p.selectOption('#uf', uf); console.log(uf + ':', await g('v-sem'), '|', await g('v-eco'), '|', await g('uf-h')); }
  await p.selectOption('#uf', 'SP'); await p.fill('#area', '250'); console.log('SP 250 m²:', await g('v-sem'), '|', await g('v-eco'));
  await p.click('#sis button[data-v="wf"]'); console.log('wood frame:', await g('v-eco'));
  await p.click('#sis button[data-v="alv"]'); console.log('alvenaria:', await g('v-eco'), '|', await g('l-eco'));
  // recarregar: quem já se identificou vê direto
  await p.reload(); await p.waitForTimeout(300); console.log('ao voltar:', JSON.stringify(await vis()));
  // contadores
  await p.evaluate(() => document.getElementById('obras-aferidas').scrollIntoView()); await p.waitForTimeout(2000);
  console.log('contadores:', await p.evaluate(() => [...document.querySelectorAll('[data-count]')].map(e => e.textContent).join(' | ')));
  console.log('erros de script:', errs.length ? errs : 'nenhum');
  await b.close();
})();
