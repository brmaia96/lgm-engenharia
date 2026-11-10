# Comparador da Casa Taquaraçu: estrutura x pronta. Nada é deformado: só recorte 16:9, escala uniforme e deslocamento.
import cv2, numpy as np, sys
S='/tmp/claude-0/-home-user-lgm-engenharia/49376ed1-2cbe-5161-a523-12fb37b2af57/scratchpad'
W,H=2000,1125
def crop169(p,cy):
    im=cv2.imread(p); h,w=im.shape[:2]; ch=int(w*9/16); y=int((h-ch)*cy); return cv2.resize(im[y:y+ch],(W,H),interpolation=cv2.INTER_AREA)
A=crop169(S+'/assets/taquaracu/clean/08-fundacao-e-estrutura.jpg',.52)   # estrutura
B=crop169(S+'/assets/taquaracu/clean/01-capa-aerea.jpg',.62)             # pronta
k=float(sys.argv[1]) if len(sys.argv)>1 else .68
ca=np.array([536/960*W,189/540*H]); cb=np.array([382/960*W,232/540*H])    # centro do telhado principal em cada imagem
a=cv2.resize(A,(int(W*k),int(H*k)),interpolation=cv2.INTER_AREA); off=(cb-ca*k).round().astype(int)
x0,y0=off; l,t=max(x0,0),max(y0,0); r,b=max(W-(x0+a.shape[1]),0),max(H-(y0+a.shape[0]),0)
ext=cv2.copyMakeBorder(a,t,b,l,r,cv2.BORDER_REPLICATE)
sx,sy=max(-x0,0),max(-y0,0); ext=ext[sy:sy+H,sx:sx+W]
# suaviza só a área estendida, para não aparecerem faixas
m=np.zeros((H,W),np.float32); m[t:t+a.shape[0]-sy, l:l+a.shape[1]-sx]=1; m=cv2.GaussianBlur(m,(0,0),18)[...,None]
blur=cv2.GaussianBlur(ext,(0,0),40); est=(ext*m+blur*(1-m)).astype(np.uint8)
cv2.imwrite(S+'/work/minas-estrutura.png',est); cv2.imwrite(S+'/work/minas-pronta.png',B)
half=B.copy(); half[:, :W//2]=est[:, :W//2]; cv2.line(half,(W//2,0),(W//2,H),(255,255,255),2)
cv2.imwrite(S+'/work/minas-half.jpg',cv2.resize(np.hstack([est,half]),(2000,563)),[cv2.IMWRITE_JPEG_QUALITY,82])
print('k',k,'off',off)
