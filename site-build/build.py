# Gera o site L. Engenharia em scratchpad/site a partir de build/data.py
import os, shutil, sys, html, urllib.parse, importlib.util
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import grade as G
S='/tmp/claude-0/-home-user-lgm-engenharia/49376ed1-2cbe-5161-a523-12fb37b2af57/scratchpad'
A=S+'/assets'; B=S+'/build'; OUT=os.environ.get('SITE_OUT',S+'/site'); AUX=OUT if os.environ.get('SITE_OUT') else B
spec=importlib.util.spec_from_file_location('data',os.environ.get('SITE_DATA',B+'/data.py')); D=importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
P=D.PROJECTS
WA='https://wa.me/5514991850799'
e=html.escape
def wa(msg): return WA+'?text='+urllib.parse.quote(msg)

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT+'/img')
FILES={}   # published path -> source path (relative to OUT)
def reg(p): FILES[p]=p

def treat(im,fam,mono=False,expo=True):
    if fam=='b': return G.ink(im,G.PAPER if mono else G.PANEL)
    if fam=='c': return G.duotone(im,invert=True) if mono else G.model(im)
    a=G.grade_a(im,expo=expo)
    return G.duotone(a) if mono else a
def put(src, dst, maxw=1800, crop=None, ratio=None, focus=(.5,.5), q=80, pad=None, fam='a', mono=False, expo=True):
    """resize/crop one image into site/img; returns (path,w,h)"""
    im=Image.open(src).convert('RGB')
    if crop:
        W,H=im.size; im=im.crop((int(crop[0]*W),int(crop[1]*H),int(crop[2]*W),int(crop[3]*H)))
    if pad:
        im=G.ink(im,G.PAPER); cw,ch=1200,900; cv=Image.new('RGB',(cw,ch),tuple(int(round(x*255)) for x in G.PAPER)); k=min(cw*.82/im.width,ch*.82/im.height)
        im2=im.resize((int(im.width*k),int(im.height*k)),Image.LANCZOS); cv.paste(im2,((cw-im2.width)//2,(ch-im2.height)//2)); im=cv; ratio=None; fam=None
    if ratio:
        W,H=im.size; tw,th=(W,int(round(W/ratio))) if W/H<ratio else (int(round(H*ratio)),H)
        x=int(round((W-tw)*focus[0])); y=int(round((H-th)*focus[1])); im=im.crop((x,y,x+tw,y+th))
    if im.width>maxw: im=im.resize((maxw,int(round(im.height*maxw/im.width))),Image.LANCZOS)
    if fam: im=treat(im,fam,mono,expo)
    os.makedirs(os.path.dirname(OUT+'/'+dst),exist_ok=True)
    im.save(OUT+'/'+dst,'JPEG',quality=q,optimize=True,progressive=True); reg(dst)
    return dst,im.width,im.height

FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Playfair+Display:ital@0;1&display=swap"><link rel="stylesheet" href="styles.css">'
def header(cur):
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if k==cur else '',t) for k,h,t in
        (('obras','obras.html','obras'),('inss','inss.html','inss'),('sobre','sobre.html','sobre'),('agenda','agenda.html','agenda')))
    return ('<header class="top col"><a class="mk" href="index.html" aria-label="L. Engenharia, início">L<i>.</i></a>'
            '<nav class="nav" aria-label="Páginas">%s</nav></header>')%nav
FOOT=('<footer class="col"><div class="ft">'
 '<div><b>Luis Gustavo Maia</b>Engenheiro civil<br>CREA-SP 5071068977</div>'
 '<div><b>Contato</b><a href="agenda.html">Marcar reunião</a><br><a href="%s" target="_blank" rel="noopener">WhatsApp (14) 99185-0799</a><br><a href="https://www.instagram.com/eng.gustavomaia/" target="_blank" rel="noopener">Instagram @eng.gustavomaia</a></div>'
 '<div><b>Atendimento</b>Marília, SP<br>Projetos em todo o Brasil</div>'
 '</div></footer>')%WA
def page(fn,title,cur,body,main=False):
    inner=header(cur)+body+FOOT+'<script src="site.js"></script>'
    if main:
        doc='<title>%s</title><meta name="claude:viewport-fit-sides" content="cover">%s<div lang="pt-BR">%s</div>\n'%(title,FONTS,inner)
    else:
        doc=('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
             '<title>%s</title>%s</head><body>%s</body></html>\n')%(title,FONTS,inner)
    open(OUT+'/'+fn,'w').write(doc)
    if not main: reg(fn)
    else:
        open(AUX+'/index.deploy.html','w').write(('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
          '<meta name="description" content="Luis Gustavo Maia, engenheiro civil. Projeto executivo em steel frame, projetos complementares e INSS de obra. Marília, SP, com atendimento em todo o Brasil.">'
          '<title>%s</title>%s</head><body>%s</body></html>\n')%(title,FONTS,inner))

def call(h2,msg,label='Conversar pelo WhatsApp'):
    return '<section class="col call"><h2>%s</h2><p class="links"><a class="lnk" href="agenda.html">Marcar reunião</a><a class="lnk" href="%s" target="_blank" rel="noopener">%s</a></p></section>'%(h2,wa(msg),label)

# ---------- imagens e cartões ----------
for p in P:
    s=p['slug']; base=A+'/'+p.get('assets',s)+'/'
    c=p['card']; ck=dict(maxw=1200,crop=c.get('crop'),ratio=4/3,focus=c.get('focus',(.5,.5)),q=78,pad=c.get('draw'),fam=c.get('fam','a'))
    p['_card']=put(base+c['src'],'img/%s/card.jpg'%s,**ck); p['_cardm']=put(base+c['src'],'img/%s/card-m.jpg'%s,mono=True,**ck)
    h=p['hero']; p['_hero']=put(base+h['src'],'img/%s/hero.jpg'%s,maxw=2200,crop=h.get('crop'),q=80,fam=h.get('fam','a'))
    if p is P[0]: p['_herom']=put(base+h['src'],'img/%s/hero-m.jpg'%s,maxw=2200,crop=h.get('crop'),q=80,fam=h.get('fam','a'),mono=True)
    n=0
    for sec in p['sections']:
        for it in sec['items']:
            n+=1; it['fam']=D.FAM.get(p.get('assets',s),{}).get(it['src'].split('/')[-1],'a'); it['_img']=put(base+it['src'],'img/%s/%02d.jpg'%(s,n),maxw=1900,crop=it.get('crop'),q=80,fam=it['fam'])
def sub(p): return p['sub']
def card(p,lazy=True,feat=False):
    src,w,h=p['_hero'] if feat else p['_card']; ms=(p['_herom'] if feat else p['_cardm'])[0]
    at=(' style="object-position:%s"'%p['hero'].get('pos','50% 50%') if feat else '')+(' loading="lazy" decoding="async"' if lazy else '')
    return ('<a class="card%s" href="o-%s.html" data-cat="%s"><span class="ph"><img src="%s" width="%d" height="%d" alt="%s"%s><img class="m" src="%s" width="%d" height="%d" alt="" aria-hidden="true"%s></span>'
            '<span class="cap"><b>%s</b><span>%s</span></span><span class="sub">%s</span></a>')%(
            ' feat' if feat else '',p['slug'],e(p['cat']),src,w,h,e(p['card'].get('alt',p['name'])),at,ms,w,h,at,e(p['name']),e(p['city']),e(sub(p)))

# ---------- páginas de projeto ----------
LB=('<dialog class="lb" id="lb" aria-label="Imagens do projeto"><header><span class="n"></span><button class="x" type="button">fechar</button></header>'
    '<div class="stage"><img alt=""><button class="nv p" type="button" aria-label="Imagem anterior"><span aria-hidden="true">&larr;</span></button>'
    '<button class="nv nx" type="button" aria-label="Próxima imagem"><span aria-hidden="true">&rarr;</span></button></div><footer><b></b><span></span></footer></dialog>')
for i,p in enumerate(P):
    hs,hw,hh=p['_hero']; H=p['hero']
    b='<main><section class="col phead"><p class="crumb"><a href="obras.html">obras</a> / %s</p><h1>%s</h1><p class="meta">%s</p></section>'%(e(p['cat_label']),e(p['name']),e(p['city']))
    if H.get('draw'): b+='<div class="wide herod %s"><img src="%s" width="%d" height="%d" alt="%s"></div>'%(H['draw'],hs,hw,hh,e(H['alt']))
    else: b+='<img class="wide hero" src="%s" width="%d" height="%d" alt="%s" style="object-position:%s">'%(hs,hw,hh,e(H['alt']),H.get('pos','50% 50%'))
    b+='<section class="col sec-s intro"><div class="txt"><p class="lead">%s</p>%s</div><dl class="ficha">%s</dl></section>'%(
        p['lead'],''.join('<p>%s</p>'%t for t in p.get('text',[])),''.join('<div><dt>%s</dt><dd>%s</dd></div>'%(e(k),v) for k,v in p['ficha']))
    for sec in p['sections']:
        g=''
        for it in sec['items']:
            src,w,h=it['_img']; cb,cs=it['cap']
            g+=('<figure class="%s%s"><a class="z"%s href="%s" data-b="%s" data-s="%s"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"%s></a>'
                '<figcaption class="cap"><b>%s</b><span>%s</span></figcaption></figure>')%(it.get('lay','full'),' night' if it['fam']=='c' else '',' style="aspect-ratio:%s"'%it['r'] if it.get('r') else '',src,e(cb),e(cs),src,w,h,e(it['alt']),
                ' style="object-position:%s"'%it['pos'] if it.get('pos') else '',e(cb),e(cs))
        b+='<section class="band sec"><div class="tag"><b>%s</b></div><div class="gal">%s</div></section>'%(e(sec['label']),g)
    pv=P[i-1]; nx=P[(i+1)%len(P)]
    b+='<nav class="col" aria-label="Outros projetos"><div class="pn"><a href="o-%s.html"><span>anterior</span><b>%s</b></a><a href="o-%s.html"><span>próximo</span><b>%s</b></a></div></nav>'%(pv['slug'],e(pv['name']),nx['slug'],e(nx['name']))
    b+=call('Um projeto parecido com este?','Olá Gustavo, vi %s no site e quero conversar sobre um projeto.'%p.get('ref',p['name']))
    b+='</main>'+LB
    page('o-%s.html'%p['slug'],'%s · L. Engenharia'%p['name'],'obras',b)

# ---------- obras ----------
cats=[]
for p in P:
    if p['cat'] not in [c[0] for c in cats]: cats.append((p['cat'],p['cat_plural']))
flt='<button type="button" data-k="*" aria-pressed="true">todas<sup>%d</sup></button>'%len(P)+''.join(
    '<button type="button" data-k="%s" aria-pressed="false">%s<sup>%d</sup></button>'%(e(k),e(l),sum(1 for p in P if p['cat']==k)) for k,l in cats)
b=('<main><section class="col phead"><h1>Obras</h1><p class="meta">%s</p><div class="flt" id="flt" role="group" aria-label="Filtrar por tipo">%s</div>'
   '<p class="sr" id="flt-st" aria-live="polite"></p></section><section class="col"><div class="grid three" id="grid">%s</div></section>%s</main>')%(
   e(D.OBRAS_META),flt,''.join(card(p,lazy=(k>1),feat=(k==0)) for k,p in enumerate(P)),
   call('Tem um terreno ou um projeto em andamento?','Olá Gustavo, vi as obras no site e quero conversar sobre um projeto.'))
page('obras.html','Obras · L. Engenharia','obras',b)

# ---------- home ----------
put(S+'/work/minas-estrutura.png','img/cmp/estrutura.jpg',maxw=2000,q=84,fam='c')
put(S+'/work/minas-pronta.png','img/cmp/pronta.jpg',maxw=2000,q=84)
M=A+'/marca/clean/'
OBRA=put(M+'obra-real.jpg','img/marca/obra-real.jpg',maxw=2000,q=82)
put(M+'estrutura-render.jpg','img/marca/estrutura.jpg',maxw=1400,q=84,fam='c')
put(M+'detalhe-ligacao.jpg','img/marca/detalhe.jpg',maxw=1400,q=84,fam='c')
sel=[p for p in P if p['slug'] in D.HOME_SELECT]; sel.sort(key=lambda p:D.HOME_SELECT.index(p['slug']))
os.makedirs(OUT+'/media',exist_ok=True); shutil.copy(S+'/video3/apresentacao.mp4',OUT+'/media/apresentacao.mp4'); reg('media/apresentacao.mp4')
put(S+'/video3/frames/f00105.jpg','img/video-poster.jpg',maxw=1920,q=84,fam=None)
put(S+'/portrait/retrato.jpg','img/retrato.jpg',maxw=1100,q=86,fam=None)
b=('<main><div class="wide vid"><video id="vid" src="media/apresentacao.mp4" poster="img/video-poster.jpg" width="1920" height="1080" muted loop playsinline autoplay preload="metadata" aria-label="Vídeo de apresentação de Luis Gustavo Maia, engenheiro civil: trajetória, o que faz, projetos e INSS de obra"></video>'
 '<button class="vbtn" id="vbtn" type="button">pausar</button></div>'
 '<div class="col"><div class="cap"><b>Luis Gustavo Maia</b><span>engenheiro civil · CREA-SP 5071068977</span></div></div>'
 '<section class="col sec-s"><h1>Projeto, execução e engenharia tributária, <b>com uma única responsabilidade técnica.</b></h1></section>'
 '<section class="band sec"><div class="tag"><b>Estrutura × pronta</b></div><div>'
 '<figure class="cmp" id="cmp" style="--p:50%%"><img src="img/cmp/pronta.jpg" width="2000" height="1125" alt="Casa Taquaraçu pronta, vista aérea com piscina" draggable="false">'
 '<img class="st" src="img/cmp/estrutura.jpg" width="2000" height="1125" alt="Estrutura em light steel frame da Casa Taquaraçu, sobre radier em pilares" draggable="false">'
 '<span class="tg l">estrutura</span><span class="tg r">pronta</span>'
 '<span class="bar" aria-hidden="true"><svg viewBox="0 0 44 16" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M9 2L3 8l6 6M35 2l6 6-6 6"/></svg></span>'
 '<input id="cmp-r" type="range" min="0" max="100" step="1" value="50" aria-label="Comparar a estrutura em steel frame e a casa pronta"></figure>'
 '<div class="cap">%s</div></div></section>'%D.CMP_CAPTION)
b+='<section class="band sec"><div class="tag"><b>Obras</b></div><div><div class="grid three">%s</div><p style="margin-top:44px"><a class="lnk" href="obras.html">Todas as obras</a></p></div></section>'%''.join(card(p) for p in sel)
b+=('<section class="col sec"><h2 style="font-size:clamp(26px,3vw,40px);line-height:1.22;letter-spacing:-.012em">Steel frame não é moda. <b>É engenharia.</b></h2></section>'
 '<img class="wide obra" src="%s" width="%d" height="%d" alt="Steel frame em obra: painéis de parede e treliças de entrepiso montados sobre a laje" loading="lazy" decoding="async">'
 '<div class="col"><div class="cap"><b>Steel frame em obra</b><span>painéis de parede e treliças de entrepiso</span></div></div>')%OBRA
b+=('<section class="band sec"><div class="tag"><b>Engenharia tributária</b></div><div><h2 style="max-width:20em">O INSS de uma casa de 150 m² em steel frame, <b>com e sem planejamento.</b></h2>'
 '<div class="nums" style="margin-top:36px"><div><div class="num off">R$ 8.832</div><div class="nl">aferição indireta, sem planejamento</div></div>'
 '<div><div class="num">R$ 2.650</div><div class="nl">com enquadramento e notas corretas</div></div>'
 '<div><div class="num sv">R$ 6.182</div><div class="nl">de volta ao orçamento da obra</div></div></div>'
 '<p style="margin-top:44px"><a class="lnk" href="inss.html">Simular o INSS da minha obra</a></p></div></section>')
b+=call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.')+'</main>'
page('index.html','L. Engenharia','home',b,main=True)

# ---------- inss e sobre ----------
page('inss.html','INSS de obra · L. Engenharia','inss',D.INSS_BODY+LB)
page('agenda.html','Marcar reunião · L. Engenharia','agenda',D.AGENDA_BODY)
page('sobre.html','Sobre · L. Engenharia','sobre',D.SOBRE_BODY+call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.'))
for f in ('styles.css','site.js'): shutil.copy(B+'/'+f,OUT+'/'+f); reg(f)
import json; json.dump(FILES,open(AUX+'/files.json','w'),indent=0)
tot=sum(os.path.getsize(OUT+'/'+f) for f in FILES)
print(len(FILES),'files',round(tot/1e6,1),'MB; largest',max((os.path.getsize(OUT+'/'+f),f) for f in FILES))
