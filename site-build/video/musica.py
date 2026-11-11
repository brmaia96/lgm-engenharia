# Trilha original do vídeo (sintetizada aqui, sem amostra de terceiros): 84 bpm, Ré menor, 78 s.
import numpy as np, wave
SR=44100; D=78.0; BPM=84; BEAT=60/BPM; BAR=4*BEAT; N=int(SR*D); t=np.arange(N)/SR
def hz(m): return 440*2**((m-69)/12)
# progressão de 4 compassos: Dm9  Bbmaj7  Fmaj7  C(add9)
CH=[[50,57,60,64,65],[46,53,57,62,65],[41,53,57,60,64],[48,55,60,62,64]]
out=np.zeros((N,2))
def env(n,a,r):
    e=np.ones(n); na=min(n,int(a*SR)); nr=min(n,int(r*SR)); e[:na]=np.linspace(0,1,na)**1.5; e[-nr:]*=np.linspace(1,0,nr)**1.5; return e
def add(sig,start,pan=.5,g=1.0):
    i=int(start*SR); 
    if i>=N: return
    sig=sig[:N-i]; out[i:i+len(sig),0]+=sig*g*np.cos(pan*np.pi/2); out[i:i+len(sig),1]+=sig*g*np.sin(pan*np.pi/2)
nb=int(np.ceil(D/BAR))
rng=np.random.default_rng(3)
for b in range(nb):
    ch=CH[b%4]; st=b*BAR; n=int((BAR+1.2)*SR); tt=np.arange(n)/SR
    # pad: senoides com leve desafinação e segundo harmônico suave
    pad=np.zeros(n)
    for m in ch[1:]:
        f=hz(m)
        for det,ph in ((-.18,0),(.21,1.3)): pad+=np.sin(2*np.pi*(f+det)*tt+ph)+.22*np.sin(2*np.pi*2*(f+det)*tt+ph)+.07*np.sin(2*np.pi*3*(f+det)*tt)
    pad*=env(n,1.1,1.4)*(.5+.5*np.sin(2*np.pi*tt/BAR-np.pi/2)*.25+.25)
    lvl=.030*min(1,(b+1)/3)
    add(pad,st,.35,lvl); add(np.roll(pad,180),st,.65,lvl)
    # baixo
    if b>=2:
        for k,bt in enumerate((0,2.5)):
            nn=int(1.6*BEAT*SR); x=np.arange(nn)/SR; f=hz(ch[0]-12 if ch[0]>45 else ch[0])
            add((np.sin(2*np.pi*f*x)+.3*np.sin(2*np.pi*2*f*x))*np.exp(-x*1.6)*env(nn,.01,.2),st+bt*BEAT,.5,.20)
    # arpejo em colcheias, com eco
    if b>=4 and b<nb-2:
        seq=[ch[1],ch[3],ch[2],ch[4],ch[3],ch[2],ch[4],ch[3]]
        for k,m in enumerate(seq):
            nn=int(.9*SR); x=np.arange(nn)/SR; f=hz(m+12)
            s=(np.sin(2*np.pi*f*x)+.35*np.sin(2*np.pi*2*f*x)*np.exp(-x*6))*np.exp(-x*5.5)*env(nn,.004,.1)
            g=.085*(1.0 if k%2==0 else .7)
            for e_,dl in enumerate((0,.75*BEAT,1.5*BEAT)): add(s,st+k*BEAT/2+dl,(.25,.75,.5)[e_],g*(.5**e_))
    # bumbo suave e chimbal de ruído
    if b>=8 and b<nb-3:
        for bt in range(4):
            nn=int(.32*SR); x=np.arange(nn)/SR; fk=48+70*np.exp(-x*28)
            add(np.sin(2*np.pi*np.cumsum(fk)/SR)*np.exp(-x*11),st+bt*BEAT,.5,.30)
            nh=int(.07*SR); hh=rng.standard_normal(nh)*np.exp(-np.arange(nh)/SR*70); hh=np.diff(hh,prepend=0)
            add(hh,st+bt*BEAT+BEAT/2,.6,.035)
# masterização simples
out*=np.minimum(1,t/2.5)[:,None]*np.minimum(1,(D-t)/4.0)[:,None]
out=np.tanh(out*1.6)/np.tanh(1.6); out*=.82/np.abs(out).max()
w=wave.open('musica.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
print('ok',D,'s rms',float(np.sqrt((out**2).mean())))
