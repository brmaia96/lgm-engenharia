INSS_BODY = '''<main>
<section class="col phead"><p class="crumb">engenharia tributária</p>
<h1>A obra paga INSS. <b>Quase sempre a mais.</b></h1>
<p class="lead" style="margin-top:26px">Sem planejamento, a Receita Federal calcula a contribuição pela área construída. Com a obra enquadrada e as notas certas, <b>a base de cálculo cai.</b></p></section>

<section class="band sec-s"><div class="tag"><b>Exemplo de obra</b></div><div>
<h2>Casa de 150 m² em steel frame</h2>
<div class="nums" style="margin-top:34px">
<div><div class="num off">R$ 8.832</div><div class="nl">aferição indireta, sem planejamento</div></div>
<div><div class="num">R$ 2.650</div><div class="nl">com enquadramento e notas corretas</div></div>
<div><div class="num sv">R$ 6.182</div><div class="nl">de volta ao orçamento da obra</div></div>
</div>
<h3 style="margin-top:64px">Memória de cálculo</h3>
<dl class="memo" style="margin-top:16px">
<div><dt>Custo da obra por aferição</dt><span class="f">150 m² × R$ 2.000</span><dd>R$ 300.000</dd></div>
<div><dt>Mão de obra presumida, obra cadastrada como alvenaria</dt><span class="f">20%</span><dd>R$ 60.000</dd></div>
<div><dt>Fator social, até 200 m²</dt><span class="f">40%</span><dd>R$ 24.000</dd></div>
<div class="res"><dt>Contribuição devida</dt><span class="f">36,8%</span><dd>R$ 8.832</dd></div>
<div><dt>Redução por pré-fabricado</dt><span class="f">70%</span><dd>− R$ 6.182</dd></div>
<div class="res"><dt>Contribuição com planejamento</dt><span class="f"></span><dd>R$ 2.650</dd></div>
</dl>
</div></section>

<section class="band sec"><div class="tag"><b>Simulador</b></div><div>
<h2>Quanto a Receita cobraria da sua obra?</h2>
<form id="f" novalidate style="margin-top:34px">
<div class="calc">
<div><label for="area">Área construída (m²)</label><input id="area" type="number" inputmode="decimal" min="1" step="1" placeholder="150" aria-describedby="area-h"><p class="hint" id="area-h" role="alert"></p></div>
<div><label for="sis">Sistema construtivo</label><select id="sis">
<option value="alv">Alvenaria</option><option value="sf">Steel frame</option><option value="wf">Wood frame</option><option value="mod">Modular ou pré-fabricado</option></select></div>
<div><label for="cid">Cidade</label><input id="cid" type="text" placeholder="Marília, SP" autocomplete="address-level2"></div>
</div>
<button class="btn" type="submit">Gerar simulação</button>
</form>
<div class="out" id="out" hidden aria-live="polite">
<p class="meta">Aferição indireta estimada</p>
<div class="num" id="val"></div>
<p>É o que a Receita cobra quando a obra não tem planejamento tributário. <b>Com o enquadramento certo, esse valor cai.</b></p>
<p style="margin-top:30px"><a class="lnk" id="wa" href="https://wa.me/5514991850799" target="_blank" rel="noopener">Simular a redução com o especialista</a></p>
</div>
</div></section>

<section class="band sec"><div class="tag"><b>Sistemas industrializados</b></div><div>
<div class="sys">
<div><h2>Steel framing</h2><p>Painéis de aço galvanizado. <b>Feitos em fábrica e montados na obra</b>, podem entrar como pré-fabricado.</p><span class="k">15% como obra mista, ou pré-fabricado com redução de 70%</span></div>
<div><h2>Wood framing</h2><p>Estrutura em madeira tratada, painelizada. A regra trata como obra de madeira ou mista.</p><span class="k">mão de obra presumida de 15%, em vez de 20%</span></div>
<div><h2>Construção modular</h2><p>Módulos prontos de fábrica. <b>Com notas do fabricante acima de 40% do custo da obra</b>, a base de cálculo cai.</p><span class="k">redução de 70% na base</span></div>
</div>
<p class="src" style="margin-top:56px">Estimativa para pessoa física, obra nova residencial, sem decadência. Cálculo conforme o Manual do Sero v3.0, da Receita Federal (ago/2024), com VAU de referência de R$ 2.000/m². O manual não cita steel frame, wood frame ou modular pelo nome: o enquadramento como pré-fabricado depende das notas fiscais e do cadastro da obra, e é confirmado caso a caso na simulação com o especialista.</p>
</div></section>
</main>
<script>(function(){var VAU=2000,ALIQ=0.368,PCT={alv:.20,sf:.15,wf:.15,mod:.15},NOME={alv:'Alvenaria',sf:'Steel frame',wf:'Wood frame',mod:'Modular ou pré-fabricado'};
function fs(a){return a<=100?.20:a<=200?.40:a<=300?.55:a<=400?.70:.90}
var f=document.getElementById('f'),ar=document.getElementById('area'),h=document.getElementById('area-h'),out=document.getElementById('out');
function brl(v){return 'R$ '+Math.round(v).toLocaleString('pt-BR')}
ar.addEventListener('input',function(){ar.classList.remove('err');h.textContent=''});
f.addEventListener('submit',function(ev){ev.preventDefault();var a=parseFloat(String(ar.value).replace(',','.'));
if(!(a>0)){ar.classList.add('err');h.textContent='Informe a área construída em m².';ar.focus();out.hidden=true;return}
var s=document.getElementById('sis').value,c=document.getElementById('cid').value.trim(),v=a*VAU*PCT[s]*fs(a)*ALIQ;
document.getElementById('val').textContent=brl(v);
var m=['Olá Gustavo, fiz a simulação de INSS no site.','','Área: '+a.toLocaleString('pt-BR')+' m²','Sistema: '+NOME[s]];if(c)m.push('Cidade: '+c);
m.push('Aferição indireta estimada: '+brl(v),'','Quero simular a redução com o especialista.');
document.getElementById('wa').href='https://wa.me/5514991850799?text='+encodeURIComponent(m.join('\\n'));
out.hidden=false;out.scrollIntoView({behavior:'smooth',block:'nearest'})});})();</script>'''

SOBRE_BODY = '''<main>
<section class="col phead who"><div><p class="crumb">sobre</p>
<h1>Oito anos em aço leve.</h1>
<p class="lead" style="margin-top:26px">Steel frame desde 2018, <b>em canteiro, dentro de construtora.</b> Hoje o projeto, a estrutura e a engenharia tributária da obra saem com a mesma assinatura.</p></div>
<figure><img src="img/retrato.jpg" width="1100" height="1468" alt="Retrato de Luis Gustavo Maia"><figcaption class="cap"><b>Luis Gustavo Maia</b><span>engenheiro civil</span></figcaption></figure></section>

<section class="band sec-s"><div class="tag"><b>Trajetória</b></div>
<dl class="tl">
<div><dt>2018</dt><dd>Estágio em construtora de steel frame</dd></div>
<div><dt>2020</dt><dd>Formação em engenharia civil e entrada em administradora de obras em steel frame</dd></div>
<div><dt>2022</dt><dd>Engenheiro em construtora de steel frame</dd></div>
<div><dt>2023</dt><dd>Início da operação própria</dd></div>
<div><dt>2026</dt><dd>Dedicação integral ao escritório</dd></div>
</dl></section>

<section class="band sec"><div class="tag"><b>O que entrego</b></div>
<div class="list">
<div><h3>Projeto executivo em steel frame</h3><p>Painéis, tesouras, plano de corte e caderno de montagem. O montador não interpreta, monta.</p></div>
<div><h3>Projetos complementares</h3><p>Fundação, elétrica e hidráulica compatibilizadas com a estrutura no mesmo modelo.</p></div>
<div><h3>Acompanhamento de obra</h3><p>Do radier à cobertura, com a mesma responsabilidade técnica do projeto.</p></div>
<div><h3>INSS e CNO da obra</h3><p>Cadastro, enquadramento e regularização para a obra não pagar contribuição a mais.</p></div>
</div></section>

<section class="band sec"><div class="tag"><b>Registro</b></div>
<dl class="tl">
<div><dt>CREA-SP</dt><dd>5071068977</dd></div>
<div><dt>Base</dt><dd>Marília, SP. Projetos em todo o Brasil</dd></div>
</dl></section>
</main>'''
