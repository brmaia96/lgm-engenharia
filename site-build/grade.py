# Padrão de imagem L.: três famílias, um tratamento cada.
#  a = render/foto  -> cor graduada (balanço neutro-quente, saturação contida, exposição nivelada)
#  b = desenho      -> tinta sobre papel (uma cor só)
#  c = modelo de estrutura em fundo escuro -> monocromático sobre preto
#  mono = capa em duotone quente (tinta x papel), igual para todas
import numpy as np
from PIL import Image
INK=np.array([47,45,43])/255.; PAPER=np.array([244,242,238])/255.; PANEL=np.array([247,246,244])/255.; NIGHT=10/255.
def _lum(a): return a[...,0]*.2126+a[...,1]*.7152+a[...,2]*.0722
def _arr(im): return np.asarray(im.convert('RGB'),dtype=np.float32)/255.
def _img(a): return Image.fromarray((np.clip(a,0,1)*255+.5).astype(np.uint8))
def grade_a(im,expo=True,sat=.62):
    a=_arr(im)
    m=a.reshape(-1,3).mean(0); g=m.mean(); a=a*(1+(g/np.maximum(m,1e-3)-1)*.55)      # balanço de branco parcial
    a=np.clip(a,0,1)
    if expo:
        mean=float(_lum(a).mean()); gam=float(np.clip(np.log(.47)/np.log(max(mean,1e-3)),.72,1.25)); a=a**gam
    L=_lum(a)[...,None]; a=L+(a-L)*sat
    a=a*np.array([1.015,1.0,.965])
    a=.025+a*.955
    return _img(a)
def duotone(im,invert=False):
    L=_lum(_arr(im)); lo,hi=np.percentile(L,1),np.percentile(L,99); L=np.clip((L-lo)/max(hi-lo,1e-3),0,1)
    if invert: L=1-L
    mean=float(L.mean()); L=L**float(np.clip(np.log(.56)/np.log(max(mean,1e-3)),.6,1.6))
    return _img(INK+(PAPER-INK)*L[...,None])
def ink(im,paper=PANEL):
    L=_lum(_arr(im)); L=np.clip((L-.04)/.92,0,1)
    return _img(INK+(paper-INK)*L[...,None])
def model(im):
    L=_lum(_arr(im)); lo=np.percentile(L,8); L=np.clip((L-lo)/(1-lo),0,1)**.95
    return _img((NIGHT+(.96-NIGHT)*L)[...,None]*np.array([1.0,.995,.985]))
def studio(im,sat=.78):
    """render em cor sobre fundo de estúdio escuro: sem balanço de branco (o fundo preto enganaria a média), saturação contida, preto nivelado no mesmo #0A0A0A"""
    a=_arr(im); L=_lum(a)[...,None]; a=L+(a-L)*sat
    a=a*np.array([1.01,1.0,.975])
    lo=float(np.percentile(_lum(a),3)); a=np.clip((a-lo)/(1-lo),0,1)
    return _img(NIGHT+(.97-NIGHT)*a)
