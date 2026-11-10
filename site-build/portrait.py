# Retrato: mantém a pessoa como está e troca só o fundo por um fundo de estúdio escuro e liso.
import numpy as np, cv2, onnxruntime as ort
from PIL import Image
S='/tmp/claude-0/-home-user-lgm-engenharia/49376ed1-2cbe-5161-a523-12fb37b2af57/scratchpad'
src=Image.open(S+'/dl/gustavo-pb.jpg').convert('RGB')
W,H=src.width*2,src.height*2
big=np.asarray(src.resize((W,H),Image.LANCZOS)).astype(np.float32)/255.
# máscara da pessoa (u2net human seg)
x=np.asarray(src.resize((320,320),Image.BILINEAR)).astype(np.float32)/255.
x=(x-np.array([.485,.456,.406]))/np.array([.229,.224,.225]); x=x.transpose(2,0,1)[None].astype(np.float32)
ses=ort.InferenceSession(S+'/models/u2net_human_seg.onnx',providers=['CPUExecutionProvider'])
d=ses.run(None,{ses.get_inputs()[0].name:x})[0][0,0]; d=(d-d.min())/(d.max()-d.min())
m=cv2.resize(d,(W,H),interpolation=cv2.INTER_CUBIC); m=np.clip((m-.35)/.3,0,1)
m=cv2.erode(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))); m=cv2.GaussianBlur(m,(0,0),3.0)
cv2.imwrite(S+'/portrait/mask.png',(m*255).astype(np.uint8))
g=big.mean(2)
# fundo de estúdio: cinza-carvão com luz suave vinda da direita, sem nenhuma forma
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); xx/=W; yy/=H
bg=.075+.085*np.exp(-(((xx-.80)/.55)**2+((yy-.30)/.60)**2))
bg*=1-.35*np.clip((yy-.55)/.45,0,1)
out=g*m+bg*(1-m)
# acabamento: curva leve, grão fino
out=np.clip(out,0,1); out=out**.96
rng=np.random.default_rng(7); out=np.clip(out+rng.normal(0,.012,out.shape).astype(np.float32),0,1)
rgb=np.stack([out,out*.99,out*.965],-1)
Image.fromarray((rgb*255+.5).astype(np.uint8)).save(S+'/portrait/retrato.jpg',quality=93)
prev=np.hstack([np.stack([g]*3,-1),rgb]); Image.fromarray((prev*255).astype(np.uint8)).resize((1304,870)).save(S+'/portrait/prev.jpg',quality=85)
print('ok',W,H,float(m.mean()))
