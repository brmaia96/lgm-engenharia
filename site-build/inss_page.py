# -*- coding: utf-8 -*-
# Página de INSS de obra do site L. Engenharia.
#
# REGRA EDITORIAL (instrução direta do cliente, nov/2026): básico, direto e reto. A página mostra que existe
# imposto, que existe caminho para pagar menos e que o engenheiro domina o assunto. O "como" fica para a
# conversa: nada de passo a passo, lista de notas, percentuais de enquadramento ou memória de cálculo.
# Ordem pedida: cálculo breve -> calculadora (estado + VAU automático) -> contato -> mapa das obras aferidas
# com contador de m² e de desconto -> steel frame, wood frame e modular -> perguntas frequentes -> fontes (só título).
#
# Fonte única dos números: a home repete o exemplo daqui (NUM).
# Regras conferidas no texto consolidado da IN RFB 2.021/2021, na IN RFB 2.061/2021 e no Manual do Sero v3.0.
# A versão longa e conferida da página está em inss_page.py.bak-v19.
import json, os, re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- regra do cálculo (residencial unifamiliar, obra nova, pessoa física) ----
EQ_ATE_1000, EQ_ACIMA = .89, .85     # área equivalente (IN 2.021, art. 25, § 6º, I)
P_ALV = .20                          # mão de obra presumida, alvenaria (art. 25, § 16, I)
P_MISTA = .15                        # madeira ou mista (art. 25, § 16, II)
RED_PRE = .70                        # redução por pré-fabricado (art. 26, § 2º)
ALIQ = .368                          # soma das alíquotas (Manual do Sero, item 23)
def eq(a): return EQ_ATE_1000 if a <= 1000 else EQ_ACIMA
def fs(a): return .20 if a <= 100 else .40 if a <= 200 else .55 if a <= 300 else .70 if a <= 400 else .90   # fator social (art. 26, § 1º)

# ---- VAU por estado: residencial unifamiliar. Arquivo gerado a partir da tabela do Sero (ver vau_uf.json) ----
VAUS = json.load(open(HERE + '/vau_uf.json', encoding='utf-8'))
UFS = [('AC','Acre'),('AL','Alagoas'),('AP','Amapá'),('AM','Amazonas'),('BA','Bahia'),('CE','Ceará'),('DF','Distrito Federal'),('ES','Espírito Santo'),
       ('GO','Goiás'),('MA','Maranhão'),('MT','Mato Grosso'),('MS','Mato Grosso do Sul'),('MG','Minas Gerais'),('PA','Pará'),('PB','Paraíba'),('PR','Paraná'),
       ('PE','Pernambuco'),('PI','Piauí'),('RJ','Rio de Janeiro'),('RN','Rio Grande do Norte'),('RS','Rio Grande do Sul'),('RO','Rondônia'),('RR','Roraima'),
       ('SC','Santa Catarina'),('SP','São Paulo'),('SE','Sergipe'),('TO','Tocantins')]
VAU_UF = {k: v for k, v in VAUS['ufs'].items() if v}

def brl(v): return 'R$\u00a0' + format(int(round(v)), ',d').replace(',', '.')   # espaço que não quebra entre R$ e o número
def dec(v, n=1): return format(v, ',.%df' % n).replace(',', 'X').replace('.', ',').replace('X', '.')
def inss(area, uf):
    # mesma sequência do Sero, conferida nas memórias de cálculo reais do cliente: área equivalente com duas casas,
    # custo da obra = área equivalente x VAU, mão de obra de 20% (alvenaria), fator social e alíquota.
    aeq = round(area * eq(area), 2); cod = round(aeq * VAU_UF[uf], 2)
    return cod * P_ALV * fs(area) * ALIQ

# ---- exemplo que a home repete ----
AREA, UF_EX = 150, 'SP'
VAU = VAU_UF[UF_EX]
INSS_ALV = inss(AREA, UF_EX)
ECON = INSS_ALV * RED_PRE
NUM = dict(area='%d m²' % AREA, uf='São Paulo', sem=brl(INSS_ALV), econ=brl(ECON), pct='70%')

# ---- contato: para onde vai cada cadastro ----
WHATS = '5514991850799'
# Base de contatos. Deixar url vazio = o cadastro segue só pelo WhatsApp. Com um Formulário Google do cliente,
# preencher url (https://docs.google.com/forms/d/e/<id>/formResponse) e o código entry.N de cada campo:
# cada envio vira uma linha na planilha dele.
# Dois formatos aceitos: tipo='google' (Formulário Google: url .../formResponse + código entry.N de cada campo)
# ou tipo='json' (serviço que recebe JSON por POST). Com a base ligada, o botão só mostra o resultado e o
# WhatsApp vira o segundo passo, como no protótipo do cliente (pasta site-calculadora do Drive).
LEADS = dict(tipo='google', url='', campos=dict(nome='', whatsapp='', email='', cidade='', uf='', area='', sistema='', fase='', estimativa='', avisos=''))
COMUNIDADE_URL = ''   # link do grupo/comunidade do WhatsApp, quando o cliente criar

# ---- obras aferidas (mapa e contadores) ----
_BR = json.load(open(HERE + '/brasil.json'))
# Fonte: memórias de cálculo do Sero guardadas no Drive do cliente (70 memórias, 38 obras, de 2021 a 2026).
# Entram 27 das 28 obras com aferição "Concluída" (fica fora a de Marília de 2021, a confirmar) e Franca, que tem a certidão. Ficam fora as dez com aferição
# ainda em rascunho (entre elas as salas comerciais de Marília, rascunho de 09/11/2026).
# Só cidade, área, ano e valores: nunca nome, CNO ou endereço.
OBRAS_CIDADES = [('Marília', 'SP', 16), ('Sinop', 'MT', 1), ('Água Boa', 'MT', 1), ('Assis', 'SP', 1), ('Botucatu', 'SP', 1), ('Franca', 'SP', 1),
                 ('Itupeva', 'SP', 1), ('Mirassol', 'SP', 1), ('Pedrinhas Paulista', 'SP', 1), ('Piraju', 'SP', 1), ('São Roque', 'SP', 1),
                 ('Tupã', 'SP', 1), ('Vargem Grande Paulista', 'SP', 1)]
# m² aferidos em cada obra (área principal + complementar da memória concluída); o último é Franca
AREAS_AFERIDAS = [141.93, 280.73, 275.77, 272.37, 174.16, 235.04, 60.60, 308.58, 28.87, 59.00, 55.00, 302.20, 409.11, 175.82, 204.96, 30.22,
                  399.96, 260.46, 106.41, 211.66, 340.92, 370.63, 266.85, 115.10, 445.71, 150.00, 318.18, 139.37]
# Desconto documentado, com um critério só:
#  - enquadramento (duas primeiras): simulação anterior x aferição concluída;
#  - fator de ajuste (as demais): débito que a própria memória concluída apura antes do fator de ajuste, zerado por ele.
# Não entram reduções por remuneração declarada (o INSS dessa folha foi pago mês a mês) nem obra sem valor anterior na memória.
DESCONTOS = [('Marília', '400 m²', '2026', 29668.63, 0.0), ('Sinop', '205 m²', '2026', 27026.57, 7909.57),
             ('Assis', '446 m²', '2026', 10378.47, 0.0), ('Marília', '371 m²', '2026', 7624.20, 0.0), ('Marília', '212 m²', '2025', 4513.47, 0.0),
             ('Piraju', '106 m²', '2025', 1114.39, 0.0), ('Tupã', '142 m²', '2021', 1098.34, 0.0), ('Marília', '61 m²', '2022', 330.61, 0.0)]
CASOS = DESCONTOS[:4]     # a tabela da página mostra só os quatro maiores
M2_TOTAL = sum(AREAS_AFERIDAS)
N_OBRAS = sum(c[2] for c in OBRAS_CIDADES); ECON_REAL = sum(d[3] - d[4] for d in DESCONTOS)
N_DESC = len(DESCONTOS); N_CID = len(OBRAS_CIDADES)
EXT = {3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez'}
N_DESC_EXT = EXT.get(N_DESC, str(N_DESC))
# Com a obra de Marília de 2021 (576,18 m²; 46.802,38 -> 18.649,69) os totais voltam a 29 obras, 6.715,79 m² e R$ 101.997,80 em nove.
# Para repor: 576.18 em AREAS_AFERIDAS, Marília com 17 e a tupla ('Marília', '576 m²', '2021', 46802.38, 18649.69) em DESCONTOS.
assert N_OBRAS == len(AREAS_AFERIDAS) == 28 and abs(ECON_REAL - 73845.11) < .01 and abs(M2_TOTAL - 6139.61) < .01

FAQ = [
 ('Toda obra paga INSS?', 'Quase toda. Quem constrói, reforma ou amplia responde pela contribuição da mão de obra. As exceções são poucas.'),
 ('Quando tenho que resolver isso?', 'Antes de começar. A obra é inscrita na Receita em até 30 dias do início, e o que é declarado ali define o imposto no fim.'),
 ('Steel frame paga menos INSS?', 'Pode pagar. A norma trata estrutura de metal e pré-fabricado de forma diferente da alvenaria, mas nada é automático.'),
 ('Minha obra já está pronta. Ainda dá para reduzir?', 'Em muitos casos, sim. Depende dos documentos que existem e de quando a obra terminou.'),
 ('Construí há mais de cinco anos. Ainda devo?', 'Depende da data e da prova dessa data. Parte da obra, ou toda ela, pode já estar fora do alcance da cobrança.'),
 ('O valor da calculadora é o que eu vou pagar?', 'Não. É uma estimativa do que a Receita cobraria sem planejamento, com a obra calculada como alvenaria e o valor de referência do estado. O valor oficial sai do sistema da Receita, no dia da aferição.'),
 ('Atende fora de Marília?', 'Sim. A regularização é feita pela internet, para obra em qualquer cidade do Brasil.'),
]
FAQ_LD = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}, ensure_ascii=False) + '</script>'

def mapa_obras():
    dots = ''
    for nome, uf, n in sorted(OBRAS_CIDADES, key=lambda c: -c[2]):
        x, y = _BR['pts'][nome]; r = 10 if n > 1 else 4
        dots += '<circle cx="%s" cy="%s" r="%s" fill="#9A7350"><title>%s, %s: %d %s</title></circle>' % (x, y, r, nome, uf, n, 'obras' if n > 1 else 'obra')
    def lab(nome, txt, dx): x, y = _BR['pts'][nome]; return '<text x="%s" y="%s" text-anchor="end" font-size="20" fill="#6B6868">%s</text>' % (x - dx, y + 7, txt)
    labels = lab('Marília', 'Marília, %d obras' % OBRAS_CIDADES[0][2], 40) + lab('Sinop', 'Sinop, MT', 14) + lab('Água Boa', 'Água Boa, MT', 14)
    svg = ('<svg viewBox="0 0 %d %d" role="img" aria-label="Mapa do Brasil com as cidades das obras aferidas: %s." font-family="inherit">'
           '<path d="%s" fill="#F7F6F4" stroke="#A0A09F" stroke-width="1" stroke-linejoin="round"/>%s%s</svg>') % (
           _BR['w'], _BR['h'], '; '.join('%s, %s, %d' % c for c in OBRAS_CIDADES), _BR['path'], dots, labels)
    def lista(uf):
        cs = [('%s (%d)' % (c[0], c[2]) if c[2] > 1 else c[0]) for c in OBRAS_CIDADES if c[1] == uf]
        return cs[0] if len(cs) == 1 else ', '.join(cs[:-1]) + ' e ' + cs[-1]
    cid = '<div><dt>São Paulo</dt><dd>%s</dd></div><div><dt>Mato Grosso</dt><dd>%s</dd></div>' % (lista('SP'), lista('MT'))
    assert all(c[1] in ('SP', 'MT') for c in OBRAS_CIDADES)
    casos = ''.join('<tr><th scope="row">%s<span class="ar">, %s</span></th><td class="c-ar">%s</td><td class="c-an">%s</td><td class="off">%s</td><td>%s</td><td class="hl">%s</td></tr>' % (
        c, ar, ar, an, brl(x), brl(y), brl(round(x) - round(y))) for c, ar, an, x, y in CASOS)
    m2 = format(round(M2_TOTAL), ',d').replace(',', '.')
    return ('''<section class="band sec" id="obras-aferidas"><div class="tag"><b>Obras aferidas</b></div><div>
<h2>Não é teoria. <b>É obra aferida.</b></h2>
<div class="nums" style="margin-top:36px">
<div><div class="num" data-count="%d">%d</div><div class="nl">obras aferidas na Receita, em %d cidades</div></div>
<div><div class="num" data-count="%d" data-suf=" m²">%s m²</div><div class="nl">de área aferida</div></div>
<div><div class="num sv" data-count="%d" data-pre="R$ ">%s</div><div class="nl">de desconto obtido em %s delas</div></div>
</div>
<div class="mapa" style="margin-top:56px">
<figure class="fig">%s</figure>
<div><dl class="ufs">%s</dl>
<div class="scroll"><table class="tb casos"><caption class="sr">Os quatro maiores descontos</caption><thead><tr><th scope="col">Cidade</th><th scope="col" class="c-ar">Área</th><th scope="col" class="c-an">Ano</th><th scope="col">Antes</th><th scope="col">Depois</th><th scope="col">Desconto</th></tr></thead><tbody>%s</tbody></table></div>
<p class="src" style="margin-top:16px">Os quatro maiores. Antes e depois são o saldo na aferição final, sem contar o INSS recolhido ao longo da obra. Valores das memórias de cálculo da Receita Federal.</p></div>
</div>
</div></section>
''') % (N_OBRAS, N_OBRAS, N_CID, round(M2_TOTAL), m2, round(ECON_REAL), brl(ECON_REAL), N_DESC_EXT, svg, cid, casos)

_BODY = '''<main>
<section class="col phead"><p class="crumb">engenharia tributária</p>
<h1>A obra paga INSS. <b>Quase sempre a mais.</b></h1>
<p class="lead" style="margin-top:26px">Sem planejamento, a Receita Federal cobra pela área construída. <b>Com o enquadramento certo, a conta cai.</b></p></section>

<section class="band sec-s" id="calculo"><div class="tag"><b>O cálculo</b></div><div>
<h2>Como a Receita chega ao valor</h2>
<ol class="steps mini" style="margin-top:36px">
<li><h3>Custo da obra</h3><p>A área, pelo valor do m² do estado.</p></li>
<li><h3>Mão de obra</h3><p>Parte do custo, pelo tipo de obra.</p></li>
<li><h3>Fator social</h3><p>Redutor pela área, na pessoa física.</p></li>
<li><h3>Alíquota</h3><p>36,8% sobre o que sobrou.</p></li>
</ol>
</div></section>

<section class="band sec" id="simulador"><div class="tag"><b>Calculadora</b></div><div>
<h2>Quanto a Receita cobraria da sua obra?</h2>
<form id="f" method="post" novalidate style="margin-top:34px">
<div class="calc">
<div><label for="uf">Estado</label><select id="uf" name="uf">[[UF_OPTS]]</select><p class="hint info" id="uf-h"></p></div>
<div><label for="area">Área construída (m²)</label><input id="area" name="area" type="number" inputmode="decimal" min="1" step="1" value="[[AREA]]" aria-describedby="area-h"><input id="area-r" class="rg" type="range" min="40" max="600" step="5" value="[[AREA]]" aria-label="Área construída"><p class="hint" id="area-h" role="alert"></p></div>
<div><span class="lab" id="sis-l">Sistema construtivo</span><div class="seg" id="sis" role="group" aria-labelledby="sis-l">
<button type="button" data-v="alv" aria-pressed="false">alvenaria</button><button type="button" data-v="sf" aria-pressed="true">steel frame</button><button type="button" data-v="wf" aria-pressed="false">wood frame</button><button type="button" data-v="mod" aria-pressed="false">modular</button></div></div>
</div>
<div class="capt" id="gate">
<h3>O resultado sai na hora. <b>Diga para quem é.</b></h3>
<div class="calc four" style="margin-top:30px">
<div><label for="l-nome">Nome</label><input id="l-nome" name="nome" type="text" autocomplete="name" autocapitalize="words" required aria-describedby="l-nome-h"><p class="hint" id="l-nome-h"></p></div>
<div><label for="l-fone">WhatsApp, com DDD</label><input id="l-fone" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(14) 90000-0000" required aria-describedby="l-fone-h"><p class="hint" id="l-fone-h"></p></div>
<div><label for="l-mail">E-mail</label><input id="l-mail" name="email" type="email" autocomplete="email" autocapitalize="off" spellcheck="false" required aria-describedby="l-mail-h"><p class="hint" id="l-mail-h"></p></div>
<div><label for="l-cid">Cidade da obra</label><input id="l-cid" name="cidade" type="text" autocomplete="address-level2" autocapitalize="words" required aria-describedby="l-cid-h"><p class="hint" id="l-cid-h"></p></div>
<div><label for="l-fase">Em que fase está</label><select id="l-fase" name="fase"><option value="ainda vou construir">Ainda vou construir</option><option value="obra em andamento">Obra em andamento</option><option value="obra concluída, falta regularizar">Obra concluída, falta regularizar</option></select></div>
</div>
<label class="chk"><input type="checkbox" id="l-ok" name="aceite" required aria-describedby="l-ok-h"><span>Autorizo o contato sobre esta simulação. Meus dados não são passados a terceiros.</span></label>
<p class="hint" id="l-ok-h"></p>
<label class="chk" style="margin-top:12px"><input type="checkbox" id="l-av" name="avisos"><span>Quero receber avisos sobre INSS de obra e steel frame.</span></label>
<p class="hint" id="lead-h" role="alert"></p>
<button class="btn" type="submit" id="lead-b">[[BTN]]</button>[[BTN_NOTE]]
</div>
</form>
<div class="out" id="out" tabindex="-1" aria-labelledby="out-t" style="margin-top:44px" hidden>
<h3 class="meta" id="out-t">Sua estimativa</h3>
<div class="nums two" aria-live="polite" aria-atomic="true">
<div><div class="num" id="v-sem">—</div><div class="nl">de INSS, sem planejamento</div></div>
<div><div class="num sv" id="v-eco">—</div><div class="nl" id="l-eco">a menos, com o enquadramento certo</div></div>
</div>
<p class="ok" id="lead-ok" hidden><span id="lead-t"></span></p>
<p style="margin-top:30px"><a class="btn" id="wa" href="https://wa.me/[[WHATS]]" target="_blank" rel="noopener" style="margin-top:0">Quero pagar menos: falar com o engenheiro</a></p>
<p class="src" style="margin-top:26px">Estimativa para pessoa física, obra nova residencial, calculada como alvenaria, com o valor por metro quadrado de [[VAU_MES]]. O valor oficial sai do sistema da Receita, no dia da aferição.</p>
</div>
<p class="note" style="margin-top:44px"><b>Obra comercial, multifamiliar ou reforma?</b> A conta é outra. <a href="https://wa.me/[[WHATS]]?text=[[MSG_OUTRA]]" target="_blank" rel="noopener">Peça a simulação pelo WhatsApp</a></p>
</div></section>

[[MAPA]]

<section class="band sec" id="sistemas"><div class="tag"><b>Sistemas</b></div><div>
<h2>Steel frame, wood frame e modular <b>podem pagar menos.</b></h2>
<div class="sys" style="margin-top:40px">
<div><h3>Steel frame</h3><p>A norma trata a estrutura de metal de forma diferente da alvenaria.</p></div>
<div><h3>Wood frame</h3><p>Na estrutura de madeira, a mão de obra presumida é menor.</p></div>
<div><h3>Modular</h3><p>O módulo que chega pronto da fábrica reduz a base do imposto.</p></div>
</div>
<p class="note" style="margin-top:44px"><b>Nada é automático.</b> O enquadramento depende do projeto e das notas fiscais. É o que eu analiso com você.</p>
</div></section>
<img class="wide obra" src="[[IMG]]" width="[[IMGW]]" height="[[IMGH]]" alt="Estrutura em light steel frame vista por dentro: montantes, guias e treliças de aço galvanizado" loading="lazy" decoding="async" style="object-position:50% 50%;aspect-ratio:21/9">
<div class="col"><div class="cap"><b><a href="o-casa-taquaracu.html">Casa Taquaraçu</a></b><span>estrutura em light steel frame</span></div></div>

<section class="band sec" id="perguntas"><h2 class="tag">Perguntas frequentes</h2><div>
<div class="faq">
[[FAQ]]
</div>
</div></section>

<section class="band sec-n"><h2 class="tag">Fontes</h2><div>
<ol class="fontes">
<li><span>Instrução Normativa RFB nº 2.021, de 2021</span></li>
<li><span>Instrução Normativa RFB nº 2.061, de 2021</span></li>
<li><span>Manual do Sero, Receita Federal</span></li>
</ol>
</div></section>
[[CALL]]
</main>
<script>(function(){
var VAU=[[VAU_JSON]],UFN=[[UFN_JSON]],ALIQ=[[ALIQ]],WA='[[WHATS]]',LD=[[LEADS_JSON]];
var NOME={alv:'alvenaria',sf:'steel frame',wf:'wood frame',mod:'modular'},RED={alv:0,sf:[[RED_PRE]],wf:[[RED_MISTA]],mod:[[RED_PRE]]};
function fs(a){return a<=100?.20:a<=200?.40:a<=300?.55:a<=400?.70:.90}
function eq(a){return a<=1000?[[EQ1]]:[[EQ2]]}
function $(i){return document.getElementById(i)}
function brl(v){return 'R$\\u00a0'+Math.round(v).toLocaleString('pt-BR')}
var ar=$('area'),rg=$('area-r'),uf=$('uf'),seg=$('sis'),h=$('area-h'),S={sis:'sf',v:0,e:0,a:0,d:null},ok=false;
function msg(){var d=S.d,m=['Olá Gustavo, fiz a simulação do INSS da minha obra no site.',''];
if(d){m.push('Nome: '+d.nome,'WhatsApp: '+d.whatsapp,'E-mail: '+d.email,'Cidade: '+d.cidade+' · '+uf.value)}else{m.push('Estado: '+UFN[uf.value])}
m.push('Obra: '+S.a.toLocaleString('pt-BR')+' m² · '+NOME[S.sis]+(d?' · '+d.fase:''),'Estimativa do site: '+brl(S.v)+' sem planejamento');
if(d&&d.avisos==='sim')m.push('Quero receber os avisos sobre INSS de obra e steel frame.');
m.push('','Quero saber como pagar menos.');return 'https://wa.me/'+WA+'?text='+encodeURIComponent(m.join('\\n'))}
function pick(v){S.sis=v;[].forEach.call(seg.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x.getAttribute('data-v')===v?'true':'false')})}
/* mesma sequência do Sero: área equivalente com duas casas, custo da obra, 20% de mão de obra, fator social, alíquota */
function calc(){var a=parseFloat(String(ar.value).replace(',','.'));
if(!(a>0)){ar.classList.add('err');ar.setAttribute('aria-invalid','true');h.textContent='Informe a área construída em m².';$('v-sem').textContent='—';$('v-eco').textContent='—';return false}
ar.classList.remove('err');ar.removeAttribute('aria-invalid');h.textContent='';
var u=uf.value,aeq=Math.round(a*eq(a)*100)/100,cod=Math.round(aeq*VAU[u]*100)/100,v=cod*[[P_ALV]]*fs(a)*ALIQ,e=v*RED[S.sis];S.v=v;S.e=e;S.a=a;
$('uf-h').textContent='Valor por m² em '+UFN[u]+': '+brl(VAU[u]);
if(!ok)return true;
$('v-sem').textContent=brl(v);
if(e>0){$('v-eco').textContent='até '+brl(e);$('l-eco').textContent='a menos, com o enquadramento certo'}
else{$('v-eco').textContent='depende';$('l-eco').textContent='na alvenaria, a redução vem de outro caminho'}
$('wa').href=msg();
/* guarda a última simulação de quem já se identificou: só estado, área e sistema */
if(ok){try{localStorage.setItem('l-inss-sim',JSON.stringify({uf:u,a:a,sis:S.sis}))}catch(x){}}
return true}
ar.addEventListener('input',function(){var a=parseFloat(ar.value);if(a>0)rg.value=Math.min(600,Math.max(40,a));calc()});
rg.addEventListener('input',function(){ar.value=rg.value;calc()});
uf.addEventListener('change',calc);
seg.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b)return;pick(b.getAttribute('data-v'));calc()});
/* Enter na área só calcula; não envia o cadastro pela metade */
ar.addEventListener('keydown',function(ev){if(ev.key==='Enter'){ev.preventDefault();if(calc()&&!$('gate').hidden)$('l-nome').focus()}});
function abre(){ok=true;$('gate').hidden=true;$('out').hidden=false}
/* quem já se identificou neste navegador vê o resultado direto, com a própria simulação (nenhum dado pessoal é guardado) */
try{if(localStorage.getItem('l-inss-ok')==='1'){var sim=JSON.parse(localStorage.getItem('l-inss-sim')||'null');
if(sim&&VAU[sim.uf]&&sim.a>0&&NOME[sim.sis]){uf.value=sim.uf;ar.value=sim.a;rg.value=Math.min(600,Math.max(40,sim.a));pick(sim.sis)}
abre()}}catch(x){}
calc();
/* contato: os dados vêm antes do resultado. Sem base configurada, a conversa no WhatsApp abre com tudo preenchido */
var lf=$('f'),lh=$('lead-h');
var CAMPOS=[ ['l-nome',function(v){return v.trim().length>=2},'Informe o seu nome.'],
['l-fone',function(v){return v.replace(/\\D/g,'').length>=10},'Informe o WhatsApp com DDD.'],
['l-mail',function(v){return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v.trim())},'Informe um e-mail válido.'],
['l-cid',function(v){return v.trim().length>=2},'Informe a cidade da obra.']];
function marca(id,m){var el=$(id),hh=$(id+'-h');el.classList.toggle('err',!!m);if(m)el.setAttribute('aria-invalid','true');else el.removeAttribute('aria-invalid');if(hh)hh.textContent=m||''}
function limpa(){if(!$('gate').querySelector('.err'))lh.textContent=''}
CAMPOS.forEach(function(c){var el=$(c[0]);el.addEventListener('input',function(){if(el.classList.contains('err')&&c[1](el.value)){marca(c[0],'');limpa()}})});
$('l-ok').addEventListener('change',function(){if($('l-ok').checked){marca('l-ok','');limpa()}});
lf.addEventListener('submit',function(ev){ev.preventDefault();
if(!$('out').hidden)return;
var first=null;if(!calc())first=ar;
CAMPOS.forEach(function(c){var el=$(c[0]),good=c[1](el.value);marca(c[0],good?'':c[2]);if(!good&&!first)first=el});
var aceite=$('l-ok').checked;marca('l-ok',aceite?'':'Marque a autorização para ver o resultado.');if(!aceite&&!first)first=$('l-ok');
if(first){lh.textContent='Confira os campos marcados.';first.focus();return}
lh.textContent='';
var d={nome:$('l-nome').value.trim(),whatsapp:$('l-fone').value.trim(),email:$('l-mail').value.trim(),cidade:$('l-cid').value.trim(),
fase:$('l-fase').value,avisos:$('l-av').checked?'sim':'não'};
S.d=d;abre();try{localStorage.setItem('l-inss-ok','1')}catch(x){}
calc();var url=msg();$('wa').href=url;
var t=$('lead-t');
if(LD&&LD.url){
var reg={nome:d.nome,whatsapp:d.whatsapp,email:d.email,cidade:d.cidade,uf:uf.value,area:String(S.a),sistema:NOME[S.sis],fase:d.fase,estimativa:brl(S.v),avisos:d.avisos};
/* se a base não responder (rede, bloqueio do navegador), o contato não se perde: pede o envio pelo WhatsApp */
function falhou(){t.innerHTML='<b>Falta um toque:</b> envie a simulação pelo botão abaixo.'}
t.innerHTML='<b>Simulação registrada.</b> Retorno pelo seu WhatsApp.';
try{var pr;if(LD.tipo==='json'){pr=fetch(LD.url,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(reg)}).then(function(r){if(!r.ok)throw 0})}
else{var fd=new FormData();for(var k in LD.campos){if(LD.campos[k])fd.append(LD.campos[k],reg[k]||'')}pr=fetch(LD.url,{method:'POST',mode:'no-cors',body:fd})}
pr.catch(falhou)}catch(x){falhou()}}
else{var w=null;try{w=window.open(url,'_blank')}catch(x){}
if(w){try{w.opener=null}catch(x){}}
t.innerHTML=w?'O WhatsApp abriu com a sua simulação. <b>É só enviar a mensagem.</b>':'<b>Falta um toque:</b> envie a simulação pelo botão abaixo.'}
$('lead-ok').hidden=false;var o=$('out');try{o.focus({preventScroll:true})}catch(x){o.focus()}o.scrollIntoView({block:'nearest'});
});
/* contadores */
var cs=[].slice.call(document.querySelectorAll('[data-count]'));
function fmt(e,x){e.textContent=(e.getAttribute('data-pre')||'')+Math.round(x).toLocaleString('pt-BR')+(e.getAttribute('data-suf')||'')}
function run(e){var to=+e.getAttribute('data-count'),t0=null;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){fmt(e,to);return}
function st(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1400),q=1-Math.pow(1-p,3);fmt(e,to*q);if(p<1)requestAnimationFrame(st)}requestAnimationFrame(st)}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){run(x.target);io.unobserve(x.target)}})},{threshold:.6});cs.forEach(function(e){io.observe(e)})}
})();</script>'''

def inss_body(img=('img/inss/estrutura.jpg', 2000, 1125)):
    opts = ''.join('<option value="%s"%s>%s</option>' % (k, ' selected' if k == UF_EX else '', n) for k, n in UFS if k in VAU_UF)
    rep = {
        'AREA': str(AREA), 'VAU_MES': VAUS['rotulo'], 'UF_OPTS': opts,
        'VAU_JSON': json.dumps({k: round(v, 2) for k, v in VAU_UF.items()}), 'UFN_JSON': json.dumps({k: n for k, n in UFS if k in VAU_UF}, ensure_ascii=False),
        'ALIQ': repr(ALIQ), 'P_ALV': repr(P_ALV), 'RED_PRE': repr(RED_PRE), 'RED_MISTA': repr(round(1 - P_MISTA / P_ALV, 4)), 'EQ1': repr(EQ_ATE_1000), 'EQ2': repr(EQ_ACIMA),
        'WHATS': WHATS, 'LEADS_JSON': json.dumps(LEADS if LEADS['url'] else None),
        'BTN': 'Ver o INSS da minha obra' if LEADS['url'] else 'Ver o resultado e enviar pelo WhatsApp',
        'BTN_NOTE': '' if LEADS['url'] else '<p class="src">O WhatsApp abre com a simulação pronta. É só enviar.</p>',
        'MSG_OUTRA': quote('Olá Gustavo, quero uma simulação do INSS de uma obra comercial, multifamiliar ou reforma.'),
        'FAQ': '\n'.join('<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in FAQ),
        'MAPA': mapa_obras(),
        'CALL': ('<section class="col call"><h2>Quer saber quanto a sua obra pode pagar a menos?</h2><p class="links"><a class="lnk" href="#simulador">Calcular o INSS da minha obra</a>'
                 '<a class="lnk" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">Conversar pelo WhatsApp</a></p></section>') % (WHATS, quote('Olá Gustavo, vi a página de INSS no site e quero conversar sobre a minha obra.')), 'IMG': img[0], 'IMGW': str(img[1]), 'IMGH': str(img[2]),
    }
    out = re.sub(r'/\*.*?\*/\n?', '', _BODY, flags=re.S)   # o script publicado não leva os comentários
    for k, v in rep.items(): out = out.replace('[[%s]]' % k, v)
    assert '[[' not in out, out[out.index('[['):][:60]
    return out + FAQ_LD
