# Gera o site L. Engenharia em scratchpad/site a partir de build/data.py
import os, shutil, sys, html, urllib.parse, importlib.util
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import grade as G
S='/tmp/claude-0/-home-user-lgm-engenharia/49376ed1-2cbe-5161-a523-12fb37b2af57/scratchpad'
A=S+'/assets'; B=S+'/build'; OUT=os.environ.get('SITE_OUT',S+'/site'); AUX=OUT if os.environ.get('SITE_OUT') else B
spec=importlib.util.spec_from_file_location('data',os.environ.get('SITE_DATA',B+'/data.py')); D=importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
P=D.PROJECTS
_bs=importlib.util.spec_from_file_location('blog',B+'/blog.py'); BL=importlib.util.module_from_spec(_bs); _bs.loader.exec_module(BL)
ART=BL.ARTICLES
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
    if fam=='d': return G.duotone(im,invert=True) if mono else G.studio(im)
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
        (('inss','inss.html','inss'),('obras','obras.html','obras'),('blog','blog.html','blog'),('sobre','sobre.html','sobre'),('agenda','agenda.html','agenda')))
    return ('<header class="top col"><a class="mk" href="index.html" aria-label="L. Engenharia, início">L<i>.</i></a>'
            '<nav class="nav" aria-label="Páginas">%s</nav></header>')%nav
FOOT=('<footer class="col"><div class="ft">'
 '<div><b>Luis Gustavo Maia</b>Engenheiro civil<br>CREA-SP 5071068977</div>'
 '<div><b>Contato</b><a href="agenda.html">Marcar reunião</a><br><a href="%s" target="_blank" rel="noopener">WhatsApp (14) 99185-0799</a><br><a href="https://www.instagram.com/eng.gustavomaia/" target="_blank" rel="noopener">Instagram @eng.gustavomaia</a></div>'
 '<div><b>Atendimento</b>Marília, SP<br>Projetos em todo o Brasil</div>'
 '</div></footer>')%WA
DESC0='Luis Gustavo Maia, engenheiro civil. Projeto executivo em steel frame, projetos complementares e INSS de obra. Marília, SP, com atendimento em todo o Brasil.'
def head(title,desc):
    d=e(desc or DESC0,quote=True); t=e(html.unescape(title),quote=True)
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="description" content="%s"><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">'
            '<meta property="og:site_name" content="L. Engenharia"><meta property="og:title" content="%s"><meta property="og:description" content="%s">'
            '<title>%s</title>%s')%(d,t,d,title,FONTS)
def page(fn,title,cur,body,main=False,desc=None,extra=''):
    inner=header(cur)+body+FOOT+'<script src="site.js"></script>'+extra
    full='<!doctype html><html lang="pt-BR"><head>%s</head><body>%s</body></html>\n'%(head(title,desc),inner)
    if main:
        open(OUT+'/'+fn,'w').write('<title>%s</title><meta name="claude:viewport-fit-sides" content="cover">%s<div lang="pt-BR">%s</div>\n'%(title,FONTS,inner))
        open(AUX+'/index.deploy.html','w').write(full)
    else:
        open(OUT+'/'+fn,'w').write(full); reg(fn)

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
                '<figcaption class="cap"><b>%s</b><span>%s</span></figcaption></figure>')%(it.get('lay','full'),' night' if it['fam'] in ('c','d') else '',' style="aspect-ratio:%s"'%it['r'] if it.get('r') else '',src,e(cb),e(cs),src,w,h,e(it['alt']),
                ' style="object-position:%s"'%it['pos'] if it.get('pos') else '',e(cb),e(cs))
        b+='<section class="band sec"><div class="tag"><b>%s</b></div><div class="gal">%s</div></section>'%(e(sec['label']),g)
    pv=P[i-1]; nx=P[(i+1)%len(P)]
    b+='<nav class="col" aria-label="Outros projetos"><div class="pn"><a href="o-%s.html"><span>anterior</span><b>%s</b></a><a href="o-%s.html"><span>próximo</span><b>%s</b></a></div></nav>'%(pv['slug'],e(pv['name']),nx['slug'],e(nx['name']))
    b+=call('Um projeto parecido com este?','Olá Gustavo, vi %s no site e quero conversar sobre um projeto.'%p.get('ref',p['name']))
    b+='</main>'+LB
    page('o-%s.html'%p['slug'],'%s · L. Engenharia'%p['name'],'obras',b,desc='%s, %s. %s. Projeto de Luis Gustavo Maia, engenheiro civil.'%(p['name'],p['city'].replace(' · ',', '),sub(p).replace(' · ',', ')))

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
page('obras.html','Obras · L. Engenharia','obras',b,desc='Projetos de Luis Gustavo Maia: casas, chalés e estruturas em aço, com fachadas, interiores e a estrutura de cada obra.')

# ---------- blog ----------
for a in ART:
    c=a.get('cover')
    if c: a['_hero']=put(A+'/'+c['src'],'img/blog/%s.jpg'%a['slug'],maxw=2200,crop=c.get('crop'),q=80,fam=c.get('fam','a'))
def post(a,lazy=True):
    return ('<a class="row" href="b-%s.html" data-cat="%s"><span class="t">%s</span><span class="h"><b>%s</b><span class="s">%s</span></span><span class="m">%d min</span></a>')%(
            a['slug'],e(a['tema']),e(a['tema']),a['title'],a['resumo'],a['mins'])
for i,a in enumerate(ART):
    c=a.get('cover')
    b=('<main><article><section class="col phead"><p class="crumb"><a href="blog.html">blog</a> / %s</p><h1>%s</h1><p class="lead" style="margin-top:26px">%s</p>'
       '<p class="meta">leitura de %d min · %s</p></section>')%(e(a['tema']),a['h1'],a['lead'],a['mins'],e(BL.DATA))
    if c:
        hs,hw,hh=a['_hero']; b+='<img class="wide hero" src="%s" width="%d" height="%d" alt="%s" style="object-position:%s">'%(hs,hw,hh,e(c['alt']),c.get('pos','50% 50%'))
        if c.get('cap'): b+='<div class="col"><div class="cap"><b>%s</b><span>%s</span></div></div>'%c['cap']
    for k,(lab,htm) in enumerate(a['body']):
        b+='<section class="band %s"><div class="tag"><b>%s</b></div><div class="prose">%s</div></section>'%('sec-s' if k==0 else 'sec',e(lab),htm)
    if a.get('fontes'):
        b+='<section class="band sec"><div class="tag"><b>Fontes</b></div><ol class="fontes">%s</ol></section>'%''.join(
            '<li><span>%s</span></li>'%(('%s <a href="%s" target="_blank" rel="noopener">%s</a>'%(t,u,e(u.split('//')[-1].split('/')[0]))) if u else t) for t,u in a['fontes'])
    b+='</article>'
    others=[x for x in ART if x is not a]; rl=[x for x in others if x['slug'] in a.get('rel',[])] or others[:2]
    if rl: b+='<section class="band sec"><div class="tag"><b>Continue lendo</b></div><div class="rel">%s</div></section>'%''.join('<a href="b-%s.html"><span>%s · %d min</span><b>%s</b></a>'%(x['slug'],e(x['tema']),x['mins'],x['title']) for x in rl[:2])
    b+=call(a.get('call','Está decidindo como construir?'),'Olá Gustavo, li o artigo "%s" no site e quero conversar sobre um projeto.'%html.unescape(a['title']))+'</main>'
    page('b-%s.html'%a['slug'],'%s · L. Engenharia'%a['title'],'blog',b,desc=a['desc'],extra=LB if 'class="gal"' in b else '')
temas=[]
for a in ART:
    if a['tema'] not in temas: temas.append(a['tema'])
flt='<button type="button" data-k="*" aria-pressed="true">todos<sup>%d</sup></button>'%len(ART)+''.join(
    '<button type="button" data-k="%s" aria-pressed="false">%s<sup>%d</sup></button>'%(e(t),e(t),sum(1 for a in ART if a['tema']==t)) for t in temas)
b=('<main><section class="col phead"><h1>%s</h1><p class="lead" style="margin-top:26px">%s</p><div class="flt" id="flt" role="group" aria-label="Filtrar por tema" data-one="artigo" data-many="artigos">%s</div>'
   '<p class="sr" id="flt-st" aria-live="polite"></p></section><section class="col"><div class="rows" id="grid">%s</div></section>%s</main>')%(
   BL.INDEX_H1,BL.INDEX_LEAD,flt,''.join(post(a,lazy=(k>2)) for k,a in enumerate(ART)),
   call('Ficou com uma dúvida que não está aqui?','Olá Gustavo, li o blog no site e tenho uma dúvida sobre construção.','Perguntar pelo WhatsApp'))
if ART: page('blog.html','Blog · L. Engenharia','blog',b,desc='Perguntas de quem vai construir, respondidas com norma, número e fonte: custo, conforto, prazo, durabilidade e financiamento do steel frame.')

# ---------- home ----------
put(S+'/work/minas-estrutura.png','img/cmp/estrutura.jpg',maxw=2000,q=84,fam='c')
put(S+'/work/minas-pronta.png','img/cmp/pronta.jpg',maxw=2000,q=84)
M=A+'/marca/clean/'
OBRA=put(M+'obra-real.jpg','img/marca/obra-real.jpg',maxw=2000,q=82)
sel=[p for p in P if p['slug'] in D.HOME_SELECT]; sel.sort(key=lambda p:D.HOME_SELECT.index(p['slug']))
os.makedirs(OUT+'/media',exist_ok=True); shutil.copy(S+'/video3/apresentacao.mp4',OUT+'/media/apresentacao.mp4'); reg('media/apresentacao.mp4')
put(S+'/video3/frames/f00105.jpg','img/video-poster.jpg',maxw=1920,q=84,fam=None)
put(S+'/portrait/retrato.jpg','img/retrato.jpg',maxw=1100,q=86,fam=None)
b=('<main><div class="wide vid"><video id="vid" src="media/apresentacao.mp4" poster="img/video-poster.jpg" width="1920" height="1080" muted loop playsinline autoplay preload="metadata" aria-label="Vídeo de apresentação de Luis Gustavo Maia, engenheiro civil: trajetória, o que faz, projetos e INSS de obra"></video>'
 '<button class="vbtn" id="vbtn" type="button">pausar</button></div>'
 '<div class="col"><div class="cap"><b>Luis Gustavo Maia</b><span>engenheiro civil · CREA-SP 5071068977</span></div></div>'
 '<section class="col sec-s"><h1>Projeto, execução e engenharia tributária, <b>com uma única responsabilidade técnica.</b></h1></section>')
CMP=('<section class="band sec"><div class="tag"><b>Estrutura × pronta</b></div><div>'
 '<figure class="cmp" id="cmp" style="--p:50%%"><img src="img/cmp/pronta.jpg" width="2000" height="1125" alt="Casa Taquaraçu pronta, vista aérea com piscina" draggable="false">'
 '<img class="st" src="img/cmp/estrutura.jpg" width="2000" height="1125" alt="Estrutura em light steel frame da Casa Taquaraçu, sobre radier em pilares" draggable="false">'
 '<span class="tg l">estrutura</span><span class="tg r">pronta</span>'
 '<span class="bar" aria-hidden="true"><svg viewBox="0 0 44 16" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M9 2L3 8l6 6M35 2l6 6-6 6"/></svg></span>'
 '<input id="cmp-r" type="range" min="0" max="100" step="1" value="50" aria-label="Comparar a estrutura em steel frame e a casa pronta"></figure>'
 '<div class="cap">%s</div></div></section>'%D.CMP_CAPTION)
b+=('<section class="band sec-s"><div class="tag"><b>Engenharia tributária</b></div><div><h2 style="max-width:20em">O INSS de uma casa de %(area)s em steel frame, <b>com e sem planejamento.</b></h2>'
 '<div class="nums" style="margin-top:36px"><div><div class="num off">%(sem)s</div><div class="nl">aferição indireta, sem planejamento</div></div>'
 '<div><div class="num">%(com)s</div><div class="nl">com pré-fabricado comprovado por nota</div></div>'
 '<div><div class="num sv">%(econ)s</div><div class="nl">de volta ao orçamento da obra</div></div></div>'
 '<p class="links" style="display:flex;flex-wrap:wrap;gap:10px 44px;margin-top:44px;max-width:none"><a class="lnk" href="inss.html">Entender o INSS da obra</a><a class="lnk" href="inss.html#simulador">Simular o INSS da minha obra</a></p></div></section>')%D.INSS.NUM
b+=CMP
b+='<section class="band sec"><div class="tag"><b>Obras</b></div><div><div class="grid three">%s</div><p style="margin-top:44px"><a class="lnk" href="obras.html">Todas as obras</a></p></div></section>'%''.join(card(p) for p in sel)
b+=('<section class="col sec"><h2 style="font-size:clamp(26px,3vw,40px);line-height:1.22;letter-spacing:-.012em">Steel frame não é moda. <b>É engenharia.</b></h2></section>'
 '<img class="wide obra" src="%s" width="%d" height="%d" alt="Steel frame em obra: painéis de parede e treliças de entrepiso montados sobre a laje" loading="lazy" decoding="async">'
 '<div class="col"><div class="cap"><b>Steel frame em obra</b><span>painéis de parede e treliças de entrepiso</span></div></div>')%OBRA
hb=[a for a in ART if a['slug'] in BL.HOME] or ART[:3]
hb.sort(key=lambda a:(BL.HOME.index(a['slug']) if a['slug'] in BL.HOME else 99))
if hb: b+='<section class="band sec"><div class="tag"><b>Blog</b></div><div><div class="rows">%s</div><p style="margin-top:44px"><a class="lnk" href="blog.html">Todos os artigos</a></p></div></section>'%''.join(post(a) for a in hb)
b+=call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.')+'</main>'
page('index.html','L. Engenharia','home',b,main=True)

# ---------- inss e sobre ----------
INSS_IMG=put(A+'/taquaracu/clean/10-steel-frame-por-dentro.jpg','img/inss/estrutura.jpg',maxw=2000,ratio=16/9,focus=(.5,.42),q=82)
page('inss.html','INSS de obra · L. Engenharia','inss',D.INSS.inss_body(INSS_IMG),desc='INSS de obra: como a Receita calcula, como pagar só o devido, por que o steel frame pode reduzir a base de cálculo e o passo a passo do CNO à certidão. Com simulador.')
page('agenda.html','Marcar reunião · L. Engenharia','agenda',D.AGENDA_BODY,desc='Marque uma reunião de 30 minutos por vídeo com Luis Gustavo Maia, engenheiro civil, sobre o terreno, o projeto ou o INSS da obra.')
page('sobre.html','Sobre · L. Engenharia','sobre',D.SOBRE_BODY+call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.'),desc='Luis Gustavo Maia, engenheiro civil, CREA-SP 5071068977. Steel frame desde 2018: projeto executivo, complementares, acompanhamento de obra e INSS.')
for f in ('styles.css','site.js'): shutil.copy(B+'/'+f,OUT+'/'+f); reg(f)
import json; json.dump(FILES,open(AUX+'/files.json','w'),indent=0)
tot=sum(os.path.getsize(OUT+'/'+f) for f in FILES)
print(len(FILES),'files',round(tot/1e6,1),'MB; largest',max((os.path.getsize(OUT+'/'+f),f) for f in FILES))
