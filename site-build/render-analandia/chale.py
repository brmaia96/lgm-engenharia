# Chalé Analândia: modelo e render (Blender como módulo Python, Cycles em CPU).
# Geometria: render-analandia/spec/spec_1.json (lida das pranchas do executivo). Eixos: X oeste->leste, Y sul->norte, Z para cima.
# uso: python3 chale.py <vista> <saida.png> [amostras] [largura]
import bpy, bmesh, sys, math
from mathutils import Vector

view = sys.argv[1]; out = sys.argv[2]
samples = int(sys.argv[3]) if len(sys.argv) > 3 else 96
W = int(sys.argv[4]) if len(sys.argv) > 4 else 1800

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.transmission_bounces = 6
sc.render.threads_mode = 'FIXED'; sc.render.threads = 4
sc.render.resolution_x = W; sc.render.resolution_y = int(W * 2 / 3); sc.render.film_transparent = False
sc.view_settings.view_transform = 'Filmic'; sc.view_settings.look = 'Medium Contrast'; sc.view_settings.exposure = 0.0

# ---------------- materiais ----------------
def mat(name, color, rough=.6, metal=0.0, spec=.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m
def noise_color(m, c1, c2, scale=8.0, detail=6.0, bump=0.0):
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
    r = nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].color = (*c1, 1); r.color_ramp.elements[1].color = (*c2, 1)
    r.color_ramp.elements[0].position = .35; r.color_ramp.elements[1].position = .7
    nt.links.new(tc.outputs['Object'], n.inputs['Vector']); nt.links.new(n.outputs['Fac'], r.inputs['Fac']); nt.links.new(r.outputs['Color'], b.inputs['Base Color'])
    if bump:
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
        nt.links.new(n.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
M_ROOF = mat('telha', (.10, .105, .115), .42, .85)
M_SEAM = mat('junta', (.085, .09, .10), .4, .85)
M_WHITE = mat('reboco', (.72, .71, .68), .85); noise_color(M_WHITE, (.69, .68, .65), (.75, .74, .71), 30, 8, .05)
M_INT = mat('interno', (.9, .88, .84), .8)
M_FRAME = mat('caixilho', (.02, .02, .022), .4, .6)
M_WOOD = mat('madeira', (.36, .22, .12), .55); noise_color(M_WOOD, (.30, .18, .10), (.44, .28, .16), 3.0, 10, .08)
M_FLOOR = mat('piso', (.55, .54, .52), .35); noise_color(M_FLOOR, (.50, .49, .47), (.60, .59, .57), 2.0, 8, .02)
M_PAVE = mat('calcada', (.40, .38, .35), .8); noise_color(M_PAVE, (.34, .33, .30), (.45, .43, .40), 1.2, 10, .06)
M_GRASS = mat('grama', (.10, .20, .05), .9); noise_color(M_GRASS, (.06, .15, .035), (.16, .27, .07), 1.6, 12, .5)
M_HEDGE = mat('cerca-viva', (.04, .11, .03), .9); noise_color(M_HEDGE, (.025, .08, .02), (.07, .16, .045), 9, 12, .9)
M_TILE = mat('pastilha', (.20, .45, .52), .25)
M_CER = mat('ceramica', (.52, .25, .15), .7); noise_color(M_CER, (.46, .21, .12), (.58, .30, .18), 6, 8, .2)
M_SOFA = mat('sofa', (.45, .42, .38), .9)
M_WALLB = mat('muro', (.62, .61, .58), .9)
def glass(name, tint=(.82, .9, .9), a=.22):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); mix = nt.nodes.new('ShaderNodeMixShader')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tr.inputs['Color'].default_value = (*tint, 1)
    gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = .02
    fr = nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.5
    mp = nt.nodes.new('ShaderNodeMath'); mp.operation = 'ADD'; mp.inputs[1].default_value = a * .25
    nt.links.new(fr.outputs['Fac'], mp.inputs[0]); nt.links.new(mp.outputs[0], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(gl.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o.inputs['Surface'])
    return m
M_GLASS = glass('vidro')
def water():
    m = bpy.data.materials.new('agua'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (.55, .85, .88, 1); b.inputs['Roughness'].default_value = .03
    for k in ('Transmission Weight', 'Transmission'):
        if k in b.inputs: b.inputs[k].default_value = 1.0
    b.inputs['IOR'].default_value = 1.33
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 5; n.inputs['Detail'].default_value = 3
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .12
    nt.links.new(n.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m
M_WATER = water()
def emit(name, color, s):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*color, 1); e.inputs['Strength'].default_value = s
    nt.links.new(e.outputs[0], o.inputs['Surface']); return m

# ---------------- geometria ----------------
def obj_from(verts, faces, name, m):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.data.materials.append(m); return o
def box(x0, x1, y0, y1, z0, z1, m, name='b'):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return obj_from(v, f, name, m)
def prism_xz(poly, y0, y1, m, name='p'):
    n = len(poly); v = [(x, y0, z) for x, z in poly] + [(x, y1, z) for x, z in poly]
    f = [tuple(range(n)), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return obj_from(v, f, name, m)
def boolean_cut(o, cutter):
    md = o.modifiers.new('cut', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = cutter; md.solver = 'EXACT'
    cutter.hide_render = True; cutter.display_type = 'WIRE'

L = 9.35
# águas (placa entre a linha interna e a externa)
def xi_w(z): return z / 2
def xo_w(z): return -0.15 + 0.5105 * z
west = prism_xz([(0, 0), (-0.15, 0), (3.5, 7.15), (3.5, 7.0)], 0, L, M_ROOF, 'agua-oeste')
east_n = prism_xz([(7, 0), (7.15, 0), (3.5, 7.15), (3.5, 7.0)], 4.8, L, M_ROOF, 'agua-leste-norte')
east_s = prism_xz([(4.55, 4.9), (4.55, 5.093), (3.5, 7.15), (3.5, 7.0)], 0, 4.8, M_ROOF, 'agua-leste-sul')
# forro interno claro (fino, por dentro)
prism_xz([(0.02, 0), (0.06, 0), (3.5, 6.92), (3.5, 6.98)], 1.15, 8.5, M_INT, 'forro-o')
prism_xz([(6.98, 0), (6.94, 0), (3.5, 6.92), (3.5, 6.98)], 4.8, 8.5, M_INT, 'forro-l')
# juntas elevadas a cada 0,508 m
slope = math.atan2(7.15, 3.65)
def seams(side, y0, y1, zmin=0.0):
    y = y0 + .254
    while y < y1 - .05:
        if side == 'w': a = (xo_w(zmin), zmin); b_ = (3.5, 7.15)
        else: a = (7 - xo_w(zmin) , zmin); b_ = (3.5, 7.15)
        nx = (-1 if side == 'w' else 1) * math.sin(slope); nz = math.cos(slope); h = .035
        poly = [a, (a[0] + nx * h, a[1] + nz * h), (b_[0] + nx * h, b_[1] + nz * h), b_]
        prism_xz(poly, y - .012, y + .012, M_SEAM, 'junta'); y += .508
seams('w', 0, L); seams('e', 4.8, L); seams('e', 0, 4.8, 5.093)
# cumeeira
prism_xz([(3.36, 7.02), (3.5, 7.21), (3.64, 7.02), (3.5, 7.12)], -0.02, L + .02, M_SEAM, 'cumeeira')
# testeiras (bordas da cobertura) em madeira nas duas empenas
for y0, y1 in ((L - .04, L + .0), (0.0, .04)):
    prism_xz([(-0.15, 0), (0.12, 0), (3.5, 6.62), (3.5, 7.15)], y0, y1, M_WOOD, 'testeira-o')
    if y0 > 1: prism_xz([(7.15, 0), (6.88, 0), (3.5, 6.62), (3.5, 7.15)], y0, y1, M_WOOD, 'testeira-l')

# janelas nas águas (JBV60 e JCV180): pano escuro levemente saliente
def slope_window(side, y0, y1, z0, z1):
    off = .02
    if side == 'w':
        nx, nz = -math.sin(slope), math.cos(slope); p = lambda z: (xo_w(z) + nx * off, z + nz * off); q = lambda z: (xo_w(z) + nx * (off + .03), z + nz * (off + .03))
    else:
        nx, nz = math.sin(slope), math.cos(slope); p = lambda z: (7 - xo_w(z) + nx * off, z + nz * off); q = lambda z: (7 - xo_w(z) + nx * (off + .03), z + nz * (off + .03))
    prism_xz([p(z0), q(z0), q(z1), p(z1)], y0, y1, M_GLASS, 'jan-agua')
    pf = lambda z, e: ((xo_w(z) if side == 'w' else 7 - xo_w(z)) + nx * e, z + nz * e)
    prism_xz([pf(z0 - .05, .0), pf(z0 - .05, .045), pf(z1 + .05, .045), pf(z1 + .05, .0)], y0 - .05, y1 + .05, M_FRAME, 'jan-agua-q')
for y0, y1 in ((5.9, 6.5), (6.9, 7.5)):
    slope_window('w', y0, y1, .3, 2.3); slope_window('e', y0, y1, .3, 2.3)
slope_window('w', 1.8, 3.6, 1.5, 2.1)

# piso interno e varandas
box(0, 7, 0, L, -0.12, 0, M_FLOOR, 'piso')
# frente norte: vidro do piso ao cume, recuado 0,80
prism_xz([(0.02, 0), (6.98, 0), (3.5, 6.96)], 8.515, 8.535, M_GLASS, 'vidro-norte')
def bar(x0, z0, x1, z1, t=.05, y0=8.49, y1=8.56):
    d = Vector((x1 - x0, z1 - z0)); n = Vector((-d.y, d.x)).normalized() * t / 2
    prism_xz([(x0 + n.x, z0 + n.y), (x1 + n.x, z1 + n.y), (x1 - n.x, z1 - n.y), (x0 - n.x, z0 - n.y)], y0, y1, M_FRAME, 'perfil')
bar(1.25, 2.5, 5.75, 2.5, .07); bar(2.0, 4.0, 5.0, 4.0, .07)
for x in (2.5, 3.5, 4.5): bar(x, 0, x, 2.5, .05)
bar(0.03, .03, 6.97, .03, .06); bar(0.02, 0, 3.5, 6.96, .07); bar(6.98, 0, 3.5, 6.96, .07)
# fundos: parede recuada 1,00 com portas; sacada
back = prism_xz([(0.0, 0), (4.55, 0), (4.55, 4.9), (3.5, 7.0)], 1.0, 1.15, M_WHITE, 'parede-sul')
c1 = box(2.8, 3.6, .9, 1.25, 0, 2.1, M_WHITE, 'c1'); boolean_cut(back, c1)
c2 = box(2.65, 4.25, .9, 1.25, 2.7, 4.8, M_WHITE, 'c2'); boolean_cut(back, c2)
box(2.8, 3.6, 1.06, 1.1, 0, 2.1, M_WOOD, 'porta-pam80')
box(2.65, 4.25, 1.07, 1.09, 2.7, 4.8, M_GLASS, 'pcv160'); box(3.43, 3.47, 1.05, 1.11, 2.7, 4.8, M_FRAME, 'pcv160-m')
for z in (2.72, 4.78): box(2.65, 4.25, 1.05, 1.11, z - .02, z + .02, M_FRAME, 'pcv160-t')
# laje do piso superior (inclui a sacada)
slab = prism_xz([(1.2, 2.4), (4.6, 2.4), (4.6, 2.7), (1.35, 2.7)], 0.0, 4.8, M_INT, 'laje')
box(1.22, 4.48, .07, .125, 2.7, 3.7, M_GLASS, 'gc-sacada'); box(1.22, 4.48, .06, .135, 3.68, 3.72, M_FRAME, 'gc-sacada-c')
box(2.75, 4.48, 4.7, 4.75, 2.7, 3.7, M_GLASS, 'gc-mezanino'); box(2.75, 4.48, 4.69, 4.76, 3.68, 3.72, M_FRAME, 'gc-mez-c')
# anexo de dois pavimentos e caixa-d'água
ax = box(4.55, 7.15, 0, 4.8, 0, 7.0, M_WHITE, 'anexo')
cut = box(4.7, 7.0, .15, 4.65, 6.6, 7.2, M_WHITE, 'anexo-topo'); boolean_cut(ax, cut)
def pane(x0, x1, y0, y1, z0, z1):
    box(x0, x1, y0, y1, z0, z1, M_GLASS, 'vidro');
for z0, z1 in ((1.5, 2.1), (4.3, 4.8)):
    box(5.25, 6.45, -.012, .0, z0, z1, M_GLASS, 'jcv120'); box(5.2, 6.5, -.02, .0, z0 - .05, z0, M_FRAME, 'q'); box(5.2, 6.5, -.02, .0, z1, z1 + .05, M_FRAME, 'q')
    box(5.2, 5.25, -.02, .0, z0, z1, M_FRAME, 'q'); box(6.45, 6.5, -.02, .0, z0, z1, M_FRAME, 'q'); box(5.83, 5.87, -.02, .0, z0, z1, M_FRAME, 'q')
box(7.15, 7.162, 2.5, 3.1, 1.5, 2.1, M_GLASS, 'jbv60'); box(7.15, 7.17, 2.45, 3.15, 1.45, 1.5, M_FRAME, 'q'); box(7.15, 7.17, 2.45, 3.15, 2.1, 2.15, M_FRAME, 'q')
box(7.15, 7.165, 1.0, 2.0, 5.5, 6.5, M_FRAME, 'portinhola')
box(4.53, 4.55, .25, .95, 0, 2.1, M_FRAME, 'paa70')
# interior: escada, sofá, tapete, bancada, luminária
for i in range(6): box(4.85, 5.85, 7.2 - (i + 1) * .25, 7.2 - i * .25, 0, (i + 1) * .18, M_WOOD, 'degrau')
box(4.85, 5.85, 4.8, 5.7, .9, 1.08, M_WOOD, 'patamar')
for i in range(8): box(4.85 - (i + 1) * .2625, 4.85 - i * .2625, 4.8, 5.7, 1.08 + i * .18 - .05, 1.08 + (i + 1) * .18, M_WOOD, 'degrau2')
box(1.3, 3.5, 6.3, 7.2, 0, .42, M_SOFA, 'sofa'); box(1.3, 3.5, 6.05, 6.3, 0, .8, M_SOFA, 'sofa-enc'); box(1.5, 3.9, 7.4, 8.3, 0, .015, mat('tapete', (.62, .58, .5), .95), 'tapete')
box(.9, 1.5, 1.8, 3.6, 0, .9, M_INT, 'bancada'); box(.86, 1.52, 1.78, 3.62, .9, .93, mat('pedra', (.08, .08, .08), .3), 'tampo')
box(4.7, 7.0, 4.65, 4.8, 0, 2.4, M_INT, 'parede-anexo-norte')
lamp = bpy.data.objects.new('pend', bpy.data.lights.new('pend', 'POINT')); lamp.data.energy = 420; lamp.data.color = (1, .78, .55); lamp.data.shadow_soft_size = .12
lamp.location = (3.2, 6.8, 2.9); sc.collection.objects.link(lamp)
l2 = bpy.data.objects.new('mez', bpy.data.lights.new('mez', 'POINT')); l2.data.energy = 260; l2.data.color = (1, .8, .6); l2.location = (3.0, 3.0, 4.6); sc.collection.objects.link(l2)
l3 = bpy.data.objects.new('coz', bpy.data.lights.new('coz', 'POINT')); l3.data.energy = 160; l3.data.color = (1, .8, .6); l3.location = (2.6, 2.8, 2.1); sc.collection.objects.link(l3)

# terreno, calçada, piscina, telheiro, muros
ground = box(-4.2, 11.4, -3.2, 22.2, -0.75, -0.10, M_GRASS, 'grama')
box(-4.25, 11.45, -3.25, 22.25, -1.0, -0.14, mat('base', (.16, .10, .06), .8), 'base')
box(-300, 300, -300, 300, -1.02, -1.0, mat('chao', (.012, .012, .012), .45), 'chao')
pave = prism_xz([(-1.15, -.2), (8.15, -.2), (8.15, -.05), (-1.15, -.05)], -1.0, 20.57, M_PAVE, 'calcada')
box(-2.95, -1.15, 11.35, 20.57, -.2, -.05, M_PAVE, 'calcada-telheiro')
pc = box(2.55, 5.55, 12.55, 18.55, -1.5, .5, M_PAVE, 'pc'); boolean_cut(pave, pc)
gc_ = box(2.5, 5.6, 12.5, 18.6, -0.74, 0.5, M_PAVE, 'gc'); boolean_cut(ground, gc_)
box(2.55, 5.55, 12.55, 18.55, -.78, -.72, M_TILE, 'piscina-fundo')
for a in ((2.5, 2.55, 12.5, 18.6), (5.55, 5.6, 12.5, 18.6), (2.5, 5.6, 12.5, 12.55), (2.5, 5.6, 18.55, 18.6)): box(*a, -.78, -.06, M_TILE, 'piscina-parede')
box(2.55, 5.55, 12.55, 14.55, -.72, -.4, M_TILE, 'prainha')
box(2.55, 5.55, 12.55, 18.55, -.25, -.17, M_WATER, 'agua')
# telheiro da churrasqueira: uma água de cerâmica sobre pilares de madeira
for x, y in ((-2.75, 13.25), (-2.75, 18.37), (0.55, 13.25), (0.55, 18.37)): box(x - .08, x + .08, y - .08, y + .08, -.05, 3.55 if x < 0 else 2.62, M_WOOD, 'pilar')
prism_xz([(-2.95, 3.70), (-2.95, 3.78), (0.85, 2.64), (0.85, 2.56)], 12.85, 18.77, M_CER, 'telheiro')
for y in (13.25, 15.8, 18.37): prism_xz([(-2.9, 3.56), (-2.9, 3.70), (0.8, 2.59), (0.8, 2.45)], y - .05, y + .05, M_WOOD, 'viga')
box(-2.95, -2.80, 13.05, 18.57, -.05, 1.0, M_WALLB, 'bancada-churrasqueira')
# ---------------- céu, sol, câmera ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (.02, .02, .022, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = .6
def area(name, loc, tgt, size, energy, color=(1, .97, .92)):
    l = bpy.data.lights.new(name, 'AREA'); l.size = size; l.energy = energy; l.color = color
    o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
def sun(*a): pass
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
def look(pos, target, lens=28, shift_y=0.0):
    cam.location = pos; d = Vector(target) - Vector(pos); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens; cam.data.shift_y = shift_y; cam.data.clip_end = 400
VIEWS = {
 'frente': dict(pos=(13.5, 27.5, 5.2), tgt=(3.3, 8.8, 2.6), lens=38, key=(16, 30, 16), rim=(-10, -6, 12)),
 'fundos': dict(pos=(14.5, -14.0, 5.6), tgt=(3.6, 4.2, 2.9), lens=40, key=(18, -16, 16), rim=(-10, 20, 12)),
 'aerea': dict(pos=(-12.5, 29.0, 15.5), tgt=(3.3, 9.5, 1.2), lens=40, key=(-14, 30, 20), rim=(16, -8, 14)),
 'frontal': dict(pos=(3.5, 30.0, 2.6), tgt=(3.5, 8.5, 3.1), lens=42, key=(12, 30, 14), rim=(-8, -6, 12)),
}
V = VIEWS[view]; look(V['pos'], V['tgt'], V['lens'])
area('key', V['key'], (3.5, 6, 2), 14, 9000)
area('fill', (V['pos'][0] * .6, V['pos'][1], 3), (3.5, 6, 2), 18, 1200, (.9, .95, 1))
area('rim', V['rim'], (3.5, 5, 4), 10, 5000, (1, .95, .9))

sc.render.filepath = out; sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print('ok', out)
