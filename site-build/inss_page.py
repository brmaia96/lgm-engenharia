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
import json, os
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
OBRAS_CIDADES = [('Marília', 'SP', 8), ('Sinop', 'MT', 1), ('Franca', 'SP', 1), ('Itupeva', 'SP', 1), ('Vargem Grande Paulista', 'SP', 1), ('Pedrinhas Paulista', 'SP', 1)]
# só cidade, área, ano e valores das memórias de cálculo do Sero: nunca nome, CNO ou endereço
CASOS = [('Marília · 576 m² · 2021', 46802.38, 18649.69), ('Sinop · 205 m² · 2026', 27026.57, 7909.57), ('Marília · 371 m² · 2026', 7624.20, 0.0)]
AREAS_AFERIDAS = [576.18, 204.96, 370.63, 115.10, 302.20, 175.82, 174.16, 272.37, 308.58, 266.85, 169.14, 139.37, 318.18]   # m² de cada obra aferida
M2_TOTAL = sum(AREAS_AFERIDAS)
N_OBRAS = sum(c[2] for c in OBRAS_CIDADES); ECON_REAL = sum(a - b for _, a, b in CASOS)
assert N_OBRAS == len(AREAS_AFERIDAS) == 13 and abs(ECON_REAL - 54893.89) < .01

FAQ = [
 ('Toda obra paga INSS?', 'Quase toda. Quem constrói, reforma ou amplia responde pela contribuição da mão de obra. As exceções são poucas.'),
 ('Quando tenho que resolver isso?', 'Antes de começar. A obra é inscrita na Receita em até 30 dias do início, e o que é declarado ali define o imposto no fim.'),
 ('Steel frame paga menos INSS?', 'Pode pagar. A norma trata estrutura de metal e pré-fabricado de forma diferente da alvenaria, mas nada é automático.'),
 ('Minha obra já está pronta. Ainda dá para reduzir?', 'Em muitos casos, sim. Depende dos documentos que existem e de quando a obra terminou.'),
 ('Construí há mais de cinco anos. Ainda devo?', 'Depende da data e da prova dessa data. Parte da obra, ou toda ela, pode já estar fora do alcance da cobrança.'),
 ('O valor da calculadora é o que eu vou pagar?', 'Não. É uma estimativa do que a Receita cobraria sem planejamento, com o valor de referência do estado. O valor oficial sai do sistema da Receita, no dia da aferição.'),
 ('Atende fora de Marília?', 'Sim. A regularização é feita pela internet, para obra em qualquer cidade do Brasil.'),
]
FAQ_LD = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}, ensure_ascii=False) + '</script>'

def mapa_obras():
    dots = ''
    for nome, uf, n in sorted(OBRAS_CIDADES, key=lambda c: -c[2]):
        x, y = _BR['pts'][nome]; r = 10 if n > 1 else 5
        dots += '<circle cx="%s" cy="%s" r="%s" fill="#9A7350" stroke="#fff" stroke-width="2"><title>%s, %s: %d %s</title></circle>' % (x, y, r, nome, uf, n, 'obras' if n > 1 else 'obra')
    mx, my = _BR['pts']['Marília']; sx_, sy_ = _BR['pts']['Sinop']
    labels = ('<text x="%s" y="%s" text-anchor="end" font-size="15" fill="#2F2E2E">Marília · 8 obras</text>' % (mx - 18, my + 5)
              + '<text x="%s" y="%s" text-anchor="end" font-size="15" fill="#2F2E2E">Sinop · MT</text>' % (sx_ - 12, sy_ + 5))
    svg = ('<svg viewBox="0 0 %d %d" role="img" aria-label="Mapa do Brasil com as cidades das obras aferidas: %s." font-family="inherit">'
           '<path d="%s" fill="#F7F6F4" stroke="#A0A09F" stroke-width="1" stroke-linejoin="round"/>%s%s</svg>') % (
           _BR['w'], _BR['h'], '; '.join('%s, %s, %d' % c for c in OBRAS_CIDADES), _BR['path'], dots, labels)
    cid = ''.join('<li><b>%s</b><span>%s · %s</span></li>' % (c[0], c[1], ('%d obras' % c[2]) if c[2] > 1 else '1 obra') for c in OBRAS_CIDADES)
    casos = ''.join('<tr><th scope="row">%s</th><td class="off">%s</td><td>%s</td><td class="hl">%s</td></tr>' % (o, brl(a), brl(b), brl(a - b)) for o, a, b in CASOS)
    m2 = format(round(M2_TOTAL), ',d').replace(',', '.')
    return ('''<section class="band sec" id="obras-aferidas"><div class="tag"><b>Obras aferidas</b></div><div>
<h2>Não é teoria. <b>É obra aferida.</b></h2>
<div class="nums" style="margin-top:36px">
<div><div class="num" data-count="%d">%d</div><div class="nl">obras aferidas na Receita</div></div>
<div><div class="num" data-count="%d" data-suf=" m²">%s m²</div><div class="nl">de área regularizada</div></div>
<div><div class="num sv" data-count="%d" data-pre="R$ ">%s</div><div class="nl">de desconto obtido em três delas</div></div>
</div>
<div class="mapa" style="margin-top:64px">
<figure class="fig">%s</figure>
<ul class="cid">%s</ul>
</div>
<table class="tb casos" style="margin-top:56px"><thead><tr><th scope="col">Obra</th><th scope="col">Antes</th><th scope="col">Depois</th><th scope="col">Desconto</th></tr></thead><tbody>%s</tbody></table>
<p class="src" style="margin-top:18px">Valores das memórias de cálculo da Receita Federal.</p>
</div></section>
''') % (N_OBRAS, N_OBRAS, round(M2_TOTAL), m2, round(ECON_REAL), brl(ECON_REAL), svg, cid, casos)

_BODY = '''<main>
<section class="col phead"><p class="crumb">engenharia tributária</p>
<h1>A obra paga INSS. <b>Quase sempre a mais.</b></h1>
<p class="lead" style="margin-top:26px">Sem planejamento, a Receita Federal cobra pela área construída. <b>Com o enquadramento certo, a conta cai.</b></p></section>

<section class="band sec-s" id="calculo"><div class="tag"><b>O cálculo</b></div><div>
<h2>Como a Receita chega ao valor</h2>
<ol class="steps mini" style="margin-top:36px">
<li><h3>Custo da obra</h3><p>A área, pelo valor do metro quadrado do seu estado.</p></li>
<li><h3>Mão de obra</h3><p>Uma parte desse custo, conforme o tipo de obra.</p></li>
<li><h3>Fator social</h3><p>Um redutor conforme a área, para pessoa física.</p></li>
<li><h3>Alíquota</h3><p>36,8% sobre o que sobrou.</p></li>
</ol>
</div></section>

<section class="band sec" id="simulador"><div class="tag"><b>Calculadora</b></div><div>
<h2>Quanto a Receita cobraria da sua obra?</h2>
<form id="f" novalidate style="margin-top:34px">
<div class="calc">
<div><label for="uf">Estado</label><select id="uf">[[UF_OPTS]]</select><p class="hint info" id="uf-h"></p></div>
<div><label for="area">Área construída (m²)</label><input id="area" type="number" inputmode="decimal" min="1" step="1" value="[[AREA]]" aria-describedby="area-h"><input id="area-r" class="rg" type="range" min="40" max="600" step="5" value="[[AREA]]" aria-label="Área construída"><p class="hint" id="area-h" role="alert"></p></div>
<div><span class="lab" id="sis-l">Sistema construtivo</span><div class="seg" id="sis" role="group" aria-labelledby="sis-l">
<button type="button" data-v="alv" aria-pressed="false">alvenaria</button><button type="button" data-v="sf" aria-pressed="true">steel frame</button><button type="button" data-v="wf" aria-pressed="false">wood frame</button><button type="button" data-v="mod" aria-pressed="false">modular</button></div></div>
</div>
<div class="capt" id="gate">
<h3>O resultado sai na hora. <b>Diga para quem é.</b></h3>
<div class="calc four" style="margin-top:30px">
<div><label for="l-nome">Nome</label><input id="l-nome" name="nome" type="text" autocomplete="name" required></div>
<div><label for="l-fone">WhatsApp, com DDD</label><input id="l-fone" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(14) 90000-0000" required></div>
<div><label for="l-mail">E-mail</label><input id="l-mail" name="email" type="email" autocomplete="email" required></div>
<div><label for="l-cid">Cidade da obra</label><input id="l-cid" name="cidade" type="text" autocomplete="address-level2" required></div>
<div><label for="l-fase">Em que fase está</label><select id="l-fase" name="fase"><option value="ainda vou construir">Ainda vou construir</option><option value="obra em andamento">Obra em andamento</option><option value="obra concluída, falta regularizar">Obra concluída, falta regularizar</option></select></div>
</div>
<label class="chk"><input type="checkbox" id="l-ok" name="aceite" required><span>Autorizo o contato sobre esta simulação. Meus dados não são passados a terceiros.</span></label>
<label class="chk" style="margin-top:12px"><input type="checkbox" id="l-av" name="avisos"><span>Quero receber avisos sobre INSS de obra e steel frame.</span></label>
<p class="hint" id="lead-h" role="alert"></p>
<button class="btn" type="submit" id="lead-b">[[BTN]]</button>
</div>
</form>
<div class="out" id="out" aria-live="polite" style="margin-top:44px" hidden>
<div class="nums two">
<div><div class="num" id="v-sem">[[INSS_ALV]]</div><div class="nl">de INSS, sem planejamento</div></div>
<div><div class="num sv" id="v-eco">até [[ECON]]</div><div class="nl" id="l-eco">a menos, com o enquadramento certo</div></div>
</div>
<p class="ok" id="lead-ok" hidden><span id="lead-t"></span></p>
<p style="margin-top:30px"><a class="btn" id="wa" href="https://wa.me/[[WHATS]]" target="_blank" rel="noopener" style="margin-top:0">Quero pagar menos: falar com o engenheiro</a></p>
<p class="src" style="margin-top:26px">Estimativa para pessoa física, obra nova residencial, com o valor por metro quadrado de [[VAU_MES]]. O valor oficial sai do sistema da Receita, no dia da aferição.</p>
</div>
<p class="note" style="margin-top:44px"><b>Obra comercial, multifamiliar ou reforma?</b> A conta é outra. <a href="https://wa.me/[[WHATS]]?text=[[MSG_OUTRA]]" target="_blank" rel="noopener">Peça a simulação pelo WhatsApp</a></p>
</div></section>

[[MAPA]]

<section class="band sec" id="sistemas"><div class="tag"><b>Steel frame, wood frame e modular</b></div><div>
<h2>Steel frame, wood frame e modular <b>podem pagar menos.</b></h2>
<div class="sys" style="margin-top:40px">
<div><h3>Steel frame</h3><p>A norma trata a estrutura de metal de forma diferente da alvenaria.</p></div>
<div><h3>Wood frame</h3><p>Na estrutura de madeira, a mão de obra presumida é menor.</p></div>
<div><h3>Modular</h3><p>O módulo que chega pronto da fábrica reduz a base do imposto.</p></div>
</div>
<p class="note" style="margin-top:44px"><b>Nada é automático.</b> O enquadramento depende do projeto e das notas fiscais. É o que eu analiso com você.</p>
</div></section>
<img class="wide obra" src="[[IMG]]" width="[[IMGW]]" height="[[IMGH]]" alt="Estrutura em light steel frame vista por dentro: montantes, guias e treliças de aço galvanizado" loading="lazy" decoding="async" style="object-position:50% 50%">
<div class="col"><div class="cap"><b><a href="o-casa-taquaracu.html">Casa Taquaraçu</a></b><span>estrutura em light steel frame</span></div></div>

<section class="band sec" id="perguntas"><div class="tag"><b>Perguntas frequentes</b></div><div>
<div class="faq">
[[FAQ]]
</div>
</div></section>

<section class="band sec"><div class="tag"><b>Fontes</b></div><div>
<ol class="fontes">
<li><span>Instrução Normativa RFB nº 2.021, de 2021</span></li>
<li><span>Instrução Normativa RFB nº 2.061, de 2021</span></li>
<li><span>Manual do Sero, Receita Federal</span></li>
</ol>
</div></section>
</main>
<script>(function(){
var VAU=[[VAU_JSON]],UFN=[[UFN_JSON]],ALIQ=[[ALIQ]],WA='[[WHATS]]',LD=[[LEADS_JSON]];
var NOME={alv:'alvenaria',sf:'steel frame',wf:'wood frame',mod:'modular'},RED={alv:0,sf:[[RED_PRE]],wf:[[RED_MISTA]],mod:[[RED_PRE]]};
function fs(a){return a<=100?.20:a<=200?.40:a<=300?.55:a<=400?.70:.90}
function eq(a){return a<=1000?[[EQ1]]:[[EQ2]]}
function $(i){return document.getElementById(i)}
function brl(v){return 'R$\\u00a0'+Math.round(v).toLocaleString('pt-BR')}
var ar=$('area'),rg=$('area-r'),uf=$('uf'),seg=$('sis'),h=$('area-h'),S={sis:'sf',v:0,e:0,a:0,d:null};
function msg(){var d=S.d,m=['Olá Gustavo, fiz a simulação do INSS da minha obra no site.',''];
if(d){m.push('Nome: '+d.nome,'WhatsApp: '+d.whatsapp,'E-mail: '+d.email,'Cidade: '+d.cidade+' · '+uf.value)}else{m.push('Estado: '+UFN[uf.value])}
m.push('Obra: '+S.a.toLocaleString('pt-BR')+' m² · '+NOME[S.sis]+(d?' · '+d.fase:''),'Estimativa do site: '+brl(S.v)+' sem planejamento');
if(d&&d.avisos==='sim')m.push('Quero receber os avisos sobre INSS de obra e steel frame.');
m.push('','Quero saber como pagar menos.');return 'https://wa.me/'+WA+'?text='+encodeURIComponent(m.join('\\n'))}
/* mesma sequência do Sero: área equivalente com duas casas, custo da obra, 20% de mão de obra, fator social, alíquota */
function calc(){var a=parseFloat(String(ar.value).replace(',','.'));
if(!(a>0)){ar.classList.add('err');h.textContent='Informe a área construída em m².';return false}
ar.classList.remove('err');h.textContent='';
var u=uf.value,aeq=Math.round(a*eq(a)*100)/100,cod=Math.round(aeq*VAU[u]*100)/100,v=cod*[[P_ALV]]*fs(a)*ALIQ,e=v*RED[S.sis];S.v=v;S.e=e;S.a=a;
$('uf-h').textContent='Valor por m² em '+UFN[u]+': '+brl(VAU[u]);
$('v-sem').textContent=brl(v);
if(e>0){$('v-eco').textContent='até '+brl(e);$('l-eco').textContent='a menos, com o enquadramento certo'}
else{$('v-eco').textContent='depende';$('l-eco').textContent='na alvenaria, a redução vem de outro caminho'}
$('wa').href=msg();return true}
ar.addEventListener('input',function(){var a=parseFloat(ar.value);if(a>=40&&a<=600)rg.value=a;calc()});
rg.addEventListener('input',function(){ar.value=rg.value;calc()});
uf.addEventListener('change',calc);
seg.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b)return;S.sis=b.getAttribute('data-v');
[].forEach.call(seg.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});calc()});
function abre(){$('gate').hidden=true;$('out').hidden=false}
/* quem já se identificou neste navegador vê o resultado direto (guarda só a marca, nenhum dado pessoal) */
try{if(localStorage.getItem('l-inss-ok')==='1')abre()}catch(e){}
calc();
/* contato: os dados vêm antes do resultado. Sem base configurada, a conversa no WhatsApp abre com tudo preenchido */
var lf=$('f'),lh=$('lead-h');
lf.addEventListener('submit',function(ev){ev.preventDefault();
if(!$('out').hidden)return;
var d={nome:$('l-nome').value.trim(),whatsapp:$('l-fone').value.trim(),email:$('l-mail').value.trim(),cidade:$('l-cid').value.trim(),
fase:$('l-fase').value,avisos:$('l-av').checked?'sim':'não'},bad=null;
if(!calc())bad=['area','Informe a área construída em m².'];
else if(d.nome.length<2)bad=['l-nome','Informe o seu nome.'];
else if(d.whatsapp.replace(/\\D/g,'').length<10)bad=['l-fone','Informe o WhatsApp com DDD.'];
else if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(d.email))bad=['l-mail','Informe um e-mail válido.'];
else if(d.cidade.length<2)bad=['l-cid','Informe a cidade da obra.'];
else if(!$('l-ok').checked)bad=['l-ok','Marque a autorização de contato.'];
[].forEach.call(lf.querySelectorAll('.err'),function(x){x.classList.remove('err')});
if(bad){$(bad[0]).classList.add('err');$(bad[0]).focus();lh.textContent=bad[1];return}
lh.textContent='';S.d=d;var url=msg();$('wa').href=url;
abre();try{localStorage.setItem('l-inss-ok','1')}catch(e){}
var t=$('lead-t');
if(LD&&LD.url){
var reg={nome:d.nome,whatsapp:d.whatsapp,email:d.email,cidade:d.cidade,uf:uf.value,area:String(S.a),sistema:NOME[S.sis],fase:d.fase,estimativa:brl(S.v),avisos:d.avisos};
try{if(LD.tipo==='json'){fetch(LD.url,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(reg)}).catch(function(){})}
else{var fd=new FormData();for(var k in LD.campos){if(LD.campos[k])fd.append(LD.campos[k],reg[k]||'')}fetch(LD.url,{method:'POST',mode:'no-cors',body:fd}).catch(function(){})}}catch(e){}
t.innerHTML='<b>Simulação registrada.</b> Retorno pelo seu WhatsApp.'}
else{var w=null;try{w=window.open(url,'_blank')}catch(e){}
if(w){try{w.opener=null}catch(e){}}
t.innerHTML=w?'O WhatsApp abriu com a sua simulação. <b>É só enviar a mensagem.</b>':'<b>Falta um toque:</b> envie a simulação pelo botão abaixo.'}
$('lead-ok').hidden=false;$('out').scrollIntoView({block:'nearest'});
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
        'AREA': str(AREA), 'INSS_ALV': brl(INSS_ALV), 'ECON': brl(ECON), 'VAU_MES': VAUS['rotulo'], 'UF_OPTS': opts,
        'VAU_JSON': json.dumps({k: round(v, 2) for k, v in VAU_UF.items()}), 'UFN_JSON': json.dumps({k: n for k, n in UFS if k in VAU_UF}, ensure_ascii=False),
        'ALIQ': repr(ALIQ), 'P_ALV': repr(P_ALV), 'RED_PRE': repr(RED_PRE), 'RED_MISTA': repr(round(1 - P_MISTA / P_ALV, 4)), 'EQ1': repr(EQ_ATE_1000), 'EQ2': repr(EQ_ACIMA),
        'WHATS': WHATS, 'LEADS_JSON': json.dumps(LEADS if LEADS['url'] else None),
        'BTN': 'Ver o INSS da minha obra' if LEADS['url'] else 'Ver o resultado e receber no WhatsApp',
        'MSG_OUTRA': quote('Olá Gustavo, quero uma simulação do INSS de uma obra comercial, multifamiliar ou reforma.'),
        'FAQ': '\n'.join('<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in FAQ),
        'MAPA': mapa_obras(), 'IMG': img[0], 'IMGW': str(img[1]), 'IMGH': str(img[2]),
    }
    out = _BODY
    for k, v in rep.items(): out = out.replace('[[%s]]' % k, v)
    assert '[[' not in out, out[out.index('[['):][:60]
    return out + FAQ_LD
