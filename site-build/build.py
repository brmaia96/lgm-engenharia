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
    return ('<header class="top col"><a class="mk" href="index.html" aria-label="L. Engenharia, início" translate="no">L<i>.</i></a>'
            '<nav class="nav" aria-label="Páginas">%s</nav></header>')%nav
FOOT=('<footer class="col"><div class="ft">'
 '<div><b>Luis Gustavo Maia</b>Engenheiro civil<br>CREA-SP 5071068977</div>'
 '<div><b>Site</b><a href="inss.html#simulador">Calcular o INSS da obra</a><br><a href="obras.html">Obras</a><br><a href="blog.html">Blog</a><br><a href="sobre.html">Sobre</a></div>'
 '<div><b>Contato</b><a href="agenda.html">Marcar reunião</a><br><a href="%s" target="_blank" rel="noopener">WhatsApp (14) 99185-0799</a><br><a href="https://www.instagram.com/eng.gustavomaia/" target="_blank" rel="noopener">Instagram @eng.gustavomaia</a></div>'
 '<div><b>Atendimento</b>Marília, SP<br>Projetos em todo o Brasil</div>'
 '</div></footer>')%WA
DESC0='Luis Gustavo Maia, engenheiro civil. Projeto executivo em steel frame, projetos complementares e INSS de obra. Marília, SP, com atendimento em todo o Brasil.'
def head(title,desc):
    d=e(desc or DESC0,quote=True); t=e(html.unescape(title),quote=True)
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="theme-color" content="#ffffff"><meta name="description" content="%s"><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">'
            '<meta property="og:site_name" content="L. Engenharia"><meta property="og:title" content="%s"><meta property="og:description" content="%s">'
            '<title>%s</title>%s')%(d,t,d,title,FONTS)
SKIP='<a class="skip" href="#conteudo">Pular para o conteúdo</a>'
def tag(t): return '<h2 class="tag">%s</h2>'%e(t)   # rótulo de seção que também é o título da seção
def page(fn,title,cur,body,main=False,desc=None,extra=''):
    assert body.count('<main>')==1, fn
    body=body.replace('<main>','<main id="conteudo" tabindex="-1">')
    inner=SKIP+header(cur)+body+FOOT+'<script src="site.js"></script>'+extra
    full='<!doctype html><html lang="pt-BR"><head>%s</head><body>%s</body></html>\n'%(head(title,desc),inner)
    if main:
        open(OUT+'/'+fn,'w').write('<title>%s</title><meta name="claude:viewport-fit-sides" content="cover">%s<div lang="pt-BR">%s</div>\n'%(title,FONTS,inner))
        open(AUX+'/index.deploy.html','w').write(full)
    else:
        open(OUT+'/'+fn,'w').write(full); reg(fn)

CALC='<a class="lnk" href="inss.html#simulador">Calcular o INSS da minha obra</a>'
def call(h2,msg,label='Conversar pelo WhatsApp',calc=False):
    return '<section class="col call"><h2>%s</h2><p class="links">%s<a class="lnk" href="agenda.html">Marcar reunião</a><a class="lnk" href="%s" target="_blank" rel="noopener">%s</a></p></section>'%(h2,CALC if calc else '',wa(msg),label)

# ---------- imagens e cartões ----------
for p in P:
    s=p['slug']; base=A+'/'+p.get('assets',s)+'/'
    c=p['card']; ck=dict(maxw=1200,crop=c.get('crop'),ratio=4/3,focus=c.get('focus',(.5,.5)),q=78,pad=c.get('draw'),fam=c.get('fam','a'))
    p['_card']=put(base+c['src'],'img/%s/card.jpg'%s,**ck); p['_cardm']=put(base+c['src'],'img/%s/card-m.jpg'%s,mono=True,**ck)
    h=p['hero']
    if h.get('pair'):   # capa em par: duas imagens verticais lado a lado (fontes de 1122 px não aguentam a largura inteira)
        p['_hero']=put(base+h['src'],'img/%s/hero.jpg'%s,maxw=1200,crop=h.get('crop'),ratio=4/5,focus=h.get('focus',(.5,.5)),q=84,fam=h.get('fam','a'))
        p['_hero2']=put(base+h['pair'],'img/%s/hero2.jpg'%s,maxw=1200,crop=h.get('pair_crop'),ratio=4/5,focus=h.get('pair_focus',(.5,.5)),q=84,fam=h.get('pair_fam',h.get('fam','a')))
    else: p['_hero']=put(base+h['src'],'img/%s/hero.jpg'%s,maxw=2200,crop=h.get('crop'),q=80,fam=h.get('fam','a'))
    n=0
    for sec in p['sections']:
        for it in sec['items']:
            n+=1; it['fam']=D.FAM.get(p.get('assets',s),{}).get(it['src'].split('/')[-1],'a'); it['_img']=put(base+it['src'],'img/%s/%02d.jpg'%(s,n),maxw=1900,crop=it.get('crop'),q=80,fam=it['fam'])
def sub(p): return p['sub']
def card(p,lazy=True,feat=False):
    src,w,h=p['_hero'] if feat else p['_card']; ms=(p['_herom'] if feat else p['_cardm'])[0]
    at=(' style="object-position:%s"'%p['hero'].get('pos','50% 50%') if feat else '')+(' loading="lazy" decoding="async"' if lazy else '')
    return ('<a class="card%s" href="o-%s.html" data-cat="%s"><span class="ph"><picture><source media="(hover:none)" srcset="%s"><img src="%s" width="%d" height="%d" alt="%s"%s></picture><img class="m" src="%s" width="%d" height="%d" alt="" aria-hidden="true"%s></span>'
            '<span class="cap"><b>%s</b><span>%s</span></span><span class="sub">%s</span></a>')%(
            ' feat' if feat else '',p['slug'],e(p['cat']),ms,src,w,h,e(p['card'].get('alt',p['name'])),at,ms,w,h,at,e(p['name']),e(p['city']),e(sub(p)))

# ---------- páginas de projeto ----------
LB=('<dialog class="lb" id="lb" aria-label="Imagens do projeto"><header><span class="n" aria-live="polite"></span><button class="x" type="button">fechar</button></header>'
    '<div class="stage"><img alt=""><button class="nv p" type="button" aria-label="Imagem anterior"><span aria-hidden="true">&larr;</span></button>'
    '<button class="nv nx" type="button" aria-label="Próxima imagem"><span aria-hidden="true">&rarr;</span></button></div><footer><b></b><span></span></footer></dialog>')
for i,p in enumerate(P):
    hs,hw,hh=p['_hero']; H=p['hero']
    b='<main><section class="col phead"><p class="crumb"><a href="obras.html">obras</a> / %s</p><h1>%s</h1><p class="meta">%s</p></section>'%(e(p['cat_label']),e(p['name']),e(p['city']))
    if H.get('pair'): b+='<div class="wide heropair"><img src="%s" width="%d" height="%d" alt="%s" fetchpriority="high"><img src="%s" width="%d" height="%d" alt="%s"></div>'%(hs,hw,hh,e(H['alt']),p['_hero2'][0],p['_hero2'][1],p['_hero2'][2],e(H['alt2']))
    elif H.get('draw'): b+='<div class="wide herod %s"><img src="%s" width="%d" height="%d" alt="%s" fetchpriority="high"></div>'%(H['draw'],hs,hw,hh,e(H['alt']))
    elif hw<1900: b+='<div class="col"><img class="hero incol" src="%s" width="%d" height="%d" alt="%s" fetchpriority="high" style="object-position:%s"></div>'%(hs,hw,hh,e(H['alt']),H.get('pos','50% 50%'))
    else: b+='<img class="wide hero" src="%s" width="%d" height="%d" alt="%s" fetchpriority="high" style="object-position:%s">'%(hs,hw,hh,e(H['alt']),H.get('pos','50% 50%'))
    b+='<section class="col sec-s intro"><div class="txt"><p class="lead">%s</p>%s</div><dl class="ficha">%s</dl></section>'%(
        p['lead'],''.join('<p>%s</p>'%t for t in p.get('text',[])),''.join('<div><dt>%s</dt><dd>%s</dd></div>'%(e(k),v) for k,v in p['ficha']))
    for sec in p['sections']:
        g=''
        for it in sec['items']:
            src,w,h=it['_img']; cb,cs=it['cap']
            g+=('<figure class="%s%s"><a class="z"%s href="%s" data-b="%s" data-s="%s"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"%s></a>'
                '<figcaption class="cap"><b>%s</b>%s</figcaption></figure>')%(it.get('lay','full'),' night' if it['fam'] in ('c','d') else '',' style="aspect-ratio:%s"'%it['r'] if it.get('r') else '',src,e(cb),e(cs),src,w,h,e(it['alt']),
                ' style="object-position:%s"'%it['pos'] if it.get('pos') else '',e(cb),('<span>%s</span>'%e(cs)) if cs else '')
            if cb.lower()==sec['label'].lower() and not cs: g=g.replace('<figcaption class="cap"><b>%s</b></figcaption></figure>'%e(cb),'</figure>')
        b+='<section class="band sec">%s<div class="gal">%s</div></section>'%(tag(sec['label']),g)
    pv=P[i-1]; nx=P[(i+1)%len(P)]
    b+='<nav class="col" aria-label="Outros projetos"><div class="pn"><a href="o-%s.html"><span>anterior</span><b>%s</b></a><a href="o-%s.html"><span>próximo</span><b>%s</b></a></div></nav>'%(pv['slug'],e(pv['name']),nx['slug'],e(nx['name']))
    b+=call('Um projeto parecido com este?','Olá Gustavo, vi %s no site e quero conversar sobre um projeto.'%p.get('ref',p['name']),calc=p['slug']=='salas-comerciais')
    b+='</main>'+LB
    page('o-%s.html'%p['slug'],'%s · L. Engenharia'%p['name'],'obras',b,desc=p.get('desc') or '%s, %s: %s. Projeto de Luis Gustavo Maia, engenheiro civil.'%(p['name'],p['city'],sub(p).replace(' · ',', ')))

# ---------- obras ----------
cats=[]
for p in P:
    if p['cat'] not in [c[0] for c in cats]: cats.append((p['cat'],p['cat_plural']))
flt='<button type="button" data-k="*" aria-pressed="true">todas<sup>%d</sup></button>'%len(P)+''.join(
    '<button type="button" data-k="%s" aria-pressed="false">%s<sup>%d</sup></button>'%(e(k),e(l),sum(1 for p in P if p['cat']==k)) for k,l in cats)
b=('<main><section class="col phead"><h1>Obras</h1><p class="meta">%s</p><div class="flt" id="flt" role="group" aria-label="Filtrar por tipo">%s</div>'
   '<p class="sr" id="flt-st" aria-live="polite"></p></section><section class="col"><div class="grid obras" id="grid">%s</div></section>%s</main>')%(
   e(D.OBRAS_META),flt,''.join(card(p,lazy=(k>1)).replace('<a class="card','<a class="card s3' if (k<2 or ((len(P)-2)%3==2 and k>=len(P)-2)) else '<a class="card',1) for k,p in enumerate(P)),
   call('Tem um terreno ou um projeto em andamento?','Olá Gustavo, vi as obras no site e quero conversar sobre um projeto.'))
page('obras.html','Obras · L. Engenharia','obras',b,desc='Projetos de Luis Gustavo Maia, engenheiro civil: casas, chalés, salas comerciais e estruturas em aço.')

# ---------- blog ----------
for a in ART:
    c=a.get('cover')
    if c:
        a['_hero']=put(A+'/'+c['src'],'img/blog/%s.jpg'%a['slug'],maxw=2110,crop=c.get('crop'),ratio=16/9,focus=c.get('focus',(.5,.5)),q=84,fam=c.get('fam','a'))
        tk=dict(maxw=720,crop=c.get('crop'),ratio=4/3,focus=c.get('focus',(.5,.5)),q=78,fam=c.get('fam','a'))
        a['_th']=put(A+'/'+c['src'],'img/blog/%s-t.jpg'%a['slug'],**tk); a['_thm']=put(A+'/'+c['src'],'img/blog/%s-tm.jpg'%a['slug'],mono=True,**tk)
def post(a,lazy=True,pic=True):
    th=''
    if pic and a.get('_th'):
        src,w,h=a['_th']; at=' loading="lazy" decoding="async"' if lazy else ''
        th='<span class="ph"><picture><source media="(hover:none)" srcset="%s"><img src="%s" width="%d" height="%d" alt="%s"%s></picture><img class="m" src="%s" width="%d" height="%d" alt="" aria-hidden="true"%s></span>'%(a['_thm'][0],src,w,h,e(a['cover']['alt']),at,a['_thm'][0],w,h,at)
    return ('<a class="row%s" href="b-%s.html" data-cat="%s">%s<span class="h"><span class="t">%s</span><b>%s</b><span class="s">%s</span></span></a>')%(
            ' pic' if th else '',a['slug'],e(a['tema']),th,e(a['tema']),a['title'],a['resumo'])
for i,a in enumerate(ART):
    c=a.get('cover')
    b=('<main><article><section class="col phead"><p class="crumb"><a href="blog.html">blog</a> / %s</p><h1>%s</h1><p class="lead" style="margin-top:26px">%s</p>'
       '<p class="meta">leitura de %d min · %s</p></section>')%(e(a['tema']),a['h1'],a['lead'],a['mins'],e(BL.DATA))
    if c:
        hs,hw,hh=a['_hero']; b+='<section class="col cover"><figure><img class="art%s" src="%s" width="%d" height="%d" alt="%s" fetchpriority="high">'%(' night' if c.get('fam') in ('c','d') else '',hs,hw,hh,e(c['alt']))
        b+=('<figcaption class="cap"><b>%s</b><span>%s</span></figcaption>'%c['cap'] if c.get('cap') else '')+'</figure></section>'
    for k,(lab,htm) in enumerate(a['body']):
        b+='<section class="band %s">%s<div class="prose">%s</div></section>'%('sec-s' if k==0 else 'sec-n',tag(lab),htm)
    if a.get('fontes'):
        # fonte: só o título, sem link e sem PDF (instrução do cliente)
        b+='<section class="band sec-s">%s<ol class="fontes">%s</ol></section>'%(tag('Fontes'),''.join('<li><span>%s</span></li>'%e(t) for t in a['fontes']))
    b+='</article>'
    others=[x for x in ART if x is not a]; rl=[x for x in others if x['slug'] in a.get('rel',[])] or others[:2]
    if rl: b+='<section class="band sec">%s<div class="rel">%%s</div></section>'%tag('Continue lendo')%''.join('<a href="b-%s.html"><span>%s</span><b>%s</b></a>'%(x['slug'],e(x['tema']),x['title']) for x in rl[:2])
    b+=call(a.get('call','Está decidindo como construir?'),'Olá Gustavo, li o artigo "%s" no site e quero conversar sobre um projeto.'%html.unescape(a['title']),calc=a['tema']=='imposto')+'</main>'
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
if ART: page('blog.html','Blog · L. Engenharia','blog',b,desc='Perguntas de quem vai construir, respondidas direto ao ponto: o INSS da obra, o CNO e o steel frame.')

# ---------- home ----------
M=A+'/marca/clean/'
sel=[p for p in P if p['slug'] in D.HOME_SELECT]; sel.sort(key=lambda p:D.HOME_SELECT.index(p['slug']))
# filme: dois cortes do mesmo roteiro (16:9 para o computador, 4:5 para o celular), gravados em scratchpad/video5
V5=S+'/video5'
os.makedirs(OUT+'/media',exist_ok=True)
for f in ('apresentacao.mp4','apresentacao-celular.mp4'): shutil.copy(V5+'/'+f,OUT+'/media/'+f); reg('media/'+f)
put(V5+'/frames-w/f00120.jpg','img/video-poster.jpg',maxw=1920,q=84,fam=None)
put(V5+'/frames-m/f00120.jpg','img/video-poster-m.jpg',maxw=1080,q=84,fam=None)
put(S+'/portrait/retrato.jpg','img/retrato.jpg',maxw=1100,q=86,fam=None)
# os dizeres do filme, na ordem em que passam (os números vêm da página de INSS, fonte única)
FILME=('O filme apresenta os serviços de Luis Gustavo Maia, engenheiro civil. A obra paga INSS, quase sempre a mais. '
 'Pelo INSS da obra: planejamento tributário, inscrição no CNO em até 30 dias do início, enquadramento do tipo de obra, aferição no Sero e certidão da obra. '
 'Resultado, pelos documentos da Receita: %d obras aferidas, em %d cidades de São Paulo e Mato Grosso, e %s de desconto documentado em %s obras. '
 'Steel frame não é moda, é engenharia. Projeto: projeto executivo em steel frame, projetos complementares, plano de corte e caderno de montagem, e estrutura metálica. '
 'Obra e regularização: acompanhamento de obra, projeto legal e aprovação, as built e laudo de habite-se, e regularização de construção. '
 'Sem terceirizar, sem delegar o que importa. Projeto, execução e engenharia tributária, com uma única responsabilidade técnica. Do terreno à chave.')%(D.INSS.N_OBRAS,D.INSS.N_CID,D.INSS.brl(D.INSS.ECON_REAL),D.INSS.N_DESC_EXT)
# A home abre como as páginas internas, com o gancho do INSS, os dois números e a calculadora na primeira tela.
# O filme vem logo depois, dentro da coluna; toca sozinho, mudo, quando entra na tela.
b=('<main><section class="col phead home"><p class="crumb">engenharia tributária</p>'
 '<h1 class="h0">A obra paga INSS. <b>Quase sempre a mais.</b></h1>'
 '<p class="lead" style="margin-top:26px">Projeto, execução e engenharia tributária, <b>com uma única responsabilidade técnica.</b></p>'
 '<div class="nums" style="margin-top:48px"><div><div class="num">%(sem)s</div><div class="nl">de INSS em uma casa de %(area)s em %(uf)s, sem planejamento</div></div>'
 '<div><div class="num sv">até %(pct)s</div><div class="nl">a menos, com o enquadramento certo</div></div>'
 '<div class="act"><a class="btn" href="inss.html#simulador">Calcular o INSS da minha obra</a></div></div></section>')%D.INSS.NUM
b+=('<section class="col sec-s"><figure class="film"><div class="vid"><video id="vid" width="1920" height="1080" muted loop playsinline autoplay preload="auto" aria-label="Filme de apresentação dos serviços de Luis Gustavo Maia, engenheiro civil" aria-describedby="vid-d">'
 '<source media="(max-width:640px)" src="media/apresentacao-celular.mp4" type="video/mp4"><source src="media/apresentacao.mp4" type="video/mp4"></video></div>'
 '<figcaption class="cap vctl"><b>Apresentação</b><span class="vb"><span>1 min 18 s</span><button id="vsnd" type="button">ativar som</button><button id="vbtn" type="button">pausar</button></span></figcaption></figure>'
 '<p class="sr" id="vid-d">%s</p></section>')%FILME
b+='<section class="band sec">%s<div><div class="grid three">%s</div><p style="margin-top:44px"><a class="lnk" href="obras.html">Todas as obras</a></p></div></section>'%(tag('Obras'),''.join(card(p) for p in sel))
# só a parte de cima da foto (treliças e painéis): o chão da obra tinha poça, sacos, ferramentas e uma pessoa
OBRA=put(M+'obra-real.jpg','img/marca/obra-real.jpg',maxw=1600,crop=(0,0,1,.53),q=86)
b+=('<section class="col sec"><h2 class="hx">Steel frame não é moda. <b>É engenharia.</b></h2>'
 '<figure style="margin-top:clamp(36px,4vw,56px)"><img class="art" src="%s" width="%d" height="%d" alt="Steel frame em obra: treliças de entrepiso e painéis de parede em aço galvanizado" loading="lazy" decoding="async" style="aspect-ratio:auto">'
 '<figcaption class="cap"><b>Steel frame em obra</b><span>painéis de parede e treliças de entrepiso</span></figcaption></figure></section>')%OBRA
hb=[a for a in ART if a['slug'] in BL.HOME] or ART[:3]
hb.sort(key=lambda a:(BL.HOME.index(a['slug']) if a['slug'] in BL.HOME else 99))
if hb: b+='<section class="band sec">%s<div><div class="rows">%s</div><p style="margin-top:44px"><a class="lnk" href="blog.html">Todos os artigos</a></p></div></section>'%(tag('Blog'),''.join(post(a,pic=False) for a in hb))
b+=call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.')+'</main>'
page('index.html','L. Engenharia','home',b,main=True)

# ---------- inss e sobre ----------
INSS_IMG=put(A+'/taquaracu/clean/10-steel-frame-por-dentro.jpg','img/inss/estrutura.jpg',maxw=2000,ratio=16/9,focus=(.5,.42),q=82)
page('inss.html','INSS de obra · L. Engenharia','inss',D.INSS.inss_body(INSS_IMG),desc='INSS de obra: quanto a Receita Federal cobraria da sua construção e por que steel frame, wood frame e modular podem pagar menos. Calculadora por estado.')
page('agenda.html','Marcar reunião · L. Engenharia','agenda',D.AGENDA_BODY,desc='Marque uma reunião de 30 minutos por vídeo com Luis Gustavo Maia, engenheiro civil, sobre o terreno, o projeto ou o INSS da obra.')
page('sobre.html','Sobre · L. Engenharia','sobre',D.SOBRE_BODY.replace('</main>',call('Do terreno. <em>À chave.</em>','Olá Gustavo, vi o site e quero conversar sobre um projeto.')+'</main>'),desc='Luis Gustavo Maia, engenheiro civil, CREA-SP 5071068977. Steel frame desde 2018: projeto executivo, complementares, acompanhamento de obra e INSS.')
for f in ('styles.css','site.js'): shutil.copy(B+'/'+f,OUT+'/'+f); reg(f)
import json; json.dump(FILES,open(AUX+'/files.json','w'),indent=0)
tot=sum(os.path.getsize(OUT+'/'+f) for f in FILES)
print(len(FILES),'files',round(tot/1e6,1),'MB; largest',max((os.path.getsize(OUT+'/'+f),f) for f in FILES))
