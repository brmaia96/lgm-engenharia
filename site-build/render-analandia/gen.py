# Render por IA a partir de uma imagem de referência (modelo 3D). uso: python3 gen.py <ref.png> <prompt.txt> <saida.png> [modelo]
import sys, json, base64, urllib.request, os, ssl
ref, pfile, out = sys.argv[1:4]; model = sys.argv[4] if len(sys.argv) > 4 else 'google/gemini-3-pro-image'
b64 = base64.b64encode(open(ref, 'rb').read()).decode()
body = {'model': model, 'modalities': ['image', 'text'],
        'messages': [{'role': 'user', 'content': [{'type': 'text', 'text': open(pfile).read()},
                                                  {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + b64}}]}]}
ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt')
proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
op = urllib.request.build_opener(urllib.request.ProxyHandler({'https': proxy}) if proxy else urllib.request.ProxyHandler(), urllib.request.HTTPSHandler(context=ctx))
rq = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                            headers={'Authorization': 'Bearer proxy-injected', 'Content-Type': 'application/json'})
try: r = json.load(op.open(rq, timeout=300))
except urllib.error.HTTPError as e: print('HTTP', e.code, e.read()[:600]); sys.exit(1)
m = r['choices'][0]['message']; imgs = m.get('images') or []
if not imgs: print('sem imagem:', json.dumps(r)[:800]); sys.exit(1)
u = imgs[0]['image_url']['url']; open(out, 'wb').write(base64.b64decode(u.split(',', 1)[1])); print('ok', out, r.get('usage', {}).get('cost'))
