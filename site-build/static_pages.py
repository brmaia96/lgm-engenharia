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
<div class="gal" style="margin-bottom:var(--sp1)">
<figure class="half night"><a class="z" href="img/marca/estrutura.jpg" data-b="Light steel frame" data-s="perfis de aço galvanizado"><img src="img/marca/estrutura.jpg" width="1024" height="1087" alt="Estrutura de uma casa de dois pavimentos em light steel frame" loading="lazy" decoding="async" style="object-position:50% 40%"></a><figcaption class="cap"><b>Light steel frame</b><span>perfis de aço galvanizado</span></figcaption></figure>
<figure class="half night"><a class="z" href="img/marca/detalhe.jpg" data-b="Ligação" data-s="montante, guia e parafusos"><img src="img/marca/detalhe.jpg" width="1122" height="1402" alt="Detalhe da ligação entre montante e guia de aço galvanizado" loading="lazy" decoding="async"></a><figcaption class="cap"><b>Ligação</b><span>montante, guia e parafusos</span></figcaption></figure>
</div>
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

# Página de agenda. AGENDA_URL: link da página de agendamento do Google Agenda (quando existir, vira o botão principal).
AGENDA_URL = ''
# E-mail que entra como convidado no evento do Google Agenda (uso autorizado pelo cliente).
AGENDA_EMAIL = 'engmaia1996@gmail.com'
def agenda_body():
    top = ('<p style="margin-top:34px"><a class="btn" style="margin-top:0" href="%s" target="_blank" rel="noopener">Ver horários livres na agenda</a></p>' % AGENDA_URL) if AGENDA_URL else ''
    return '''<main>
<section class="col phead"><p class="crumb">agenda</p>
<h1>Marque uma reunião.</h1>
<p class="lead" style="margin-top:26px">Trinta minutos por vídeo, <b>para entender o terreno, o projeto ou o INSS da obra.</b></p>''' + top + '''</section>

<section class="band sec-s"><div class="tag"><b>Escolha o horário</b></div><div>
<form id="ag" novalidate>
<div class="calc four">
<div><label for="ag-nome">Seu nome</label><input id="ag-nome" type="text" autocomplete="name" placeholder="Nome e sobrenome" aria-describedby="ag-h"><p class="hint" id="ag-h" role="alert"></p></div>
<div><label for="ag-ass">Assunto</label><select id="ag-ass"><option>Projeto em steel frame</option><option>INSS e CNO da obra</option><option>Projeto e INSS</option><option>Outro assunto</option></select></div>
<div><label for="ag-dia">Dia</label><select id="ag-dia"></select></div>
<div><label for="ag-hora">Horário de Brasília</label><select id="ag-hora"><option>09:00</option><option>10:00</option><option>11:00</option><option>14:00</option><option>15:00</option><option>16:00</option><option>17:00</option></select></div>
</div>
<button class="btn" type="submit">Pedir este horário</button>
</form>
<div class="out" id="ag-out" hidden aria-live="polite">
<p class="meta">Seu pedido</p>
<div class="num" id="ag-res" style="font-size:clamp(26px,3vw,40px);line-height:1.25"></div>
<p>Adicione ao seu Google Agenda: <b>o convite chega na minha agenda e eu confirmo com o link do Google Meet.</b> Se preferir, envie o pedido pelo WhatsApp.</p>
<p class="links" style="display:flex;flex-wrap:wrap;gap:10px 44px;margin-top:30px;max-width:none"><a class="lnk" id="ag-gc" href="https://calendar.google.com/" target="_blank" rel="noopener">Adicionar ao Google Agenda</a><a class="lnk" id="ag-wa" href="https://wa.me/5514991850799" target="_blank" rel="noopener">Enviar pedido pelo WhatsApp</a></p>
</div>
</div></section>

<section class="band sec"><div class="tag"><b>Como funciona</b></div>
<dl class="tl">
<div><dt>1</dt><dd>Você escolhe o dia e o horário e adiciona a reunião ao seu Google Agenda.</dd></div>
<div><dt>2</dt><dd>O convite entra na minha agenda. Eu confirmo e envio o link do Google Meet.</dd></div>
<div><dt>3</dt><dd>Na conversa, vemos o terreno, o projeto e o INSS da obra. Depois você recebe a proposta.</dd></div>
</dl></section>

<section class="band sec"><div class="tag"><b>Contato direto</b></div>
<dl class="tl">
<div><dt>WhatsApp</dt><dd><a href="https://wa.me/5514991850799" target="_blank" rel="noopener">(14) 99185-0799</a></dd></div>
<div><dt>Instagram</dt><dd><a href="https://www.instagram.com/eng.gustavomaia/" target="_blank" rel="noopener">@eng.gustavomaia</a></dd></div>
<div><dt>Base</dt><dd>Marília, SP. Projetos em todo o Brasil</dd></div>
</dl></section>
</main>
<script>(function(){var f=document.getElementById('ag');if(!f)return;var dia=document.getElementById('ag-dia'),nome=document.getElementById('ag-nome'),h=document.getElementById('ag-h'),out=document.getElementById('ag-out');
var DS=['domingo','segunda','terça','quarta','quinta','sexta','sábado'],d=new Date();d.setHours(12,0,0,0);var n=0;
while(n<10){d.setDate(d.getDate()+1);var w=d.getDay();if(w===0||w===6)continue;var o=document.createElement('option');
var dm=('0'+d.getDate()).slice(-2),mm=('0'+(d.getMonth()+1)).slice(-2);o.textContent=DS[w]+', '+dm+'/'+mm;o.value=''+d.getFullYear()+mm+dm;dia.appendChild(o);n++}
nome.addEventListener('input',function(){nome.classList.remove('err');h.textContent=''});
f.addEventListener('submit',function(ev){ev.preventDefault();var nm=nome.value.trim();
if(nm.length<2){nome.classList.add('err');h.textContent='Informe seu nome.';nome.focus();out.hidden=true;return}
var a=document.getElementById('ag-ass').value,dd=dia.options[dia.selectedIndex].textContent,iso=dia.value,hh=document.getElementById('ag-hora').value;
var h1=hh.replace(':','')+'00',h2=hh.slice(0,2)+'3000';
document.getElementById('ag-gc').href='https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent('Reunião com Luis Gustavo Maia: '+a)+'&dates='+iso+'T'+h1+'/'+iso+'T'+h2+'&ctz=America/Sao_Paulo&details='+encodeURIComponent('Reunião por vídeo, 30 minutos.\\nNome: '+nm+'\\nAssunto: '+a+'\\nMarcada pelo site.')+'&location='+encodeURIComponent('Google Meet')+'&add='+encodeURIComponent('__EMAIL__');
document.getElementById('ag-res').textContent=dd+', às '+hh;
var m=['Olá Gustavo, quero marcar uma reunião.','','Nome: '+nm,'Assunto: '+a,'Dia: '+dd,'Horário: '+hh+' (Brasília)','','Pode confirmar?'];
document.getElementById('ag-wa').href='https://wa.me/5514991850799?text='+encodeURIComponent(m.join('\\n'));
out.hidden=false;out.scrollIntoView({behavior:'smooth',block:'nearest'})});})();</script>'''.replace('__EMAIL__',AGENDA_EMAIL)
