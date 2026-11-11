# Trilha original do filme (sintetizada aqui, sem amostra de terceiros). 78 s, 76 bpm, Ré maior.
# Piano com parciais e martelo, colchão de cordas filtrado, baixo, percussão leve e reverberação por convolução.
# Forma: piano só (0-10 s) > entra colchão e baixo (10-26) > percussão leve (26-60) > respiro (60-70) > resolução (70-78).
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 44100; D = 78.0; BPM = 76; BEAT = 60 / BPM; BAR = 4 * BEAT; N = int(SR * D)
rng = np.random.default_rng(7)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
L = np.zeros(N); R = np.zeros(N)
def add(sig, t0, pan=.5, g=1.):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    L[i:i + len(sig)] += sig * g * np.cos(pan * np.pi / 2); R[i:i + len(sig)] += sig * g * np.sin(pan * np.pi / 2)
def lp(x, f, o=2): return sosfilt(butter(o, f / (SR / 2), 'low', output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f / (SR / 2), 'high', output='sos'), x)

def piano(m, dur=3.2, vel=.8):
    f = hz(m); n = int(dur * SR); x = np.arange(n) / SR; s = np.zeros(n); B = .00012
    for k in range(1, 12):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 12000: break
        a = vel ** (1 + k * .18) / k ** 1.1
        dec = 1.2 + k * .9 + f / 900
        s += a * np.sin(2 * np.pi * fk * x + rng.uniform(0, 6.28)) * (np.exp(-x * dec) * .82 + np.exp(-x * dec * .18) * .18)
    att = np.minimum(1, x / .004); rel = np.minimum(1, (dur - x) / .25)
    ham = lp(rng.standard_normal(n) * np.exp(-x * 90), 3000) * .06 * vel
    return (s * att * rel + ham) * .55

def pad(ms, dur):
    n = int(dur * SR); x = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        for det in (-.11, .0, .13):
            f = hz(m) * (1 + det / 100)
            ph = (f * x + rng.uniform()) % 1
            s += (2 * ph - 1) * .22          # serra
    s = lp(s, 1500, 4)
    env = np.minimum(1, x / 1.4) * np.minimum(1, (dur - x) / 1.8)
    return s * env * (.85 + .15 * np.sin(2 * np.pi * x / 6))

def bass(m, dur):
    n = int(dur * SR); x = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * x) + .25 * np.sin(2 * np.pi * 2 * f * x) + .08 * np.sin(2 * np.pi * 3 * f * x)
    return s * np.minimum(1, x / .03) * np.exp(-x * .5) * np.minimum(1, (dur - x) / .3)

def kick():
    n = int(.4 * SR); x = np.arange(n) / SR; f = 46 + 60 * np.exp(-x * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 9)
def shaker():
    n = int(.09 * SR); x = np.arange(n) / SR
    return hp(rng.standard_normal(n), 6000) * np.exp(-x * 55)
def rim():
    n = int(.06 * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * x) * .5 + hp(rng.standard_normal(n), 2500) * .5) * np.exp(-x * 80)

# progressão: Dmaj9  Bm11  Gmaj9  Asus4-A
CH = [dict(b=38, v=[57, 61, 64, 66, 69]), dict(b=35, v=[54, 57, 61, 64, 66]), dict(b=43, v=[55, 59, 62, 66, 69]), dict(b=45, v=[57, 62, 64, 69, 71])]
MEL = [[78, 76, 73, 0], [74, 73, 69, 0], [71, 74, 76, 0], [76, 73, 74, 0]]   # motivo em semínimas, 0 = pausa
nb = int(np.ceil(D / BAR))
for b in range(nb):
    t0 = b * BAR; c = CH[b % 4]; sec = t0 / D
    # piano: acorde quebrado em colcheias
    pat = [0, 2, 1, 3, 2, 4, 3, 2]
    vel = .55 if t0 < 10 else .7
    if t0 < 70 or t0 < D - 2:
        for k, i in enumerate(pat):
            add(piano(c['v'][i], 2.6, vel * (1 if k % 2 == 0 else .8)), t0 + k * BEAT / 2 + rng.normal(0, .004), .35 + .3 * (i / 4), .9)
    # melodia a partir de 10 s, pausa no respiro
    if 10 <= t0 < 60 or 70 <= t0 < D - 4:
        for k, m in enumerate(MEL[b % 4]):
            if m: add(piano(m, 3.0, .85), t0 + k * BEAT + rng.normal(0, .004), .55, .8)
    # colchão e baixo a partir de 10 s
    if t0 >= 9:
        add(pad(c['v'][:4], BAR + 1.6), t0, .5, .11 if t0 < 26 else .14)
        add(bass(c['b'], BAR * .95), t0, .5, .30)
        add(bass(c['b'], BEAT * 1.5), t0 + 2.5 * BEAT, .5, .18)
    # percussão leve de 26 a 60 s e de 70 até o fim
    if 26 <= t0 < 60 or 70 <= t0 < D - 3:
        for q in range(4):
            if q in (0, 2): add(kick(), t0 + q * BEAT, .5, .32)
            if q in (1, 3): add(rim(), t0 + q * BEAT, .58, .05)
            add(shaker(), t0 + q * BEAT + BEAT / 2, .68, .045)
            add(shaker(), t0 + q * BEAT + BEAT * .75, .32, .025)
# acorde final, longo
for m in [50, 57, 61, 64, 66, 69]: add(piano(m, 6.0, .7), D - 6.2, .5, .8)

dry = np.stack([L, R], 1)
# reverberação: resposta de sala de 2,6 s, filtrada, estéreo
n = int(2.6 * SR); x = np.arange(n) / SR
ir = np.stack([lp(rng.standard_normal(n), 5000) * np.exp(-x * 2.6) for _ in range(2)], 1); ir[:int(.012 * SR)] = 0; ir /= np.abs(ir).sum(0) ** .5 * 4
wet = np.stack([fftconvolve(dry[:, ch], ir[:, ch])[:N] for ch in range(2)], 1)
out = hp(dry[:, 0], 30)[:, None] * 0 + dry * .78 + wet * .32
out = np.stack([hp(out[:, ch], 30) for ch in range(2)], 1)
t = np.arange(N) / SR
out *= (np.minimum(1, t / 1.5) * np.minimum(1, (D - t) / 3.0))[:, None]
out = np.tanh(out * 1.3 / np.abs(out).max()) ; out *= .9 / np.abs(out).max()
w = wave.open('musica2.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
print('ok', D, 's')
