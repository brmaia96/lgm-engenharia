// Ilustrações editoriais do blog: uma por assunto, no estilo do site (papel, tinta, Jost). Sem dado inventado.
const { chromium } = require('playwright');
const fs = require('fs');
const F = __dirname + '/../fontes/x-fontsource-jost-5.3.0/package/files/';
const b64 = f => fs.readFileSync(F + f).toString('base64');
const css = [300, 400, 500].map(w => `@font-face{font-family:J;font-weight:${w};src:url(data:font/woff2;base64,${b64(`jost-latin-${w}-normal.woff2`)})}`).join('');
const INK = '#2F2E2E', BODY = '#6B6868', LINE = '#CFCBC4', PAPER = '#F6F4F0', TERRA = '#9A7350';
const page = svg => `<!doctype html><html><head><meta charset=utf-8><style>${css}html,body{margin:0;background:${PAPER}}svg{display:block}text{font-family:J}</style></head><body>${svg}</body></html>`;
const W = 1600, H = 900;
const arts = {
  // CNO: a ficha de inscrição da obra e o prazo de 30 dias contado do início
  'cno-prazo-e-inscricao': `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect x="300" y="150" width="560" height="640" fill="#fff" stroke="${LINE}" stroke-width="2"/>
    <text x="350" y="235" font-size="22" font-weight="500" fill="${BODY}" letter-spacing="1">Cadastro Nacional de Obras</text>
    <text x="350" y="320" font-size="96" font-weight="300" fill="${INK}">CNO</text>
    ${[400, 470, 540, 610, 680].map((y, i) => `<line x1="350" y1="${y}" x2="${i % 2 ? 700 : 810}" y2="${y}" stroke="${LINE}" stroke-width="2"/><rect x="350" y="${y - 30}" width="${[120, 90, 150, 70, 110][i]}" height="10" fill="${LINE}"/>`).join('')}
    <g transform="translate(980,250)">
      <rect x="0" y="0" width="360" height="380" fill="#fff" stroke="${INK}" stroke-width="2.5"/>
      <rect x="0" y="0" width="360" height="74" fill="${INK}"/>
      <line x1="80" y1="-26" x2="80" y2="26" stroke="${INK}" stroke-width="6"/><line x1="280" y1="-26" x2="280" y2="26" stroke="${INK}" stroke-width="6"/>
      <text x="180" y="250" text-anchor="middle" font-size="170" font-weight="300" fill="${INK}">30</text>
      <text x="180" y="320" text-anchor="middle" font-size="34" font-weight="400" fill="${BODY}">dias</text>
    </g>
    <line x1="860" y1="440" x2="960" y2="440" stroke="${TERRA}" stroke-width="2.5"/><path d="M948 430 L962 440 L948 450" fill="none" stroke="${TERRA}" stroke-width="2.5"/>
  </svg>`,
  // Decadência: cinco exercícios numa linha do tempo, contados a partir do ano seguinte
  'obra-antiga-decadencia': `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <line x1="180" y1="470" x2="1420" y2="470" stroke="${INK}" stroke-width="3"/>
    ${[0, 1, 2, 3, 4, 5].map(i => { const x = 300 + i * 200; return `<line x1="${x}" y1="440" x2="${x}" y2="500" stroke="${INK}" stroke-width="3"/>` }).join('')}
    ${[1, 2, 3, 4, 5].map(i => { const x = 200 + i * 200; return `<text x="${x}" y="560" text-anchor="middle" font-size="40" font-weight="300" fill="${INK}">${i}</text>` }).join('')}
    <rect x="300" y="380" width="1000" height="40" fill="${LINE}"/>
    <text x="800" y="330" text-anchor="middle" font-size="46" font-weight="300" fill="${INK}">cinco anos</text>
    <circle cx="300" cy="470" r="13" fill="${TERRA}"/>
    <text x="300" y="650" text-anchor="middle" font-size="26" fill="${BODY}">1º de janeiro</text>
    <text x="300" y="690" text-anchor="middle" font-size="26" fill="${BODY}">do ano seguinte</text>
    <text x="1300" y="650" text-anchor="middle" font-size="26" fill="${BODY}">o prazo</text>
    <text x="1300" y="690" text-anchor="middle" font-size="26" fill="${BODY}">se fecha</text>
  </svg>`,
  // Fator de ajuste: a balança entre o que a Receita presume e o que a obra declarou
  'fator-de-ajuste': `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <line x1="800" y1="190" x2="800" y2="720" stroke="${INK}" stroke-width="4"/>
    <path d="M700 740 L900 740 L860 712 L740 712 Z" fill="${INK}"/>
    <g>
      <line x1="430" y1="260" x2="1170" y2="260" stroke="${INK}" stroke-width="4"/>
      <line x1="470" y1="260" x2="400" y2="470" stroke="${INK}" stroke-width="2"/><line x1="470" y1="260" x2="540" y2="470" stroke="${INK}" stroke-width="2"/>
      <path d="M370 470 Q470 540 570 470 Z" fill="none" stroke="${INK}" stroke-width="3"/>
      <line x1="1130" y1="260" x2="1060" y2="470" stroke="${INK}" stroke-width="2"/><line x1="1130" y1="260" x2="1200" y2="470" stroke="${INK}" stroke-width="2"/>
      <path d="M1030 470 Q1130 540 1230 470 Z" fill="none" stroke="${INK}" stroke-width="3"/>
      <rect x="410" y="400" width="120" height="70" fill="${LINE}"/>
      <rect x="1075" y="380" width="110" height="90" fill="${TERRA}" opacity=".55"/>
    </g>
    <circle cx="800" cy="260" r="12" fill="${INK}"/>
    <text x="470" y="640" text-anchor="middle" font-size="34" font-weight="300" fill="${INK}">o que a Receita presume</text>
    <text x="1130" y="640" text-anchor="middle" font-size="34" font-weight="300" fill="${INK}">o que a obra declarou</text>
  </svg>`,
  // Conforto termoacústico: corte de uma parede em steel frame, camada por camada
  'steel-frame-conforto-termoacustico': (() => {
    const L = [['placa externa', 40, '#E2DED6'], ['membrana', 10, TERRA], ['OSB', 36, '#D9C7A8'], ['montante de aço com lã mineral', 240, '#EFE6D2'], ['placa de gesso', 30, '#ECEAE5'], ['placa de gesso', 30, '#E6E3DD']];
    let x = 380, s = '';
    L.forEach(([n, w, c], i) => {
      s += `<rect x="${x}" y="170" width="${w}" height="560" fill="${c}" stroke="${INK}" stroke-width="2"/>`;
      if (i === 3) { for (let k = 0; k < 9; k++) s += `<path d="M${x + 12} ${200 + k * 60} q ${w / 4} -22 ${w / 2 - 12} 0 t ${w / 2 - 12} 0" fill="none" stroke="#C9B48C" stroke-width="2"/>`; s += `<rect x="${x + w / 2 - 6}" y="170" width="12" height="560" fill="#9AA0A6"/>`; }
      const lx = x + w / 2, ly = 230 + i * 92, tx = 1000;
      s += `<circle cx="${lx}" cy="${ly}" r="5" fill="${INK}"/><polyline points="${lx},${ly} ${tx - 20},${ly}" fill="none" stroke="${BODY}" stroke-width="1.5"/><text x="${tx}" y="${ly + 9}" font-size="28" font-weight="300" fill="${INK}">${n}</text>`;
      x += w;
    });
    s += `<text x="380" y="780" font-size="24" fill="${BODY}">lado de fora</text><text x="${x}" y="780" text-anchor="end" font-size="24" fill="${BODY}">lado de dentro</text>`;
    return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${s}</svg>`;
  })(),
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1.5 });
  for (const [k, svg] of Object.entries(arts)) { await p.setContent(page(svg)); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: __dirname + '/' + k + '.png' }); console.log('ok', k); }
  await b.close();
})();
