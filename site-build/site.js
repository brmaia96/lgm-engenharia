(function(){
/* filme de apresentação: mudo, toca sozinho quando entra na tela e para quando sai; pausa e som ficam na linha da legenda */
var v=document.getElementById('vid'),vb=document.getElementById('vbtn');
if(v&&vb){var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,quer=!rm;
function lab(){vb.textContent=v.paused?'reproduzir':'pausar'}
function toca(){var q=v.play();if(q&&q.catch)q.catch(function(){lab()})}
vb.addEventListener('click',function(){if(v.paused){quer=true;toca()}else{quer=false;v.pause()}});
v.addEventListener('play',lab);v.addEventListener('pause',lab);lab();
var vs=document.getElementById('vsnd');
if(vs)vs.addEventListener('click',function(){v.muted=!v.muted;vs.textContent=v.muted?'ativar som':'tirar som';if(!v.muted&&v.paused){quer=true;toca()}});
if('IntersectionObserver' in window){new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting&&x.intersectionRatio>=.4){if(quer&&v.paused)toca()}else if(!v.paused)v.pause()})},{threshold:[0,.4]}).observe(v)}
else if(quer)toca()}

/* filtro de obras e de artigos */
var f=document.getElementById('flt');
if(f){var cards=[].slice.call(document.querySelectorAll('#grid [data-cat]')),st=document.getElementById('flt-st');
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=b.getAttribute('data-k'),n=0;
[].forEach.call(f.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
cards.forEach(function(x){var on=k==='*'||x.getAttribute('data-cat')===k;x.hidden=!on;if(on)n++});
var g=document.getElementById('grid');if(g)g.classList.toggle('on',k!=='*');if(st)st.textContent=n+' '+(n===1?(f.getAttribute('data-one')||'obra'):(f.getAttribute('data-many')||'obras'));});}

/* galeria ampliada */
var zs=[].slice.call(document.querySelectorAll('.gal .z')),lb=document.getElementById('lb');
if(zs.length&&lb&&lb.showModal){var im=lb.querySelector('img'),nn=lb.querySelector('.n'),cb=lb.querySelector('footer b'),cs=lb.querySelector('footer span'),i=0,from=null;
function show(k){i=(k+zs.length)%zs.length;var a=zs[i],t=a.querySelector('img');im.src=a.getAttribute('href');im.alt=t?t.alt:'';
nn.textContent=(i+1)+' / '+zs.length;cb.textContent=a.getAttribute('data-b')||'';cs.textContent=a.getAttribute('data-s')||'';
var nx=zs[(i+1)%zs.length];if(nx){var pre=new Image();pre.src=nx.getAttribute('href')}}
zs.forEach(function(a,k){a.addEventListener('click',function(e){e.preventDefault();from=a;show(k);lb.showModal()})});
lb.querySelector('.x').addEventListener('click',function(){lb.close()});
lb.querySelector('.p').addEventListener('click',function(){show(i-1)});
lb.querySelector('.nx').addEventListener('click',function(){show(i+1)});
lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
lb.addEventListener('close',function(){if(from)from.focus()});
/* deslize troca de imagem; com dois dedos ou com a tela ampliada, não (quem abre os dedos quer ver o detalhe) */
var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches.length>1?null:e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(sx===null||e.touches.length>0||(window.visualViewport&&visualViewport.scale>1.01)){sx=null;return}
var dx=e.changedTouches[0].clientX-sx;sx=null;if(Math.abs(dx)>50)show(i+(dx<0?1:-1))},{passive:true});}
})();
