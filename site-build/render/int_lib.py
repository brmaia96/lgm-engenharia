# Base comum das internas (Lofts, Casa Garça): Cycles, materiais neutros, paredes com vãos, câmera na altura do olho.
# Coordenadas da planta: x da esquerda para a direita, y de cima para baixo (como na prancha); no Blender X = x, Y = -y (sem espelhar).
import bpy, bmesh, math, sys, mathutils
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = A[0] if A else '/tmp/int.png'
RW, RH, SPP = (int(A[1]), int(A[2]), int(A[3])) if len(A) > 3 else (900, 600, 64)
VIEW = A[4] if len(A) > 4 else 'a'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 10; sc.cycles.diffuse_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.transparent_max_bounces = 8
sc.cycles.sample_clamp_indirect = 6.0; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = .03
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0., alpha=None, trans=0.):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m
    if trans: b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = 1.45
    return M
def ruido(M, esc, a, b, bump=.1, det=10):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
def veio(M, esc, a, b):   # madeira: ondas esticadas
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1, 1, 14); nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = esc * 2.5; wv.inputs['Distortion'].default_value = 1.2; wv.inputs['Detail'].default_value = 4
    nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(wv.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
def piso_placas(M, tam, a, b, junta=(150, 146, 140)):
    # porcelanato em placas: tom levemente variado por placa e junta fina
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tc = nt.nodes.new('ShaderNodeTexCoord')
    br = nt.nodes.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 1 / tam; br.inputs['Mortar Size'].default_value = .0025 / tam
    br.offset = 0; br.squash = 1; br.inputs['Color1'].default_value = (*lin(a), 1); br.inputs['Color2'].default_value = (*lin(b), 1)
    br.inputs['Mortar'].default_value = (*lin(junta), 1); br.inputs['Brick Width'].default_value = 1; br.inputs['Row Height'].default_value = 1
    nt.links.new(tc.outputs['Object'], br.inputs['Vector']); nt.links.new(br.outputs['Color'], bs.inputs['Base Color'])
OBJ = []
def box(n, x0, x1, y0, y1, z0, z1, M):
    Y0, Y1 = -y1, -y0
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (Y0 + Y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, Y1 - Y0, z1 - z0); o.name = n; o.data.materials.append(M)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); OBJ.append(o); return o
def parede(n, eixo, c0, c1, u0, u1, z0, z1, M, vaos=()):
    # parede ao longo de 'x' (c0-c1 = faixa em y) ou de 'y' (c0-c1 = faixa em x), de u0 a u1, com vãos (a, b, za, zb)
    us = sorted({u0, u1, *[v for a, b, _, _ in vaos for v in (a, b)]}); zs = sorted({z0, z1, *[v for _, _, za, zb in vaos for v in (za, zb)]})
    us = [u for u in us if u0 <= u <= u1]; zs = [z for z in zs if z0 <= z <= z1]
    for i in range(len(us) - 1):
        for j in range(len(zs) - 1):
            um, zm = (us[i] + us[i + 1]) / 2, (zs[j] + zs[j + 1]) / 2
            if any(a < um < b and za < zm < zb for a, b, za, zb in vaos): continue
            if eixo == 'x': box(n, us[i], us[i + 1], c0, c1, zs[j], zs[j + 1], M)
            else: box(n, c0, c1, us[i], us[i + 1], zs[j], zs[j + 1], M)
alu_e = mat('alu-esquadria', (46, 46, 48), .35, .7)
vidro_m = mat('vidro', (235, 240, 240), .02, 0., trans=1.)
def janela(eixo, c, a, b, za, zb, folhas=2):
    # caixilho de alumínio com vidro no plano c (y se eixo 'x', x se eixo 'y'), vão a-b, za-zb
    t = .045
    def bx(u0, u1, w0, w1, z0, z1, M):
        if eixo == 'x': box('jan', u0, u1, w0, w1, z0, z1, M)
        else: box('jan', w0, w1, u0, u1, z0, z1, M)
    bx(a, b, c - .03, c + .03, za, za + t, alu_e); bx(a, b, c - .03, c + .03, zb - t, zb, alu_e)
    bx(a, a + t, c - .03, c + .03, za, zb, alu_e); bx(b - t, b, c - .03, c + .03, za, zb, alu_e)
    for k in range(1, folhas): m = a + (b - a) * k / folhas; bx(m - .02, m + .02, c - .03, c + .03, za, zb, alu_e)
    bx(a + t, b - t, c - .006, c + .006, za + t, zb - t, vidro_m)
def portal(eixo, c, a, b, za, zb, fora):
    # light portal no vão (ajuda o Cycles a trazer o céu para dentro); 'fora' = +1/-1 lado de fora em c
    if eixo == 'x':
        loc = ((a + b) / 2, -(c + .08 * fora), (za + zb) / 2); rot = (math.radians(90), 0, 0) if fora > 0 else (math.radians(-90), 0, 0)
        sx, sy = b - a, zb - za
    else:
        loc = (c + .08 * fora, -(a + b) / 2, (za + zb) / 2); rot = (0, math.radians(90), 0) if fora > 0 else (0, math.radians(-90), 0)
        sx, sy = zb - za, b - a
    bpy.ops.object.light_add(type='AREA', location=loc, rotation=rot); L = bpy.context.object
    L.data.shape = 'RECTANGLE'; L.data.size = sx; L.data.size_y = sy; L.data.cycles.is_portal = True
def ceu(elev=38, rot=200, forca=.35):
    w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
    sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(elev); sky.sun_rotation = math.radians(rot)
    sky.sun_intensity = .45; nw.nodes['Background'].inputs['Strength'].default_value = forca; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
def camera(x, y, z, tx, ty, tz, lente=24, shift_y=0., shift_x=0., expo=0.):
    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
    cam.location = (x, -y, z); cam.data.lens = lente; cam.data.sensor_width = 36; cam.data.sensor_fit = 'HORIZONTAL'
    d = mathutils.Vector((tx, -ty, z)) - cam.location   # alvo na mesma altura: verticais retas; o enquadramento sobe com shift
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.shift_y = shift_y; cam.data.shift_x = shift_x
    cam.data.clip_start = .05; sc.view_settings.exposure = expo
def render():
    sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
