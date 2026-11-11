# Casa da Raia: modelo montado com as cotas das pranchas do executivo (planta, cobertura, cortes e fachadas) e renderizado no Cycles.
# Eixos: x ao longo da rua (0 a 20 m, esquerda para a direita como na planta), y da rua para os fundos (0 a 20 m), z altura.
# Medidas: cobertura 16,75 x 11,05 m (x 2,25-19,00; y 3,45-14,50), cumeeira +5,15 em y 7,25, águas a 30%; torre 3,00 x 3,00 m;
# vidro retrátil x 0,15-2,25 / y 7,25-11,87; garagem em sanduíche x 0,15-7,55; piscina 18,00 x 2,26 m com escada em baia.
import bpy, bmesh, math, sys, mathutils
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = A[0] if A else '/tmp/raia.png'
RW, RH, SPP = (int(A[1]), int(A[2]), int(A[3])) if len(A) > 3 else (1200, 800, 32)
VIEW = A[4] if len(A) > 4 else 'persp'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -0.6
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0., t=0., ior=1.45):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m
    b.inputs['Transmission Weight'].default_value = t; b.inputs['IOR'].default_value = ior; return M
def ruido(M, esc, a, b, bump=.15, det=10):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
reboco = mat('reboco', (238, 236, 231), .85); ruido(reboco, 90, (232, 230, 225), (242, 240, 236), .05)
telha = mat('telha', (176, 104, 74), .7)
# telha cerâmica: ondulação ao longo da água (Wave) para ler a capa e canal
nt = telha.node_tree; bs = nt.nodes['Principled BSDF']; wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = 1.0
tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.0, 2.6, 0.0)
nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
bmp = nt.nodes.new('ShaderNodeBump'); bmp.inputs['Strength'].default_value = .6; nt.links.new(wv.outputs['Fac'], bmp.inputs['Height']); nt.links.new(bmp.outputs['Normal'], bs.inputs['Normal'])
nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; cr = nt.nodes.new('ShaderNodeValToRGB')
cr.color_ramp.elements[0].color = (*lin((160, 92, 64)), 1); cr.color_ramp.elements[1].color = (*lin((190, 116, 84)), 1)
nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
madeira = mat('beiral', (96, 64, 44), .6)
sand = mat('sanduiche', (196, 198, 200), .45, .6)
caix = mat('esquadria', (38, 38, 40), .35, .7)
vidro = mat('vidro', (160, 176, 182), .0, 0., 1., 1.52)
vidroesc = mat('vidro-esc', (30, 36, 40), .05, .2)
deck = mat('deck', (206, 200, 188), .6); ruido(deck, 25, (196, 190, 178), (214, 208, 196), .08)
grama = mat('grama', (78, 112, 52), .9); ruido(grama, 220, (62, 96, 40), (96, 130, 64), .35, 15)
muro = mat('muro', (214, 210, 202), .9); ruido(muro, 70, (204, 200, 192), (222, 218, 210), .06)
azulejo = mat('pastilha', (80, 170, 196), .15); agua = mat('agua', (150, 214, 226), .02, 0., 1., 1.33)
cerca = mat('cerca-viva', (58, 92, 40), .8); ruido(cerca, 14, (40, 70, 28), (86, 124, 56), 1.2, 16)
metal = mat('chamine', (150, 152, 154), .4, .8)

def box(n, x0, x1, y0, y1, z0, z1, M):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.name = n; o.data.materials.append(M); return o
RY, RZ, SL = 7.25, 5.15, .30
def zroof(y): return RZ - SL * abs(y - RY)
def wall(n, x0, x1, y0, y1, M=reboco, under=.14):
    # bloco de parede com o topo seguindo o telhado (gera o oitão onde passa a cumeeira)
    ys = [y0] + ([RY] if y0 < RY < y1 else []) + [y1]
    bm = bmesh.new(); bot = []; top = []
    for x in (x0, x1):
        for y in ys:
            bot.append(bm.verts.new((x, y, 0))); top.append(bm.verts.new((x, y, zroof(y) - under)))
    n_ = len(ys)
    def q(a, b, c, d): bm.faces.new((a, b, c, d))
    for i in range(n_ - 1):
        q(bot[i], bot[i + 1], top[i + 1], top[i]); q(bot[n_ + i + 1], bot[n_ + i], top[n_ + i], top[n_ + i + 1])
        q(top[i], top[i + 1], top[n_ + i + 1], top[n_ + i]); q(bot[i + 1], bot[i], bot[n_ + i], bot[n_ + i + 1])
    q(bot[0], top[0], top[n_], bot[n_]); q(bot[n_ - 1], bot[2 * n_ - 1], top[2 * n_ - 1], top[n_ - 1])
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); me.materials.append(M); o = bpy.data.objects.new(n, me); bpy.context.collection.objects.link(o); return o
def slab(n, pts, th, M):
    bm = bmesh.new(); vs = [bm.verts.new(p) for p in pts]; f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f]); bmesh.ops.translate(bm, vec=(0, 0, -th), verts=[v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); me.materials.append(M); o = bpy.data.objects.new(n, me); bpy.context.collection.objects.link(o); return o

# ---- volumes (planta) ----
wall('cozinha-estar', 3.21, 12.72, 8.11, 12.93)
wall('lavabo-banho', 9.06, 12.72, 12.93, 14.41)
wall('closet-suite', 12.72, 17.80, 10.95, 14.41)
wall('banhos-circ', 12.72, 17.80, 7.90, 10.95)
wall('dormitorios', 7.85, 17.80, 5.26, 7.90)
wall('despensa-hall', 3.21, 7.85, 5.26, 8.11)
box('lavanderia', .15, 3.21, 5.26, 8.11, 0, 3.0, reboco)
# ---- telhado de duas águas, beiral e torre ----
X0, X1, YF, YB = 2.25, 19.00, 3.45, 14.50
slab('agua-frente', [(X0, YF, zroof(YF)), (X1, YF, zroof(YF)), (X1, RY, RZ), (X0, RY, RZ)], -.10, telha)
slab('agua-fundos', [(X0, RY, RZ), (X1, RY, RZ), (X1, YB, zroof(YB)), (X0, YB, zroof(YB))], -.10, telha)
box('cumeeira', X0, X1, RY - .12, RY + .12, RZ - .02, RZ + .10, telha)
for y,sg in ((YF,-1),(YB,1)): box('testeira', X0 - .02, X1 + .02, y + sg * .0 - .03, y + sg * .0 + .03, zroof(y) - .20, zroof(y) + .06, madeira)
for x in (X0, X1): pass
box('torre', 15.05, 18.05, 7.25, 10.25, 2.5, 5.85, reboco); box('torre-topo', 14.95, 18.15, 7.15, 10.35, 5.85, 5.93, sand)
bpy.ops.mesh.primitive_cylinder_add(radius=.13, depth=1.0, location=(3.7, 11.9, 4.2)); ch = bpy.context.object; ch.data.materials.append(metal)
# garagem (telha sanduíche a 5%) e cobertura de vidro retrátil
box('garagem-cob', .15, 7.55, .55, 7.25, 3.05, 3.17, sand)
box('vidro-cob', .15, 2.25, 7.25, 11.87, 3.14, 3.17, vidro)
for y in (7.25, 8.79, 10.33, 11.87): box('perfil', .15, 2.25, y - .04, y + .04, 3.12, 3.2, caix)
for x in (.15, 1.45, 2.25): box('perfil', x - .04, x + .04, 7.25, 11.87, 3.12, 3.2, caix)
for x in (.2, 2.2):
    for y in (7.3, 11.8): box('pilar', x - .05, x + .05, y - .05, y + .05, 0, 3.15, caix)
# ---- esquadrias da fachada dos fundos (cotas da planta) ----
def janela(x0, x1, z0, z1, y, folhas=2, porta=False):
    box('vidro', x0, x1, y - .01, y + .03, z0, z1, vidroesc)
    t = .05
    for a, b, c, d in ((x0, x1, z0, z0 + t), (x0, x1, z1 - t, z1), (x0, x0 + t, z0, z1), (x1 - t, x1, z0, z1)): box('caix', a, b, y, y + .06, c, d, caix)
    for k in range(1, folhas): xm = x0 + (x1 - x0) * k / folhas; box('caix', xm - .025, xm + .025, y, y + .06, z0, z1, caix)
# cadeia de cotas da fachada dos fundos, a partir da parede em x = 3,21: 1,18 | 4,57 | 1,06 | 0,80 | 1,11 | 0,80 | 1,14 | 1,50 | 2,51
janela(4.39, 8.96, 0, 2.50, 12.93, 4, True)          # porta de correr de quatro folhas do estar
janela(10.02, 10.82, 0, 2.10, 14.41, 1, True)        # porta do lavabo
janela(11.93, 12.73, 1.60, 2.10, 14.41)              # janela alta do banho social
janela(13.87, 15.37, 1.10, 2.10, 14.41)              # janela de duas folhas da suíte
# lateral direita: dois banhos (janelas altas) e dormitório 02
def jlat(y0, y1, z0, z1, x=17.80):
    box('vidro', x - .01, x + .03, y0, y1, z0, z1, vidroesc)
    for a, b, c, d in ((y0, y1, z0, z0 + .05), (y0, y1, z1 - .05, z1), (y0, y0 + .05, z0, z1), (y1 - .05, y1, z0, z1)): box('caix', x, x + .06, a, b, c, d, caix)
jlat(9.2, 9.8, 1.6, 2.2); jlat(8.15, 8.75, 1.6, 2.2); jlat(6.0, 7.4, 1.0, 2.2)
# ---- lote: deck, grama, piscina em raia, cerca viva e muros de divisa ----
box('deck', .15, 19.85, 8.11, 14.85, -.05, 0, deck); box('deck2', .15, 1.15, 14.85, 19.85, -.05, 0, deck)
box('grama-lat', 17.8, 19.85, 5.0, 8.11, -.05, -.01, grama)
box('grama-fundo', 3.45, 19.85, 15.5, 16.65, -.05, -.01, grama)
box('borda-f', 1.15, 19.65, 16.65, 16.90, -.05, .02, deck); box('borda-t', 1.15, 19.65, 19.16, 19.35, -.05, .02, deck)
box('borda-e', 1.15, 1.40, 15.0, 19.35, -.05, .02, deck); box('borda-d', 19.40, 19.65, 16.65, 19.35, -.05, .02, deck)
box('borda-baia', 3.20, 3.45, 15.0, 16.90, -.05, .02, deck); box('borda-baia2', 1.15, 3.45, 14.85, 15.10, -.05, .02, deck)
box('pastilha', 1.40, 19.40, 16.90, 19.16, -1.40, -.02, azulejo)
box('agua', 1.40, 19.40, 16.90, 19.16, -1.40, -.04, agua)
box('baia', 1.40, 3.20, 15.10, 16.90, -.60, -.02, azulejo); box('agua-baia', 1.40, 3.20, 15.10, 16.90, -.60, -.04, agua)
# cerca viva: doze arbustos ao longo do muro dos fundos, como na prancha
import random; random.seed(4)
for k in range(12):
    x = 2.8 + k * 1.4
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=.8, location=(x, 19.5, .85)); o = bpy.context.object
    o.scale = (.95, .45, 1.15); o.data.materials.append(cerca)
    d = o.modifiers.new('disp', 'DISPLACE'); t = bpy.data.textures.new('cv%d' % k, 'VORONOI'); t.noise_scale = .09; d.texture = t; d.strength = .12
    bpy.ops.object.shade_smooth()
for a in ((0, .15, 0, 20), (19.85, 20.0, 0, 20), (0, 20, 19.85, 20.0)):
    box('muro', a[0], a[1], a[2], a[3], 0, 2.2, muro)
box('chao', -20, 40, -20, 40, -.06, -.05, grama)
# ---- céu físico e câmera ----
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(34); sky.sun_rotation = math.radians(290)
sky.sun_intensity = .5; nw.nodes['Background'].inputs['Strength'].default_value = .3; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
if VIEW == 'ortho':          # vista ortogonal dos fundos, para sobrepor à Fachada Posterior da prancha
    for o in [o for o in bpy.data.objects if o.name.startswith(('muro', 'cerca', 'Cube'))]: o.hide_render = True
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 22; cam.location = (10, 40, 3.0); cam.rotation_euler = (math.radians(90), 0, math.radians(180))
else:
    cx, cy, f = (float(A[5]), float(A[6]), float(A[7])) if len(A) > 7 else (2.6, 19.5, 17.0)
    cam.location = (cx, cy, 1.6); cam.data.lens = f; cam.data.sensor_width = 36
    tg = mathutils.Vector((float(A[8]) if len(A) > 8 else 12.0, float(A[9]) if len(A) > 9 else 11.0, 2.3)); cam.rotation_euler = (tg - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.shift_y = .05
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
