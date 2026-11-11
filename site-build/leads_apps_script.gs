// Base de contatos do site (calculadora de INSS).
// Colar em: planilha "Base de contatos - site (calculadora de INSS)" > Extensões > Apps Script.
// Implantar > Nova implantação > App da Web; Executar como: eu; Quem pode acessar: qualquer pessoa.
// A URL que termina em /exec vai em LEADS (tipo='script') no inss_page.py.
var CAMPOS = ['nome', 'whatsapp', 'email', 'cidade', 'uf', 'area', 'sistema', 'fase', 'estimativa', 'avisos'];
function limpa(v) {
  v = String(v == null ? '' : v).slice(0, 200);
  return /^[=+\-@]/.test(v) ? "'" + v : v;   // evita que o texto vire fórmula na planilha
}
function doPost(e) {
  var lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    var d = JSON.parse(e.postData.contents || '{}');
    if (!d.nome || !d.whatsapp) return ContentService.createTextOutput('faltou');
    var linha = [new Date()].concat(CAMPOS.map(function (k) { return limpa(d[k]); }));
    SpreadsheetApp.getActiveSpreadsheet().getSheets()[0].appendRow(linha);
    return ContentService.createTextOutput('ok');
  } finally { lock.releaseLock(); }
}
