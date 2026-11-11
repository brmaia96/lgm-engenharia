(function(){
/* filme de apresentação: começa sozinho, mudo (regra dos navegadores). O som entra no primeiro toque, clique ou tecla
   na página, com volume subindo devagar, a menos que a pessoa tenha escolhido "tirar som". Continua tocando ao rolar a página. */
var v=document.getElementById('vid'),vb=document.getElementById('vbtn');
if(v&&vb){var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,quer=!rm,escolheu=false,vs=document.getElementById('vsnd');
function lab(){vb.textContent=v.paused?'reproduzir':'pausar';if(vs)vs.textContent=v.muted?'ativar som':'tirar som'}
function toca(){var q=v.play();if(q&&q.catch)q.catch(function(){lab()})}
function sobe(){v.volume=0;var t0=null;function st(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1400);v.volume=.85*p;if(p<1)requestAnimationFrame(st)}requestAnimationFrame(st)}
function som(on){v.muted=!on;if(on){sobe();quer=true;if(v.paused)toca()}lab()}
if(rm){v.removeAttribute('autoplay');v.pause()}else toca();
vb.addEventListener('click',function(){if(v.paused){quer=true;toca()}else{quer=false;v.pause()}});
v.addEventListener('play',lab);v.addEventListener('pause',lab);v.addEventListener('volumechange',lab);lab();
if(vs)vs.addEventListener('click',function(ev){ev.stopPropagation();escolheu=true;som(v.muted)});
function primeiro(ev){if(ev.target===vs||ev.target===vb)return;document.removeEventListener('pointerdown',primeiro,true);document.removeEventListener('keydown',primeiro,true);
if(!escolheu&&!rm&&v.muted){var r=v.getBoundingClientRect();som(true)}}
document.addEventListener('pointerdown',primeiro,true);document.addEventListener('keydown',primeiro,true);
if('IntersectionObserver' in window){new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting&&quer&&v.paused)toca()})},{threshold:[0]}).observe(v)}   /* não pausa ao rolar a página (pedido do cliente) */
/* se o navegador segurou o play (modo econômico do celular), o primeiro toque em qualquer lugar da página dá o play */
v.addEventListener('loadeddata',function(){if(quer&&v.paused)toca()});}

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
