(function(){
/* comparador estrutura x pronta */
var c=document.getElementById('cmp');
if(c){var r=c.querySelector('input'),d=false;
function set(p){p=Math.max(0,Math.min(100,p));c.style.setProperty('--p',p+'%');r.value=Math.round(p);c.classList.toggle('nl',p<10);c.classList.toggle('nr',p>90)}
function at(e){var b=c.getBoundingClientRect();set((e.clientX-b.left)/b.width*100)}
c.addEventListener('pointerdown',function(e){d=true;try{c.setPointerCapture(e.pointerId)}catch(x){}at(e)});
c.addEventListener('pointermove',function(e){if(d||e.pointerType==='mouse')at(e)});
c.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'&&!d)at(e)});
['pointerup','pointercancel'].forEach(function(n){c.addEventListener(n,function(){d=false})});
r.addEventListener('input',function(){set(+r.value)});}

/* vídeo de apresentação */
var v=document.getElementById('vid'),vb=document.getElementById('vbtn');
if(v&&vb){var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function lab(){vb.textContent=v.paused?'reproduzir':'pausar'}
if(rm){v.removeAttribute('autoplay');v.pause()}else{var pr=v.play();if(pr&&pr.catch)pr.catch(function(){lab()})}
vb.addEventListener('click',function(){if(v.paused){var q=v.play();if(q&&q.catch)q.catch(function(){})}else v.pause()});
v.addEventListener('play',lab);v.addEventListener('pause',lab);lab();}

/* filtro de obras */
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
var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;sx=null;if(Math.abs(dx)>50)show(i+(dx<0?1:-1))},{passive:true});}
})();
