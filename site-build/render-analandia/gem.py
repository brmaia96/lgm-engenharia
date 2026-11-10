# Render por IA com o Gemini (chave do Google AI Studio injetada pelo proxy). uso: python3 gem.py <ref> <prompt.txt> <saida.png> [modelo]
import sys, json, base64, urllib.request, os, ssl, re
ref, pfile, out = sys.argv[1:4]; model = sys.argv[4] if len(sys.argv) > 4 else 'gemini-3-pro-image'
mime = 'image/png' if ref.lower().endswith('.png') else 'image/jpeg'
b64 = base64.b64encode(open(ref, 'rb').read()).decode()
body = {'model': model, 'modalities': ['text', 'image'],
        'messages': [{'role': 'user', 'content': [{'type': 'text', 'text': open(pfile).read()},
                                                  {'type': 'image_url', 'image_url': {'url': 'data:%s;base64,%s' % (mime, b64)}}]}]}
ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt')
proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
op = urllib.request.build_opener(urllib.request.ProxyHandler({'https': proxy}) if proxy else urllib.request.ProxyHandler(), urllib.request.HTTPSHandler(context=ctx))
rq = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', data=json.dumps(body).encode(),
                            headers={'Authorization': 'Bearer proxy-injected', 'Content-Type': 'application/json'})
try: raw = op.open(rq, timeout=400).read()
except urllib.error.HTTPError as e: print('HTTP', e.code, e.read()[:700]); sys.exit(1)
r = json.loads(raw); m = r['choices'][0]['message']
data = None
for im in (m.get('images') or []):
    u = im.get('image_url', {}).get('url', '')
    if u.startswith('data:'): data = u.split(',', 1)[1]
c = m.get('content')
if not data and isinstance(c, list):
    for p in c:
        u = (p.get('image_url') or {}).get('url', '') if isinstance(p, dict) else ''
        if u.startswith('data:'): data = u.split(',', 1)[1]
if not data and isinstance(c, str):
    g = re.search(r'data:image/[a-z]+;base64,([A-Za-z0-9+/=]+)', c)
    if g: data = g.group(1)
if not data:
    s = json.dumps(r); print('sem imagem; chaves:', list(m.keys()), s[:500]); sys.exit(1)
open(out, 'wb').write(base64.b64decode(data)); print('ok', out, r.get('usage'))
