# Lofts (Angra dos Reis): modelo montado SÓ com as cotas das pranchas P01 e P02 de arquitetura (projeto legal / executivo).
# P01: locação (lote 30 x 12, lofts de 4,55 de frente com 3,00 entre eles, corredor de piso drenante de 2,85 junto à divisa norte,
#      palmeiras e agaves na faixa de jardim), planta do térreo (4,55 x 5,65, paredes de 0,15, projeção da laje 0,70 à frente,
#      parede de ala no lado da rua avançando 0,70), quadro de esquadrias (P01 pivotante 1,20 x 2,20; J01 1,00 x 0,40 p1,40;
#      J02 0,60 x 0,60 p1,50; J03 1,50 x 0,40 p1,30; J04 0,30 x 4,40 p0,70; J05 2,00 x 0,60 p1,50).
# P02: fachadas e cortes (altura 6,03; marquise de 0,10 a +3,05, i 3%; parede de ala até 3,15; níveis +0,15, +2,90, +5,40;
#      pintura branco gelo). Palmeiras (~6,5 m) e agaves (~1,2 m) com o porte desenhado nas fachadas.
# Eixos: X do fundo do lote (0) para a rua (30); Y da divisa norte (0) para a sul (12); z altura. Fachadas dos lofts para o norte.
import bpy, bmesh, math, sys, mathutils, random
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = A[0] if A else '/tmp/lofts2.png'
RW, RH, SPP = (int(A[1]), int(A[2]), int(A[3])) if len(A) > 3 else (1200, 800, 32)
VIEW = A[4] if len(A) > 4 else 'persp'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -0.6
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0., sss=0.):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m
    if sss: b.inputs['Subsurface Weight'].default_value = sss
    return M
def ruido(M, esc, a, b, bump=.1, det=10):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
gelo = mat('branco-gelo', (238, 237, 233), .85); ruido(gelo, 90, (231, 230, 226), (243, 242, 238), .04)
madeira = mat('porta-madeira', (92, 66, 46), .5); ruido(madeira, 6, (80, 56, 38), (104, 76, 54), .02, 3)
inox = mat('inox', (200, 200, 198), .25, 1.)
alu = mat('aluminio', (40, 40, 42), .4, .6)
vidro = mat('vidro', (30, 36, 40), .05, .3)
calc = mat('calcada', (206, 203, 196), .85); ruido(calc, 60, (196, 193, 186), (214, 211, 204), .06)
drenante = mat('piso-drenante', (150, 150, 146), .9); ruido(drenante, 25, (128, 130, 124), (164, 164, 158), .25)
grama = mat('grama', (92, 118, 70), .95); ruido(grama, 300, (80, 104, 62), (104, 128, 80), .15, 14)
muro = mat('muro', (232, 230, 225), .9); ruido(muro, 70, (224, 222, 217), (238, 236, 231), .05)
def box(n, x0, x1, y0, y1, z0, z1, M):
    y0, y1 = -y1, -y0      # cotas em Y da planta (da divisa norte para o sul); no Blender o norte é +Y (sem espelhar)
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.name = n; o.data.materials.append(M); return o
W, D, H = 4.55, 5.65, 6.03
YF = 4.20 + .70          # projeção da laje (0,70) começa na faixa de jardim; fachada a 4,90 da divisa norte
def janela(face, a, b, z0, z1):   # face: 'O' (oeste, x0), 'L' (leste, x1), 'S' (fundos, y1); a-b ao longo da face
    if face in 'OL':
        x = X0 if face == 'O' else X1; s = -1 if face == 'O' else 1
        box('caix', x - .01 * s if s > 0 else x - .03, x + .03 if s > 0 else x + .01, a, b, z0, z1, alu)
        box('vid', x + .02 * s - .005, x + .02 * s + .005, a + .04, b - .04, z0 + .04, z1 - .04, vidro)
    else:
        y = YF + D
        box('caix', a, b, y - .01, y + .03, z0, z1, alu); box('vid', a + .04, b - .04, y + .015, y + .025, z0 + .04, z1 - .04, vidro)
for k, X0 in enumerate((3.55, 11.10, 18.65)):
    X1 = X0 + W
    box('calcada', X0 - .70, X1 + .70, YF - .70, YF + D + .70, -.02, .10, calc)
    box('loft', X0, X1, YF, YF + D, 0, H, gelo)
    box('rufo', X0 - .03, X1 + .03, YF - .03, YF + D + .03, H, H + .03, mat('rufo%d' % k, (220, 219, 216), .4, .4))
    box('marquise', X0, X1, YF - .70, YF, 3.05, 3.15, gelo)                 # laje projetada 0,70, i 3%
    box('ala', X1 - .15, X1 - .001, YF - .699, YF, 0, 3.05, gelo)            # parede de ala do lado da rua (sob a marquise: total 3,15)
    # porta pivotante P01 1,20 x 2,20, a 1,18 m da face leste (fachada frontal), sobre o piso +0,15
    box('batente', X1 - 2.42, X1 - 1.14, YF - .02, YF + .01, .13, 2.39, alu)
    box('porta', X1 - 2.38, X1 - 1.18, YF - .04, YF + .02, .15, 2.35, madeira)
    box('puxador', X1 - 2.20, X1 - 2.17, YF - .10, YF - .06, .55, 1.95, inox)
    janela('L', YF + 1.17, YF + 2.67, 1.50, 1.90)                              # J03 cozinha
    janela('O', YF + .40, YF + .70, .85, 5.25)                                 # J04 faixa vertical
    janela('O', YF + 4.15, YF + 4.75, 1.65, 2.25)                              # J02 banho
    janela('S', X0 + 2.65, X0 + 3.65, 1.55, 1.95)                              # J01
    janela('S', X0 + 1.25, X0 + 3.25, 4.40, 5.00)                              # J05 mezanino
# lote 30 x 12: corredor de piso drenante junto à divisa norte, jardim, muros de divisa, muro da fachada e reservatório
box('gramado', .25, 24.55, .25, 11.75, -.03, 0, grama)
box('corredor', .25 + 2.85, 24.55, .25, 3.35, -.02, .012, drenante)
for xa in (4.75, 12.30, 19.85):
    box('pisada', xa, xa + 1.80, 3.35, YF - .70, -.02, .012, drenante)
box('divisa-n', 0, 30, 0, .25, 0, 2.20, muro); box('divisa-s', 0, 30, 11.75, 12, 0, 2.20, muro); box('fundo', 0, .25, 0, 12, 0, 2.20, muro)
box('muro-fachada', 24.55, 24.75, 3.35, 12, 0, 2.20, muro)
box('reservatorio', .25, 2.60, 8.60, 11.75, 0, 2.30, muro)
box('chao', -40, 70, -40, 60, -.06, -.05, mat('terreno', (150, 146, 136), .95))
# paisagismo: palmeiras e agaves nas posições da locação
folha = mat('folha', (66, 92, 48), .6, 0, .2); tronco = mat('tronco', (150, 146, 138), .8); ruido(tronco, 40, (138, 134, 126), (160, 156, 148), .3)
palmito = mat('palmito', (96, 120, 70), .6); agave_m = mat('agave', (84, 108, 92), .5, 0, .1)
def fronde(bm, base, ang, inc, L, rnd):
    # ráquis arqueada e folíolos estreitos (3 cm) e caídos, como a palmeira-imperial desenhada nas fachadas
    N = 40; pts = []
    for i in range(N + 1):
        s = L * i / N
        pts.append(base + mathutils.Vector((math.cos(ang) * math.cos(inc) * s, math.sin(ang) * math.cos(inc) * s, math.sin(inc) * s - .55 * (s / L) ** 2 * L)))
    side = mathutils.Vector((-math.sin(ang), math.cos(ang), 0))
    for i in range(3, N):
        p = pts[i]; t = i / N; ll = .62 * math.sin(math.pi * min(1, .15 + t * .95)) + .06
        fw = (pts[i + 1] - p).normalized()
        for sg in (-1, 1):
            d = (side * sg * .75 + mathutils.Vector((0, 0, -.65)) + fw * .35).normalized()
            for k in range(2):
                q = p + fw * (k * .03)
                tip = q + d * ll * rnd.uniform(.85, 1.1); w = fw * .016
                vs = [bm.verts.new(q - w), bm.verts.new(q + w), bm.verts.new(q + d * ll * .5 + w * .9), bm.verts.new(tip), bm.verts.new(q + d * ll * .5 - w * .9)]
                bm.faces.new(vs)
def palmeira(x, y, h=6.5, seed=0):
    rnd = random.Random(seed)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=.24, radius2=.16, depth=h - 3.0, location=(x, y, (h - 3.0) / 2)); t = bpy.context.object; t.data.materials.append(tronco)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=.17, depth=1.1, location=(x, y, h - 3.0 + .55)); c = bpy.context.object; c.data.materials.append(palmito)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.17, location=(x, y, h - 3.0 + 1.1)); e = bpy.context.object; e.scale.z = .8; e.data.materials.append(palmito)
    me = bpy.data.meshes.new('copa'); bm = bmesh.new(); base = mathutils.Vector((x, y, h - 1.85))
    for i in range(16):
        ang = i * 2.4 + rnd.uniform(-.2, .2); inc = math.radians(rnd.uniform(15, 60)); fronde(bm, base, ang, inc, rnd.uniform(2.4, 3.0), rnd)
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('copa', me); bpy.context.collection.objects.link(o); o.data.materials.append(folha)
def agave(x, y, r=.75, seed=0):
    rnd = random.Random(seed); me = bpy.data.meshes.new('agave'); bm = bmesh.new()
    for i in range(26):
        ang = i * 2.4 + rnd.uniform(-.1, .1); inc = math.radians(rnd.uniform(25, 70)); L = r * rnd.uniform(.8, 1.2) * (1.6 if inc > 1 else 1)
        d = mathutils.Vector((math.cos(ang) * math.cos(inc), math.sin(ang) * math.cos(inc), math.sin(inc)))
        sd = mathutils.Vector((-math.sin(ang), math.cos(ang), 0)) * .09
        b0 = mathutils.Vector((x, y, .02)); tip = b0 + d * L
        vs = [bm.verts.new(b0 - sd), bm.verts.new(b0 + sd), bm.verts.new(b0 + d * L * .5 + sd * 1.3 + mathutils.Vector((0, 0, .04))), bm.verts.new(tip), bm.verts.new(b0 + d * L * .5 - sd * 1.3 + mathutils.Vector((0, 0, .04)))]
        bm.faces.new(vs)
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('agave', me); bpy.context.collection.objects.link(o); o.data.materials.append(agave_m)
for i, px in enumerate((1.5, 9.1, 16.7, 24.0)): palmeira(px, -3.85, 6.5, i)
for i, ax in enumerate((4.1, 11.8, 19.3)): agave(ax, -3.95, .7, 10 + i); agave(ax + .7, -3.80, .6, 20 + i)
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(40); sky.sun_rotation = math.radians(float(A[9]) if len(A) > 9 else 120)
sky.sun_intensity = .5; nw.nodes['Background'].inputs['Strength'].default_value = .3; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
if VIEW in ('ortho', 'ortho-l'):
    cam.data.type = 'ORTHO'
    for n in ('divisa-n',): bpy.data.objects[n].hide_render = True
    for o in bpy.data.objects:
        if o.name.startswith(('copa', 'agave', 'Cone', 'Cylinder', 'Sphere')): o.hide_render = True
    if VIEW == 'ortho':   # fachada frontal do loft 2, olhando para o sul
        cam.data.ortho_scale = 7.5; cam.location = (11.10 + W / 2, 20, 3.0); cam.rotation_euler = (math.radians(90), 0, math.radians(180))
    else:                 # fachada lateral do lado da rua (leste) do loft 3, olhando para o oeste
        bpy.data.objects['muro-fachada'].hide_render = True
        cam.data.ortho_scale = 8.0; cam.location = (40, -(YF + D / 2 - .35), 3.0); cam.rotation_euler = (math.radians(90), 0, math.radians(90))
else:
    cx, cy, f = (float(A[5]), float(A[6]), float(A[7])) if len(A) > 7 else (19.2, .7, 18.0)
    cam.location = (cx, -cy, 1.60); cam.data.lens = f; cam.data.sensor_width = 36
    tg = mathutils.Vector((float(A[8]) if len(A) > 8 else 12.8, -5.5, 1.60)); cam.rotation_euler = (tg - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.shift_y = .13
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
