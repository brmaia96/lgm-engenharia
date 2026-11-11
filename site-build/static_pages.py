SOBRE_BODY = '''<main>
<section class="col phead who"><div><p class="crumb">sobre</p>
<h1>Engenharia tributária e aço leve, <b>com a mesma assinatura.</b></h1>
<p class="lead" style="margin-top:26px">Steel frame desde 2018, <b>em canteiro, dentro de construtora.</b> Hoje o projeto, a estrutura e o INSS da obra saem do mesmo escritório.</p></div>
<figure><img src="img/retrato.jpg" width="1100" height="1468" alt="Retrato de Luis Gustavo Maia"><figcaption class="cap"><b>Luis Gustavo Maia</b><span>engenheiro civil, CREA-SP 5071068977</span></figcaption></figure></section>

<section class="band sec-s"><h2 class="tag">Trajetória</h2>
<dl class="tl">
<div><dt>2018</dt><dd>Estágio em construtora de steel frame</dd></div>
<div><dt>2020</dt><dd>Formação em engenharia civil e entrada em administradora de obras em steel frame</dd></div>
<div><dt>2022</dt><dd>Engenheiro em construtora de steel frame</dd></div>
<div><dt>2023</dt><dd>Início da operação própria</dd></div>
<div><dt>2026</dt><dd>Dedicação integral ao escritório</dd></div>
</dl></section>

<section class="band sec"><h2 class="tag">O que entrego</h2>
<div class="list">
<div><h3>INSS e CNO da obra</h3><p>Cadastro, enquadramento e regularização para a obra não pagar contribuição a mais.</p></div>
<div><h3>Projeto executivo em steel frame</h3><p>Painéis, tesouras, plano de corte e caderno de montagem. O montador não interpreta, monta.</p></div>
<div><h3>Projetos complementares</h3><p>Fundação, elétrica e hidráulica compatibilizadas com a estrutura no mesmo modelo.</p></div>
<div><h3>Acompanhamento de obra</h3><p>Do radier à cobertura, com a mesma responsabilidade técnica do projeto.</p></div>
</div></section>

</main>'''

# Página de agenda. AGENDA_URL: link da página de agendamento do Google Agenda (quando existir, vira o botão principal).
AGENDA_URL = ''
# E-mail que entra como convidado no evento do Google Agenda (uso autorizado pelo cliente).
AGENDA_EMAIL = 'engmaia1996@gmail.com'
def agenda_body():
    top = ('<p style="margin-top:34px"><a class="btn" href="%s" target="_blank" rel="noopener">Ver horários livres na agenda</a></p>' % AGENDA_URL) if AGENDA_URL else ''
    return '''<main>
<section class="col phead"><p class="crumb">agenda</p>
<h1>Marque uma reunião.</h1>
<p class="lead" style="margin-top:26px">Trinta minutos por vídeo, <b>para entender o terreno, o projeto ou o INSS da obra.</b></p>''' + top + '''</section>

<section class="band sec-s"><h2 class="tag">Sugira um horário</h2><div>
<form id="ag" method="post" novalidate>
<div class="calc four">
<div><label for="ag-nome">Seu nome</label><input id="ag-nome" name="nome" type="text" autocomplete="name" autocapitalize="words" placeholder="Nome e sobrenome" aria-describedby="ag-h"><p class="hint" id="ag-h" role="alert"></p></div>
<div><label for="ag-ass">Assunto</label><select id="ag-ass" name="assunto"><option>INSS e CNO da obra</option><option>Projeto em steel frame</option><option>Projeto e INSS</option><option>Outro assunto</option></select></div>
<div><label for="ag-dia">Dia</label><select id="ag-dia" name="dia"></select></div>
<div><label for="ag-hora">Horário de Brasília</label><select id="ag-hora" name="hora"><option>09:00</option><option>10:00</option><option>11:00</option><option>14:00</option><option>15:00</option><option>16:00</option><option>17:00</option></select></div>
</div>
<div class="acts"><button class="btn" type="submit" data-via="gc">Pedir pelo Google Agenda</button><button class="lnk" type="submit" data-via="wa">Pedir pelo WhatsApp</button></div>
</form>
<div class="out" id="ag-out" tabindex="-1" aria-labelledby="ag-t" hidden>
<h3 class="meta" id="ag-t"></h3>
<div class="num" id="ag-res" style="font-size:clamp(26px,3vw,40px);line-height:1.25;margin-block:6px 20px"></div>
<p id="ag-p"></p>
<p class="links" style="margin-top:20px;max-width:none"><a class="lnk" id="ag-de" href="https://calendar.google.com/" target="_blank" rel="noopener">Abrir de novo</a></p>
</div>
</div></section>

<section class="band sec"><h2 class="tag">Como funciona</h2>
<ol class="tl ol">
<li>Você sugere o dia e o horário e envia o pedido pelo Google Agenda ou pelo WhatsApp.</li>
<li>O pedido chega a mim. Eu confirmo e envio o link do Google Meet.</li>
<li>Na conversa, vemos o terreno, o projeto e o INSS da obra. Depois você recebe a proposta.</li>
</ol></section>

<section class="band sec"><h2 class="tag">Contato direto</h2>
<dl class="tl">
<div><dt>WhatsApp</dt><dd><a href="https://wa.me/5514991850799" target="_blank" rel="noopener">(14) 99185-0799</a></dd></div>
<div><dt>Instagram</dt><dd><a href="https://www.instagram.com/eng.gustavomaia/" target="_blank" rel="noopener">@eng.gustavomaia</a></dd></div>
</dl></section>
</main>
<script>(function(){var f=document.getElementById('ag');if(!f)return;function $(i){return document.getElementById(i)}
var dia=$('ag-dia'),nome=$('ag-nome'),h=$('ag-h'),out=$('ag-out'),via='gc';
/* dias úteis: sem fim de semana e sem feriado nacional (fixos, Carnaval, Sexta-feira Santa e Corpus Christi) */
function pascoa(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,g=Math.floor((b-Math.floor((b+8)/25)+1)/3),hh=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-hh-k)%7,m=Math.floor((a+11*hh+22*l)/451),n=hh+l-7*m+114;return new Date(y,Math.floor(n/31)-1,n%31+1,12)}
var FX={'0101':1,'2104':1,'0105':1,'0709':1,'1210':1,'0211':1,'1511':1,'2011':1,'2512':1};
function feriado(d){var dm=('0'+d.getDate()).slice(-2),mm=('0'+(d.getMonth()+1)).slice(-2);if(FX[dm+mm])return true;var n=Math.round((d-pascoa(d.getFullYear()))/864e5);return n===-48||n===-47||n===-2||n===60}
var DS=['domingo','segunda','terça','quarta','quinta','sexta','sábado'],d=new Date();d.setHours(12,0,0,0);var n=0;
while(n<10){d.setDate(d.getDate()+1);var w=d.getDay();if(w===0||w===6||feriado(d))continue;var o=document.createElement('option');
var dm=('0'+d.getDate()).slice(-2),mm=('0'+(d.getMonth()+1)).slice(-2);o.textContent=DS[w]+', '+dm+'/'+mm;o.value=''+d.getFullYear()+mm+dm;dia.appendChild(o);n++}
nome.addEventListener('input',function(){nome.classList.remove('err');nome.removeAttribute('aria-invalid');h.textContent=''});
[].forEach.call(f.querySelectorAll('button[type=submit]'),function(b){b.addEventListener('click',function(){via=b.getAttribute('data-via')})});
f.addEventListener('submit',function(ev){ev.preventDefault();var v=via;via='gc';var nm=nome.value.trim();
if(nm.length<2){nome.classList.add('err');nome.setAttribute('aria-invalid','true');h.textContent='Informe o seu nome.';nome.focus();out.hidden=true;return}
var a=$('ag-ass').value,dd=dia.options[dia.selectedIndex].textContent,iso=dia.value,hh=$('ag-hora').value;
var h1=hh.replace(':','')+'00',h2=hh.slice(0,2)+'3000',url,tit,txt,de;
if(v==='wa'){var m=['Olá Gustavo, quero marcar uma reunião.','','Nome: '+nm,'Assunto: '+a,'Dia: '+dd,'Horário: '+hh+' (Brasília)','','Pode confirmar?'];
url='https://wa.me/5514991850799?text='+encodeURIComponent(m.join('\\n'));tit='Falta enviar a mensagem';de='Abrir o WhatsApp de novo';
txt='O WhatsApp abriu com o pedido. <b>Envie a mensagem: eu confirmo por lá.</b>'}
else{url='https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent('Reunião com Luis Gustavo Maia: '+a)+'&dates='+iso+'T'+h1+'/'+iso+'T'+h2+'&ctz=America/Sao_Paulo&details='+encodeURIComponent('Reunião por vídeo, 30 minutos.\\nNome: '+nm+'\\nAssunto: '+a+'\\nMarcada pelo site.')+'&location='+encodeURIComponent('Google Meet')+'&add='+encodeURIComponent('__EMAIL__');
tit='Falta salvar o evento';de='Abrir o Google Agenda de novo';
txt='O Google Agenda abriu com a reunião. <b>Salve e envie o convite: é assim que o pedido chega a mim.</b> Eu confirmo com o link do Google Meet.'}
var win=null;try{win=window.open(url,'_blank')}catch(x){}
if(win){try{win.opener=null}catch(x){}}else{tit='Falta um toque';de=v==='wa'?'Abrir o WhatsApp':'Abrir o Google Agenda';txt=v==='wa'?'<b>Abra o WhatsApp e envie a mensagem:</b> eu confirmo por lá.':'<b>Abra o Google Agenda, salve o evento e envie o convite:</b> é assim que o pedido chega a mim.'}
$('ag-t').textContent=tit;$('ag-res').textContent=dd+', às '+hh;$('ag-p').innerHTML=txt;var l=$('ag-de');l.href=url;l.textContent=de;
out.hidden=false;try{out.focus({preventScroll:true})}catch(x){out.focus()}out.scrollIntoView({block:'nearest'})});})();</script>'''.replace('__EMAIL__',AGENDA_EMAIL)
