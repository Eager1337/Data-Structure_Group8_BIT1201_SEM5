import sys
import os
import inspect
import textwrap
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

PROJECT_ROOT = Path("/tmp/data_structure/Data Structure")
sys.path.insert(0, str(PROJECT_ROOT))
import src.algorithms as alg

OUTPUT_DIR = PROJECT_ROOT / "project.pptx-slides"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

P = Presentation()
P.slide_width = Inches(13.333)
P.slide_height = Inches(7.5)

C = dict(
    black='111111',
    gray='505050',
    mint='A6D8C8',
    yellow='F4CD59',
    purple='8B78CD',
    coral='F16F54',
    pale='F5F6F5',
    white='FFFFFF',
    dark_purple='5C4D8C',
    light_mint='DDF2EC',
    light_yellow='FDF5DF',
    light_coral='FDE4DF',
    border_gray='D0D5DD'
)

TITLES = []
ROLES = []

def add_transition(s, kind='fade', morph_option='byObject'):
    if kind == 'morph':
        xml = """
        <p:transition %s xmlns:p16="http://schemas.microsoft.com/office/powerpoint/2015/main" spd="med">
            <p16:morph option="%s"/>
        </p:transition>
        """ % (nsdecls("p"), morph_option)
    else:
        xml = """
        <p:transition %s spd="fast">
            <p:fade/>
        </p:transition>
        """ % nsdecls("p")
    s._element.append(parse_xml(xml))

def text(slide, value, x, y, w, h, size=20, bold=False, color='black', font='DM Sans', align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = value.split('\n')
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor.from_string(C.get(color, color))
        p.space_after = Pt(3)
    return box

def shape(slide, kind, x, y, w, h, color, name=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(C[color])
    s.line.fill.background()
    if name:
        s.name = name
    return s

def panel(slide, x, y, w, h, color='mint', name=None):
    r = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, color, name=name)
    r.adjustments[0] = 0.12
    return r

def motif(slide, x, y, size=0.40):
    for i, (kind, color) in enumerate([
        (MSO_SHAPE.OVAL, 'coral'),
        (MSO_SHAPE.ISOSCELES_TRIANGLE, 'purple'),
        (MSO_SHAPE.RECTANGLE, 'mint'),
        (MSO_SHAPE.OVAL, 'yellow')
    ]):
        s = shape(slide, kind, x + i * size, y, size, size, color)
        if i == 1:
            s.rotation = 90

def circle(slide, label, x, y, d=0.46, color='mint', size=17, name=None):
    q = shape(slide, MSO_SHAPE.OVAL, x - d / 2, y - d / 2, d, d, color, name=name)
    tf = q.text_frame
    tf.text = str(label)
    tf.word_wrap = False
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'DM Sans'
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string(C['black'])
    return q

def line(slide, x, y, xx, yy, color='purple', width=1.5, name=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(xx), Inches(yy))
    c.line.color.rgb = RGBColor.from_string(C.get(color, color))
    c.line.width = Pt(width)
    if name:
        c.name = name
    return c

def code_box(slide, value, x, y, w, h, size=15):
    panel(slide, x, y, w, h, 'pale')
    box = text(slide, value, x + 0.22, y + 0.18, w - 0.44, h - 0.32, size, font='Roboto Mono')
    for p in box.text_frame.paragraphs:
        p.space_after = Pt(0)
    return box

def table(slide, rows, x, y, w, h, widths=None, size=16, header_color='mint'):
    t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(h)).table
    if widths:
        for col, v in zip(t.columns, widths):
            col.width = Inches(v)
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            cell = t.cell(i, j)
            cell.text = str(value)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor.from_string(C[header_color if i == 0 else ('white' if i % 2 == 0 else 'pale')])
            cell.margin_left = Inches(0.14)
            cell.margin_right = Inches(0.10)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.font.name = 'DM Sans'
                p.font.size = Pt(size)
                p.font.bold = (i == 0)
                p.font.color.rgb = RGBColor.from_string(C['black'])
    return t

def slide(title, section='', role='Presenter 1', foot='Limkokwing University · Sierra Leone · DCOMP320 Final Project', transition='fade', morph_option='byObject'):
    s = P.slides.add_slide(P.slide_layouts[6])
    TITLES.append(title)
    ROLES.append(role)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = RGBColor.from_string(C['white'])
    
    # Top navigation
    text(s, 'DCOMP320', 0.75, 0.45, 1.8, 0.25, 11, True, font='Poppins')
    sections = [('Overview', 2.8), ('Hanoi', 4.4), ('Trees', 6.0), ('Huffman', 7.6), ('Graphs', 9.2), ('Defense', 10.8)]
    for name, x in sections:
        is_active = (name == section)
        text(s, name, x, 0.45, 1.2, 0.25, 11, is_active, 'purple' if is_active else 'gray')
    
    # Presenter badge at top right
    if role:
        panel(s, 9.7, 0.82, 2.9, 0.36, 'pale')
        text(s, f"🎙️ {role}", 9.8, 0.87, 2.7, 0.25, 11, True, color='dark_purple')
    
    # Footer
    slide_num = len(P.slides)
    text(s, foot, 0.75, 7.12, 10.5, 0.22, 10, color='gray')
    text(s, f"{slide_num:02d} / 26", 11.85, 7.12, 0.73, 0.22, 10, color='gray', align=PP_ALIGN.RIGHT)
    
    add_transition(s, kind=transition, morph_option=morph_option)
    return s

def heading(s, title, x=0.75, y=1.25, w=11.8, h=1.3, size=34):
    text(s, title, x, y, w, h, size, True, font='Poppins')

def note(s, presenter, duration, script, key_points, examiner_qa):
    body = (
        f"--- SPEAKER NOTES ---\n"
        f"PRESENTER ROLE: {presenter}\n"
        f"ESTIMATED DURATION: {duration}\n\n"
        f"VERBATIM TALKING SCRIPT:\n\"{script}\"\n\n"
        f"KEY TECHNICAL POINTS TO HIGHLIGHT:\n{key_points}\n\n"
        f"ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:\nQ: {examiner_qa[0]}\nA: {examiner_qa[1]}\n\n"
        f"Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py"
    )
    s.notes_slide.notes_text_frame.text = body

def excerpt(fn, start, end=None):
    src = inspect.getsource(fn)
    if end is None: return textwrap.dedent(src[src.index(start):]).rstrip()
    return textwrap.dedent(src[src.index(start):src.index(end)]).rstrip()

# Graph POS definitions
POS = {
    'Figure 1': {
        'A': (0, 4), 'B': (2.2, 4), 'C': (4.4, 4), 'D': (1.25, 2.85), 'E': (3.3, 2.85),
        'F': (-0.65, 1.65), 'G': (0.55, 1.65), 'H': (2, 1.65), 'I': (3.3, 1.65), 'J': (4.4, 1.65),
        'K': (1.25, 0.25), 'L': (4.4, 0.25)
    },
    'Figure 2': {
        'A': (0, 4.5), 'B': (1.7, 4.5), 'C': (3.5, 4.5), 'D': (1, 3.15), 'E': (2.25, 3.15),
        'F': (4.5, 3.15), 'G': (2.2, 1.7), 'H': (3.45, 1.7), 'I': (1.1, 0.2), 'J': (3.7, 0.2)
    }
}

def draw_graph(s, name, x, y, w, h, mode='path', small=False, custom_path=None):
    g = alg.assignment_graphs()[name]
    pos = POS[name]
    xs = [v[0] for v in pos.values()]
    ys = [v[1] for v in pos.values()]
    pts = {k: (x + 0.3 + (a - min(xs)) / (max(xs) - min(xs)) * (w - 0.6),
               y + 0.3 + (max(ys) - b) / (max(ys) - min(ys)) * (h - 0.6)) for k, (a, b) in pos.items()}
    dist, prev, _ = alg.dijkstra(g, 'A')
    mst, total, _ = alg.prim(g)
    
    if custom_path:
        path = custom_path
    else:
        target = 'L' if 'L' in g else 'J'
        path = alg.reconstruct_path(prev, 'A', target)
        
    sel = {frozenset((a, b)) for a, b in zip(path, path[1:])} if mode == 'path' else {frozenset((a, b)) for a, b, _ in mst}
    edges = [(a, b, weight) for a in g for b, weight in g[a].items() if a < b]
    
    for a, b, weight in edges:
        if mode == 'mst' and frozenset((a, b)) not in sel: continue
        ax, ay = pts[a]
        bx, by = pts[b]
        chosen = frozenset((a, b)) in sel
        line(s, ax, ay, bx, by, 'purple' if chosen else 'border_gray', 3.5 if chosen else 1.2, name=f"!!Edge_{name[:4]}_{a}_{b}")
        dx = bx - ax; dy = by - ay; length = (dx * dx + dy * dy) ** 0.5
        mx = (ax + bx) / 2 - dy / length * 0.10
        my = (ay + by) / 2 + dx / length * 0.10
        shape(s, MSO_SHAPE.OVAL, mx - 0.14, my - 0.13, 0.28, 0.26, 'white')
        text(s, str(weight), mx - 0.14, my - 0.13, 0.28, 0.26, 12 if small else 14, chosen, align=PP_ALIGN.CENTER)
        
    for k, (xx, yy) in pts.items():
        is_path_node = (k in path and mode == 'path')
        circle(s, k, xx, yy, 0.38 if small else 0.48, 'mint' if is_path_node else ('yellow' if mode == 'mst' else 'pale'), 14 if small else 18, name=f"!!Node_{name[:4]}_{k}")
    return g, path, dist, mst, total

def draw_tree(s, x, y, w, h, highlight_nodes=None):
    pts = {}
    def place(i, lo, hi, depth):
        pts[i] = (x + (lo + hi) / 2 * w, y + depth * h / 4)
        if i < 16:
            place(2 * i, lo, (lo + hi) / 2, depth + 1)
            place(2 * i + 1, (lo + hi) / 2, hi, depth + 1)
    place(1, 0, 1, 0)
    for i in range(1, 16):
        for j in (2 * i, 2 * i + 1):
            line(s, *pts[i], *pts[j], color='purple', width=1.2, name=f"!!TreeEdge_{i}_{j}")
    for i, (xx, yy) in pts.items():
        is_hl = (highlight_nodes and i in highlight_nodes)
        circle(s, i, xx, yy, 0.36, 'yellow' if is_hl else ('mint' if i >= 16 else 'pale'), 12, name=f"!!TreeNode_{i}")

def draw_huffman_tree_full(s, ox=6.8, oy=1.3):
    nodes = {
        '46': (ox + 2.24, oy + 0.44),
        '30': (ox + 3.40, oy + 1.50),
        '14': (ox + 2.40, oy + 2.54),
        '6':  (ox + 1.49, oy + 3.59),
        'e':  (ox + 0.64, oy + 1.44),
        'd':  (ox + 4.64, oy + 2.49),
        'c':  (ox + 3.34, oy + 3.54),
        'a':  (ox + 0.64, oy + 4.46),
        'b':  (ox + 2.14, oy + 4.46),
    }
    branches = [
        ('46', 'e', '0', (ox + 1.44, oy + 0.99)),
        ('46', '30', '1', (ox + 2.82, oy + 0.97)),
        ('30', '14', '0', (ox + 2.90, oy + 2.02)),
        ('30', 'd', '1', (ox + 4.02, oy + 1.99)),
        ('14', '6', '0', (ox + 1.94, oy + 3.06)),
        ('14', 'c', '1', (ox + 2.87, oy + 3.04)),
        ('6', 'a', '0', (ox + 1.06, oy + 4.02)),
        ('6', 'b', '1', (ox + 1.81, oy + 4.02)),
    ]
    for p, ch, bit, (bx, by) in branches:
        px, py = nodes[p]
        cx, cy = nodes[ch]
        line(s, px, py, cx, cy, color='purple', width=1.6, name=f"!!HuffEdge_{p}_{ch}")
        shape(s, MSO_SHAPE.OVAL, bx - 0.12, by - 0.13, 0.24, 0.26, 'white', name=f"!!HuffBitBg_{p}_{ch}")
        text(s, bit, bx - 0.12, by - 0.13, 0.24, 0.26, 12, bold=True, align=PP_ALIGN.CENTER)

    for k in ['46', '30', '14', '6']:
        nx, ny = nodes[k]
        circle(s, k, nx, ny, d=0.57, color='pale', size=15, name=f"!!HuffNode_{k}")

    leaves = [
        ('e', 'e:16', '0', nodes['e']),
        ('d', 'd:16', '11', nodes['d']),
        ('c', 'c:8', '101', nodes['c']),
        ('a', 'a:2', '1000', nodes['a']),
        ('b', 'b:4', '1001', nodes['b']),
    ]
    for sym, label, code_str, (nx, ny) in leaves:
        circle(s, label, nx, ny, d=0.68, color='mint', size=14, name=f"!!HuffLeaf_{sym}")
        text(s, code_str, nx - 0.45, ny + 0.38, 0.90, 0.25, 12, bold=True, color='dark_purple', align=PP_ALIGN.CENTER)

def draw_hanoi_pegs(s, state, x=0.8, y=3.0, w=5.5, h=2.8):
    peg_colors = {'A': 'coral', 'B': 'mint', 'C': 'yellow'}
    for k, peg in enumerate('ABC'):
        xx = x + (k + 0.5) * w / 3
        # Vertical post
        shape(s, MSO_SHAPE.RECTANGLE, xx - 0.02, y + 0.3, 0.04, h - 0.6, 'purple', name=f"!!HanoiPost_{peg}")
        # Base platform
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, xx - w / 7, y + h - 0.3, w / 3.5, 0.08, 'black', name=f"!!HanoiBase_{peg}")
        # Label
        circle(s, peg, xx, y + h + 0.05, d=0.35, color=peg_colors[peg], size=13, name=f"!!HanoiPegLbl_{peg}")
        
        # Disks
        disks = state[peg]
        for level, disk in enumerate(disks):
            dw = (0.35 + 0.22 * disk) * (w / 3.2)
            dh = 0.30
            dy = y + h - 0.35 - level * 0.36
            col = ['coral', 'mint', 'yellow'][disk - 1]
            shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, xx - dw / 2, dy, dw, dh, col, name=f"!!HanoiDisk{disk}")
            text(s, f"Disk {disk}", xx - dw / 2, dy + 0.04, dw, dh, 11, bold=True, align=PP_ALIGN.CENTER)

print("Starting generation of all 26 slides...")

# ==========================================
# SLIDE 01: TITLE SLIDE
# ==========================================
s = slide('Data Structures & Algorithms, Made Visible.', section='Overview', role='Presenter 1')
motif(s, 0.8, 1.4, 0.48)
heading(s, 'Data Structures\n& Algorithms,\nMade Visible.', y=2.10, w=7.2, h=2.8, size=42)
text(s, 'DCOMP320 · Final Project Presentation & Viva Defense\nLimkokwing University of Creative Technology · Sierra Leone', 0.8, 5.25, 7.0, 0.8, 18, color='gray')
text(s, 'Lecturer: Amandus Benjamin Coker\nTeam Presentation: Roles Partitioned for Group Defense', 0.8, 6.25, 7.0, 0.6, 15)

for label, sub, x, y, col in [
    ('01', 'Recursion\n(Hanoi)', 8.4, 1.6, 'coral'),
    ('02', 'Trees\n(Traversals)', 10.8, 2.7, 'mint'),
    ('03', 'Compression\n(Huffman)', 8.4, 4.1, 'yellow'),
    ('04', 'Optimization\n(Graphs)', 10.8, 5.2, 'purple')
]:
    circle(s, label, x, y, 1.05, col, 28)
    text(s, sub, x - 0.95, y + 0.65, 1.9, 0.55, 15, True, align=PP_ALIGN.CENTER)

note(s, 'Presenter 1 (Opening)', '60 seconds',
     'Good morning/afternoon, Lecturer Coker and members of the panel. Today, our team presents our comprehensive implementation, mathematical analysis, and empirical verification for the DCOMP320 Data Structures and Algorithms final project. We have implemented all four core problem domains into a clean, reproducible Python system backed by 19 automated tests. Each member of our team will walk through their specialized domain, followed by our live defense where we address all examiner questions.',
     '- Formal introduction of DCOMP320 project scope and university context.\n- Highlight that all 4 assignment domains are implemented natively without third-party libraries.\n- Present team structure and readiness for examiner viva questions.',
     ('What was the guiding software engineering philosophy behind this implementation?',
      'We decoupled algorithmic computation from I/O. Every algorithm in src/algorithms.py returns pure data structures (generators, dataclasses, tuples), enabling complete unit testing and automated validation independent of the CLI.'))

# ==========================================
# SLIDE 02: TEAM ROLES & PRESENTATION BLUEPRINT
# ==========================================
s = slide('Team Roles & Defense Strategy.', section='Overview', role='Presenter 1')
heading(s, 'Team Roles &\nDefense Strategy.', w=6.5, h=1.5)
text(s, 'Partitioned roles for a seamless 10–12 minute group viva.', 0.8, 3.0, 5.8, 0.6, 18, color='gray')

roles_data = [
    ('Presenter 1', 'Opening, Architecture, Tower of Hanoi (Recursion)', 'coral', '01'),
    ('Presenter 2', '5-Level Binary Tree, 4 Traversals, BFS vs DFS', 'mint', '02'),
    ('Presenter 3', 'Huffman Greedy Compression, Min-Heap, Bit Savings', 'yellow', '03'),
    ('Presenter 4', 'Graph Optimization: Dijkstra, Prim MST, Anomaly', 'purple', '04'),
    ('All Members', '19 Unit Tests, Live Demonstration & Examiner Viva Q&A', 'pale', 'Q&A')
]

for i, (p_name, desc, col, icon) in enumerate(roles_data):
    yy = 1.45 + i * 1.05
    circle(s, icon, 7.1, yy + 0.25, 0.55, col if col != 'pale' else 'white', 15)
    text(s, p_name, 7.6, yy, 4.8, 0.35, 19, True)
    text(s, desc, 7.6, yy + 0.38, 4.8, 0.45, 15, color='gray')

panel(s, 0.8, 4.8, 5.6, 1.8, 'pale')
text(s, '💡 Flexible Group Allocation:\n• 4 Presenters: 1 section each + shared Q&A.\n• 3 Presenters: P1 takes Hanoi, P2 takes Trees & Huffman, P3 takes Graphs & QA.\n• 2 Presenters: P1 takes Hanoi & Trees, P2 takes Huffman & Graphs.', 1.0, 4.95, 5.2, 1.5, 14)

note(s, 'Presenter 1', '45 seconds',
     'To ensure an orderly and professional defense, we have divided the four assignment problems across our presenters. I will cover the architecture and Tower of Hanoi. Presenter 2 will discuss Binary Trees and traversal mechanics. Presenter 3 will explain Huffman coding and bit compression. Presenter 4 will present Graph optimization, including shortest paths, minimum spanning trees, and our critical analysis of the Figure 2 anomaly. Finally, all team members will participate in defending the implementation during the viva.',
     '- Explicitly shows examiner that every team member has mastery over their assigned section.\n- Displays clear time management (10-12 mins total presentation).\n- Clarifies fallback mapping for 2, 3, or 4 member teams.',
     ('How did you ensure consistency across different team members code?',
      'We enforced strict type annotations, shared data contracts in algorithms.py, unified error handling, and automated unittest suites that everyone ran before committing.'))

# ==========================================
# SLIDE 03: SYSTEM ARCHITECTURE & REPRODUCIBILITY
# ==========================================
s = slide('Four Problems. One Reproducible Architecture.', section='Overview', role='Presenter 1')
heading(s, 'Four Problems.\nOne Reproducible Architecture.', w=6.8, h=1.5)
text(s, 'Zero external dependencies. Pure standard library Python.', 0.8, 2.95, 5.8, 0.5, 18, color='gray')

code_box(s, 'Data Structure/\n├── src/algorithms.py        # Pure algorithmic core\n├── main.py                  # Interactive & batch CLI\n├── tests/test_algorithms.py  # 19 automated unit tests\n├── outputs/results.json     # Full canonical trace\n└── project.report/          # 39-page formal report', 0.8, 3.65, 5.8, 2.6, 14)

for i, (name, ds, col) in enumerate([
    ('01 Tower of Hanoi', 'Recursion · Generator dispatch · O(n) Call stack', 'coral'),
    ('02 Binary Tree Traversals', 'TreeNode objects · collections.deque FIFO queue', 'mint'),
    ('03 Huffman Coding', 'heapq Min-Heap · Prefix tree · Bit packing', 'yellow'),
    ('04 Graph Optimization', 'Adjacency lists · Min-heap Dijkstra & Prim', 'purple')
]):
    yy = 1.5 + i * 1.25
    panel(s, 7.0, yy, 5.5, 1.05, 'pale')
    circle(s, str(i + 1), 7.4, yy + 0.52, 0.52, col, 16)
    text(s, name, 7.9, yy + 0.15, 4.4, 0.35, 18, True)
    text(s, ds, 7.9, yy + 0.52, 4.4, 0.40, 14, color='gray')

note(s, 'Presenter 1', '45 seconds',
     'Our repository is organized around a clean modular architecture. The core algorithms reside in src/algorithms.py with zero third-party dependencies—relying exclusively on standard library modules such as heapq and collections. The main.py entry point provides both an interactive console menu and non-interactive scriptable CLI flags. All outputs are recorded deterministically in JSON format, and every algorithm is verified by 19 automated unit tests.',
     '- Functional separation: src/algorithms.py contains zero print statements.\n- CLI options: interactive menu + batch mode (--all, --disks).\n- Deterministic JSON output enables automated regression testing.',
     ('Why did you avoid using popular third-party graph libraries like NetworkX?',
      'To demonstrate authentic academic understanding of data structures. Building our own adjacency lists, min-heaps, and tree structures proves foundational competence without relying on black-box abstractions.'))

# ==========================================
# SLIDE 04: PROBLEM 1: TOWER OF HANOI THEORY
# ==========================================
s = slide('Problem 1: Tower of Hanoi — Recursive Divide & Conquer.', section='Hanoi', role='Presenter 1')
heading(s, 'Tower of Hanoi:\nDivide-and-Conquer Recursion.', w=7.2, h=1.5)

code_box(s, excerpt(alg.hanoi, '    def solve', '    return solve'), 0.8, 2.9, 7.2, 2.6, 16)

panel(s, 8.3, 2.9, 4.3, 1.9, 'light_coral')
text(s, 'Three Golden Rules:\n1. Only one disk moved at a time.\n2. Disk removed from top of a peg.\n3. Larger disk never on smaller disk.', 8.5, 3.1, 3.9, 1.5, 16, bold=True, color='black')

panel(s, 8.3, 5.0, 4.3, 1.7, 'mint')
text(s, 'Recurrence Relation:\nT(n) = 2T(n−1) + 1\nT(n) = 2ⁿ − 1 moves\nFor n = 3: 2³ − 1 = 7 moves\nStack Depth: O(n)', 8.5, 5.15, 3.9, 1.4, 16, bold=True)

panel(s, 0.8, 5.85, 7.2, 0.85, 'pale')
text(s, 'Base Case: k = 0 yields 0 moves.\nDisks modeled as 1 (smallest) to n (largest); Pegs A, B, C.', 1.0, 6.0, 6.8, 0.55, 15)

note(s, 'Presenter 1', '60 seconds',
     'Moving to Problem 1: The Tower of Hanoi is a textbook demonstration of divide-and-conquer recursion. To move n disks from peg A to peg C using peg B as auxiliary, the algorithm breaks the task into three atomic steps: First, recursively move n minus 1 disks from A to B. Second, move the single largest disk directly from A to C. Third, recursively move the n minus 1 disks from B to C. This yields the classical recurrence T(n) equals 2 T(n minus 1) plus 1, resulting in exactly 2 to the n minus 1 moves. For n equals 3, exactly 7 moves are required.',
     '- Mathematical recurrence: T(n) = 2T(n-1) + 1, expanding to 2^n - 1.\n- Invariance: Larger disk is never placed on a smaller disk at any point in the call stack.\n- Call stack auxiliary memory is O(n), while time complexity is Theta(2^n).',
     ('How does your Python implementation avoid high recursion overhead?',
      'We use Python generators with yield from, allowing each move to be lazily emitted as a tuple without storing the entire sequence of 2^n moves in memory upfront.'))

# ==========================================
# SLIDE 05: HANOI MORPH ANIMATION: STEP 0 -> STEP 1
# ==========================================
s = slide('Hanoi State Animation: Move 1 (A → C).', section='Hanoi', role='Presenter 1', transition='morph')
heading(s, 'Hanoi State 1:\nMove 1: Disk 1 (A → C)', w=6.5, h=1.5)

# Pegs state after Move 1: A:[3, 2], B:[], C:[1]
draw_hanoi_pegs(s, {'A': [3, 2], 'B': [], 'C': [1]}, x=0.8, y=2.8, w=5.6, h=2.8)

# Table showing 7 moves with step 1 highlighted
hanoi_moves = list(alg.hanoi(3))
table_rows = [['Step', 'Disk', 'Move', 'State']] + [
    [str(i), f"Disk {d}", f"{a} → {b}", '✓ ACTIVE' if i == 1 else 'Pending']
    for i, (d, a, b) in enumerate(hanoi_moves, 1)
]
table(s, table_rows, 6.8, 2.6, 5.7, 3.8, widths=[0.9, 1.3, 1.5, 2.0], size=14, header_color='coral')

panel(s, 0.8, 6.1, 5.6, 0.65, 'light_coral')
text(s, 'Morph Transition: Disk 1 glides from Peg A to Peg C.', 1.0, 6.25, 5.2, 0.35, 14, True)

note(s, 'Presenter 1', '45 seconds',
     'Notice the PowerPoint Morph transition on screen. In Move 1, the smallest disk, Disk 1 in coral, glides seamlessly from Peg A to Peg C. This leaves Disk 2 accessible on Peg A and satisfies all rules. Peg B remains completely free as an auxiliary buffer.',
     '- Morph transition demonstrates the first physical move.\n- Disk 1 on Peg C, Disks 2 & 3 remain on Peg A.\n- Table shows Step 1 active.',
     ('Why does disk 1 move to C first instead of B for n=3?',
      'Because n=3 is odd. For odd n, the smallest disk must always make its first move directly to the target peg (C) to ensure the largest disk eventually reaches C on move 2^(n-1). For even n, disk 1 starts on the auxiliary peg (B).'))

# ==========================================
# SLIDE 06: HANOI MORPH ANIMATION: MOVES 2 & 3 (A->B, C->B)
# ==========================================
s = slide('Hanoi State Animation: Moves 2 & 3 (Subproblem n=2 on B).', section='Hanoi', role='Presenter 1', transition='morph')
heading(s, 'Hanoi States 2 & 3:\nSubproblem n=2 Solved to Peg B', w=6.8, h=1.5)

# Pegs state after Move 3: A:[3], B:[2, 1], C:[]
draw_hanoi_pegs(s, {'A': [3], 'B': [2, 1], 'C': []}, x=0.8, y=2.8, w=5.6, h=2.8)

table_rows = [['Step', 'Disk', 'Move', 'State']] + [
    [str(i), f"Disk {d}", f"{a} → {b}", '✓ ACTIVE' if i in [2, 3] else ('Done' if i < 2 else 'Pending')]
    for i, (d, a, b) in enumerate(hanoi_moves, 1)
]
table(s, table_rows, 6.8, 2.6, 5.7, 3.8, widths=[0.9, 1.3, 1.5, 2.0], size=14, header_color='mint')

panel(s, 0.8, 6.1, 5.6, 0.65, 'light_mint')
text(s, 'Subproblem Complete: n−1 = 2 disks transferred onto Peg B.', 1.0, 6.25, 5.2, 0.35, 14, True)

note(s, 'Presenter 1', '45 seconds',
     'In Step 2, Disk 2 moves from A to B. Then in Step 3, Disk 1 moves from C onto Disk 2 on Peg B. As you can see, the subproblem of size n minus 1 equals 2 is now completely solved on auxiliary Peg B. This clears Peg A completely except for the largest disk, and leaves target Peg C completely empty and ready.',
     '- Subproblem reduction: Moving n-1=2 disks to Peg B took 2^2 - 1 = 3 moves.\n- Largest disk (Disk 3) is now exposed and ready to move to Peg C.\n- Peg C is empty.',
     ('What is the maximum number of recursive calls on the stack at this point?',
      'At n=3, the maximum stack depth is exactly 3 frames (proportional to O(n)), corresponding to the depth of the recursive calls for disk 3, disk 2, and disk 1.'))

# ==========================================
# SLIDE 07: HANOI MORPH ANIMATION: MOVE 4 TO 7 (SOLVED ON C)
# ==========================================
s = slide('Hanoi State Animation: Move 4 to 7 (Solved State).', section='Hanoi', role='Presenter 1', transition='morph')
heading(s, 'Hanoi Final State:\nAll 3 Disks Transferred to Peg C', w=6.8, h=1.5)

# Pegs state after Move 7: A:[], B:[], C:[3, 2, 1]
draw_hanoi_pegs(s, {'A': [], 'B': [], 'C': [3, 2, 1]}, x=0.8, y=2.8, w=5.6, h=2.8)

table_rows = [['Step', 'Disk', 'Move', 'State']] + [
    [str(i), f"Disk {d}", f"{a} → {b}", '✓ COMPLETE']
    for i, (d, a, b) in enumerate(hanoi_moves, 1)
]
table(s, table_rows, 6.8, 2.6, 5.7, 3.8, widths=[0.9, 1.3, 1.5, 2.0], size=14, header_color='yellow')

panel(s, 0.8, 6.1, 5.6, 0.65, 'light_yellow')
text(s, 'Total Moves: 2³ − 1 = 7 legal moves verified. Peg C holds [3, 2, 1].', 1.0, 6.25, 5.2, 0.35, 14, True)

note(s, 'Presenter 1', '45 seconds',
     'In Move 4, Disk 3 moves to Peg C. Then in Moves 5, 6, and 7, the two disks on Peg B are transferred onto Peg C. The entire puzzle is solved in exactly 7 legal moves. Our automated test suite simulates and verifies this sequence for n equals 0 through n equals 8, confirming exact move counts and legal disk ordering at every step. I will now hand over to Presenter 2 for Binary Trees.',
     '- Move 4 places base disk; Moves 5-7 transfer remaining disks.\n- Final state verified: C = [3, 2, 1], A = [], B = [].\n- Smooth transition to Presenter 2 for Problem 2.',
     ('What would happen if n=0 or negative disks were passed?',
      'n=0 gracefully yields 0 moves without errors. Negative or non-integer inputs trigger strict validation in algorithms.py and raise ValueError/TypeError.'))

# ==========================================
# SLIDE 08: PROBLEM 2: BINARY TREE STRUCTURE (31 NODES)
# ==========================================
s = slide('Problem 2: Perfect Binary Tree Architecture.', section='Trees', role='Presenter 2')
heading(s, 'A Perfect Binary Tree:\nFive Levels, 31 Nodes.', w=7.5, h=1.5)

circle(s, '31', 11.6, 1.8, 1.15, 'yellow', 30)
text(s, 'Total Nodes', 10.95, 2.45, 1.3, 0.35, 16, True, align=PP_ALIGN.CENTER)

draw_tree(s, 0.8, 2.9, 11.8, 2.8)

panel(s, 0.8, 6.05, 11.8, 0.75, 'mint')
text(s, 'Node i Formula: Left child = 2i, Right child = 2i + 1   ·   15 Internal Nodes (1…15)   ·   16 Leaves (16…31)   ·   Height = 4 edges (5 levels)', 1.0, 6.25, 11.4, 0.45, 16, True)

note(s, 'Presenter 2', '60 seconds',
     'Thank you, Presenter 1. Moving to Problem 2: We analyze the complete binary tree specified in the assignment. The tree contains exactly 31 nodes labeled 1 through 31 in level order. Node i has left child 2i and right child 2i plus 1. This forms a perfect binary tree with 5 levels and height 4. Nodes 1 through 15 are internal nodes, while nodes 16 through 31 are all leaves at depth 4. Crucially, as examiners often ask, this tree is full, complete, and perfect—but it is NOT a Binary Search Tree because left children are often larger than their parents.',
     '- Mathematical definition: Node i children = 2i and 2i+1.\n- 31 nodes = 2^(h+1) - 1 where height h = 4.\n- 16 leaves (51.6% of nodes) at bottom depth.\n- NOT a BST: Inorder traversal is not sorted.',
     ('Why is this tree not a Binary Search Tree (BST)?',
      'In a BST, every left descendant must be strictly less than the node, and right descendant greater. Here, node 4 has left child 8 (greater), while node 2 has right child 5 (greater than 4). Numeric labels represent level-order positions, not BST search keys.'))

# ==========================================
# SLIDE 09: PROBLEM 2: THE 4 TRAVERSALS COMPARED
# ==========================================
s = slide('Tree Traversals: Pre, In, Post, and Level-Order.', section='Trees', role='Presenter 2')
heading(s, 'Traversal Changes Order—\nNot the Underlying Tree.', w=7.8, h=1.5)

root = alg.assignment_tree()
sequences = {
    'Preorder': alg.preorder(root),
    'Inorder': alg.inorder(root),
    'Postorder': alg.postorder(root),
    'Level-Order': alg.levelorder(root)
}
rules = [
    'Root → Left Subtree → Right Subtree',
    'Left Subtree → Root → Right Subtree',
    'Left Subtree → Right Subtree → Root',
    'Breadth-First: Level-by-level using FIFO Queue'
]

trav_table_rows = [['Traversal Type', 'Exploration Rule', 'First 10 Visited Nodes', 'Time / Space']]
for (name, vals), rule in zip(sequences.items(), rules):
    first_10 = ', '.join(map(str, vals[:10])) + ' …'
    comp = 'O(n) / O(h)' if name != 'Level-Order' else 'O(n) / O(w)'
    trav_table_rows.append([name, rule, first_10, comp])

table(s, trav_table_rows, 0.8, 2.8, 11.8, 2.7, widths=[2.0, 3.8, 4.3, 1.7], size=14, header_color='mint')

panel(s, 0.8, 5.75, 11.8, 1.05, 'pale')
text(s, '• Preorder starts at Root (1, 2, 4, 8, 16…); Inorder visits deepest left leaf first (16, 8, 17, 4…);\n• Postorder visits children before parents (16, 17, 8, 18, 19, 9, 4…); Level-Order visits sequentially (1, 2, 3… 31).\n• All traversals take linear O(n) time, visiting each of the 31 nodes exactly once.', 1.0, 5.85, 11.4, 0.85, 14)

note(s, 'Presenter 2', '60 seconds',
     'Here we compare the four canonical tree traversals. In Preorder, we visit the root before subtrees, beginning with 1, 2, 4, 8, 16. In Inorder, we explore the left subtree, then root, then right, starting at leaf 16. In Postorder, both subtrees are processed before the parent, making it ideal for bottom-up tasks like deleting trees or evaluating expression trees. Finally, Level-Order traverses horizontally across each depth level, producing the natural sequence 1 through 31. All four algorithms run in O(n) time, but their spatial memory footprints differ substantially.',
     '- Preorder (Root-L-R), Inorder (L-Root-R), Postorder (L-R-Root), Level-Order (BFS).\n- Inorder on a BST produces sorted output; here it proves the tree is not a BST.\n- Linear time complexity Theta(n) across all four methods.',
     ('Why did you avoid using recursive list concatenation (e.g., return left + [root] + right)?',
      'Recursive list concatenation copies lists at each frame, leading to O(n^2) worst-case time complexity. We passed a single accumulator list that nodes append to in O(1), preserving strict O(n) linear performance.'))

# ==========================================
# SLIDE 10: PROBLEM 2: LEVEL-ORDER QUEUE VS DFS STACK
# ==========================================
s = slide('Traversal Memory: FIFO Queue vs DFS Call Stack.', section='Trees', role='Presenter 2')
heading(s, 'Queue vs Call Stack:\nMemory Tradeoffs in Traversals.', w=7.8, h=1.5)

panel(s, 0.8, 2.8, 5.6, 2.9, 'light_mint')
text(s, 'DFS Traversal (Pre / In / Post)\n• Mechanism: System Call Stack (LIFO)\n• Auxiliary Space: O(h) where h = height\n• For this tree: Height = 4 edges\n• Max Stack Memory: 5 frames\n• Memory Advantage: Extremely lean on deep, balanced trees.', 1.0, 3.0, 5.2, 2.5, 15)

panel(s, 6.9, 2.8, 5.6, 2.9, 'light_yellow')
text(s, 'BFS Traversal (Level-Order)\n• Mechanism: FIFO Queue (collections.deque)\n• Auxiliary Space: O(w) where w = max width\n• For this tree: Leaf Level = 16 nodes\n• Max Queue Memory: 16 nodes stored\n• Memory Disadvantage: Stores half the tree at bottom level.', 1.1, 3.0, 5.2, 2.5, 15)

code_box(s, '# collections.deque gives O(1) amortized popleft\nqueue = deque([root])\nwhile queue:\n    node = queue.popleft()\n    result.append(node.value)\n    if node.left:  queue.append(node.left)\n    if node.right: queue.append(node.right)', 0.8, 5.85, 11.8, 1.05, 13)

note(s, 'Presenter 2', '60 seconds',
     'A favorite viva defense question is the memory comparison between DFS and BFS. DFS traversals use the call stack with auxiliary memory proportional to tree height O(h). In our tree of 31 nodes, the maximum stack depth is only 5 frames. Conversely, Level-Order BFS uses a FIFO queue whose size is proportional to maximum tree width O(w). At level 4, our queue must hold up to 16 leaf nodes simultaneously—more than half the tree! Furthermore, we utilized Python collections.deque, which guarantees O(1) popleft, avoiding the O(n) overhead of list.pop(0). I now pass the presentation to Presenter 3 for Huffman Coding.',
     '- DFS auxiliary space = O(h) = O(log n) for balanced trees.\n- BFS auxiliary space = O(w) = O(n/2) = O(n) for balanced trees.\n- collections.deque is an O(1) double-ended queue implemented in C.',
     ('What would happen if you used Python built-in list as a queue?',
      'Using a Python list with pop(0) causes an O(n) memory shift for every pop, degrading overall BFS traversal from O(n) to O(n^2). collections.deque provides O(1) pointer shifts.'))

# ==========================================
# SLIDE 11: PROBLEM 3: HUFFMAN CODING CONCEPTS
# ==========================================
s = slide('Problem 3: Huffman Coding & Greedy Optimization.', section='Huffman', role='Presenter 3')
heading(s, 'Huffman Coding:\nOptimal Prefix-Free Compression.', w=7.5, h=1.5)

freq_data = [['Symbol', 'Frequency', 'Percentage']] + [
    ['a', '2', '4.3%'],
    ['b', '4', '8.7%'],
    ['c', '8', '17.4%'],
    ['d', '16', '34.8%'],
    ['e', '16', '34.8%'],
    ['Total', '46', '100.0%']
]
table(s, freq_data, 0.8, 2.8, 4.8, 2.8, widths=[1.5, 1.5, 1.8], size=15, header_color='yellow')

panel(s, 6.0, 2.8, 6.5, 2.8, 'light_yellow')
text(s, 'Greedy Choice Principle:\n• Symbols with higher frequencies get shorter bit codes.\n• Symbols with lower frequencies get longer bit codes.\n\nMin-Heap Building Mechanism:\n• Insert all symbols into a priority queue (min-heap).\n• Repeatedly pop the TWO trees with smallest frequencies.\n• Merge into a new parent node with sum frequency.\n• Push parent back into heap until one tree remains.', 6.2, 3.0, 6.1, 2.4, 15)

panel(s, 0.8, 5.85, 11.7, 0.95, 'pale')
text(s, 'Heap Priority Queue: Python heapq guarantees O(k log k) tree construction time for k distinct symbols.\nPrefix-Free Property: No code word is a prefix of another code word; enables instantaneous decoding.', 1.0, 6.0, 11.3, 0.65, 15)

note(s, 'Presenter 3', '60 seconds',
     'Thank you, Presenter 2. Moving to Problem 3: Huffman Coding is a greedy algorithm designed for lossless data compression. The input consists of 5 symbols: a with frequency 2, b with 4, c with 8, and d and e each with 16, totaling 46 symbols. Huffman’s key insight is that frequently occurring symbols should be assigned shorter bit codes, while rarer symbols receive longer codes. By maintaining candidate subtrees in a min-heap priority queue, we repeatedly extract the two lowest-frequency trees, merge them, and re-insert their sum until a single prefix tree is formed.',
     '- Input frequencies: a:2, b:4, c:8, d:16, e:16 (sum = 46).\n- Greedy choice: Combine two smallest weights at every step.\n- Priority queue min-heap enables O(k log k) building time for k symbols.',
     ('Why does Huffman coding require a min-heap rather than a simple sorted list?',
      'A min-heap allows insertion and extraction of minimum elements in O(log k) time. Re-sorting a list on each merge would take O(k log k) per step, resulting in O(k^2 log k) overall time.'))

# ==========================================
# SLIDE 12: PROBLEM 3: HUFFMAN TREE CONSTRUCTION WITH MORPH
# ==========================================
s = slide('Huffman Tree Construction Step-by-Step.', section='Huffman', role='Presenter 3', transition='morph')
heading(s, 'Tree Construction:\nFour Min-Heap Merge Steps.', w=6.5, h=1.5)

draw_huffman_tree_full(s, ox=6.8, oy=1.3)

panel(s, 0.8, 2.8, 5.6, 2.9, 'light_mint')
text(s, 'Step-by-Step Merge Log:\n1. Pop a(2) & b(4)  → Parent node (6)\n2. Pop (6) & c(8)    → Parent node (14)\n3. Pop (14) & d(16)  → Parent node (30)\n4. Pop e(16) & (30)  → Root node (46)\n\nLeft Branch = Bit 0  ·  Right Branch = Bit 1', 1.0, 3.0, 5.2, 2.5, 15)

panel(s, 0.8, 5.85, 5.6, 0.95, 'pale')
text(s, 'Root Weight: 46 (matches total symbol count).\nDeepest leaves: a and b at depth 4 (4-bit codes).', 1.0, 6.0, 5.2, 0.65, 14)

note(s, 'Presenter 3', '60 seconds',
     'This diagram shows the complete Huffman prefix tree generated by our program. In step 1, a with frequency 2 and b with 4 are merged into parent node 6. In step 2, node 6 is merged with c of frequency 8 to form node 14. In step 3, node 14 merges with d of frequency 16 to create node 30. Finally, e with 16 and node 30 are merged into root 46. By assigning 0 to left branches and 1 to right branches, we generate instantaneous prefix codes by walking from root to each leaf.',
     '- Step 1: 2 + 4 = 6\n- Step 2: 6 + 8 = 14\n- Step 3: 14 + 16 = 30\n- Step 4: 16 + 30 = 46 (Root)\n- Left branch represents 0; right branch represents 1.',
     ('Is the generated Huffman tree unique?',
      'No. While the minimum total weighted path length is unique, tree structure can vary if ties exist, or if left/right branch assignments (0 vs 1) are inverted. Our code uses stable tuple tie-breaking to guarantee deterministic outputs.'))

# ==========================================
# SLIDE 13: PROBLEM 3: CODEBOOK & 30.4% BIT SAVINGS
# ==========================================
s = slide('Huffman Codebook & 30.4% Compression Verification.', section='Huffman', role='Presenter 3')
heading(s, 'Codebook Results:\n30.4% Payload Bit Reduction.', w=7.5, h=1.5)

codebook_rows = [
    ['Symbol', 'Freq', 'Code', 'Bits/Sym', 'Total Bits'],
    ['e', '16', '0', '1', '16'],
    ['d', '16', '11', '2', '32'],
    ['c', '8', '101', '3', '24'],
    ['b', '4', '1001', '4', '16'],
    ['a', '2', '1000', '4', '8'],
    ['Total', '46', '—', '2.09 avg', '96 bits']
]
table(s, codebook_rows, 0.8, 2.7, 6.2, 3.0, widths=[1.1, 1.0, 1.4, 1.3, 1.4], size=15, header_color='yellow')

panel(s, 7.4, 2.7, 5.1, 1.4, 'mint')
text(s, 'Variable-Length Payload:\n96 Bits\nAverage: 2.087 bits/symbol', 7.6, 2.85, 4.7, 1.1, 16, True)

panel(s, 7.4, 4.3, 5.1, 1.4, 'pale')
text(s, 'Fixed-Width Benchmark:\n138 Bits\n46 symbols × 3 bits (ceil(log₂ 5))', 7.6, 4.45, 4.7, 1.1, 16, True)

panel(s, 0.8, 5.85, 11.7, 0.95, 'light_yellow')
text(s, 'Exact Compression Saving: (138 − 96) / 138 = 30.43% reduction in payload transmission size.\nPrefix-Free Proof: No code begins with another code (e.g. e is 0; no other code starts with 0). Decode is deterministic.', 1.0, 6.0, 11.3, 0.65, 14, True)

note(s, 'Presenter 3', '60 seconds',
     'Here is our finalized codebook. Symbol e receives the single-bit code 0. Symbol d receives 11. Symbol c receives 101. And rare symbols a and b receive 4-bit codes 1000 and 1001. Summing the product of frequencies and bit lengths gives exactly 96 payload bits. A fixed-width encoding for 5 symbols requires 3 bits per symbol, totaling 138 bits. Huffman achieves a 30.43% reduction. Our unit test suite exhaustively validates that encoding and decoding round-trip perfectly without data loss. I now hand over to Presenter 4 for Graph Optimization.',
     '- Symbol e (16 counts) uses 1 bit: 16 bits.\n- Symbol d (16 counts) uses 2 bits: 32 bits.\n- Symbol c (8 counts) uses 3 bits: 24 bits.\n- Symbol b (4 counts) uses 4 bits: 16 bits.\n- Symbol a (2 counts) uses 4 bits: 8 bits.\n- Total = 96 bits vs 138 fixed = 30.43% savings.',
     ('What overhead does Huffman coding introduce in practical network storage?',
      'In a complete compressed file, the codebook or frequency table must be transmitted alongside the bitstream so the decompressor can reconstruct the tree. For small files, this header overhead can reduce net savings.'))

# ==========================================
# SLIDE 14: PROBLEM 4: GRAPH ANATOMY & DATA STRUCTURE
# ==========================================
s = slide('Problem 4: Graph Optimization & Undirected Representation.', section='Graphs', role='Presenter 4')
heading(s, 'Graph Optimization:\nFigure 1 & Figure 2 Representation.', w=7.8, h=1.5)

panel(s, 0.8, 2.7, 5.6, 3.0, 'light_mint')
text(s, 'Figure 1 Characteristics:\n• 12 Vertices: A through L\n• 19 Undirected Edges\n• Non-negative edge weights (1 to 9)\n• Target node L exists in the graph.\n\nFigure 2 Characteristics:\n• 10 Vertices: A through J ONLY\n• 19 Undirected Edges\n• Target node L DOES NOT EXIST!', 1.0, 2.9, 5.2, 2.6, 15)

panel(s, 6.8, 2.7, 5.7, 3.0, 'pale')
text(s, 'Data Structure: Nested Adjacency List\ngraph = {\n  "A": {"B": 2, "D": 4},\n  "B": {"A": 2, "C": 3, "D": 1, "E": 2},\n  ...\n}\n\n• O(1) Edge lookup between neighbors.\n• O(V + E) Space complexity (memory efficient).\n• Symmetric edges added for undirected graphs.', 7.0, 2.85, 5.3, 2.7, 14, font='Roboto Mono')

panel(s, 0.8, 5.9, 11.7, 0.9, 'light_coral')
text(s, 'Undirected Handout Check: The assignment diagrams contain no directional arrows; edges are strictly bidirectional.\nDefensive Engineering: Graph validator checks symmetry, non-negativity, and rejects self-loops.', 1.0, 6.05, 11.3, 0.6, 14, True)

note(s, 'Presenter 4', '60 seconds',
     'Thank you, Presenter 3. Moving to Problem 4: We investigate graph optimization on the two assignment graphs: Figure 1 and Figure 2. We represented both graphs as nested adjacency lists in Python dictionaries, ensuring O(1) edge lookup time and O(V + E) memory efficiency. Because the handout diagrams contain no directional arrowheads, all edges are modeled symmetrically as undirected edges. In our initial graph inspection, we confirmed that Figure 1 contains 12 vertices from A to L. However, we uncovered a critical anomaly in Figure 2: it contains only 10 vertices from A to J—vertex L does not exist.',
     '- Graph representation: dict of dicts for O(1) neighborhood access.\n- Symmetric bidirectional modeling because no arrows exist in handout.\n- Identification of Figure 2 anomaly: 10 vertices vs 12 vertices.',
     ('Why choose adjacency lists over an adjacency matrix?',
      'Both Figure 1 and Figure 2 are sparse graphs (19 edges on 10-12 vertices). Adjacency lists require O(V + E) space, whereas an adjacency matrix requires O(V^2) space and forces algorithms like Dijkstra to scan absent edges.'))

# ==========================================
# SLIDE 15: PROBLEM 4: FIGURE 1 DIJKSTRA SHORTEST PATH
# ==========================================
s = slide('Figure 1: Dijkstra Shortest Path (A to L = 20).', section='Graphs', role='Presenter 4')
heading(s, 'Figure 1: Dijkstra Shortest Path\nfrom Source A to Target L costs 20.', w=6.5, h=1.5)

g1, p1, dist1, _, _ = draw_graph(s, 'Figure 1', 6.6, 1.45, 5.9, 5.3, mode='path')

panel(s, 0.8, 2.8, 5.4, 2.0, 'mint')
text(s, 'Optimal Route:\nA → D → H → E → J → L\n\nEdge Weight Breakdown:\n4 + 9 + 4 + 2 + 1 = 20', 1.0, 3.0, 5.0, 1.6, 18, True)

panel(s, 0.8, 4.95, 5.4, 1.8, 'pale')
text(s, 'Dijkstra Min-Heap Relaxation:\n• Priority queue holds (tentative_dist, vertex).\n• Relaxation: if dist[u] + w(u,v) < dist[v]:\n    dist[v] = dist[u] + w(u,v)\n    heapq.heappush(heap, (dist[v], v))\n• Visited set prevents reprocessing settled nodes.', 1.0, 5.1, 5.0, 1.5, 13)

note(s, 'Presenter 4', '60 seconds',
     'Here is the verified shortest path on Figure 1 from vertex A to vertex L. Our Dijkstra implementation utilizes a binary min-heap to repeatedly settle the nearest unvisited vertex. The optimal path is A to D, D to H, H to E, E to J, and J to L, yielding an exact total distance of 20. Other potential paths, such as routing through vertices B, C, or G, accumulate higher weights. We independently verified this result against an all-pairs Floyd-Warshall implementation, and all distances from source A matched perfectly.',
     '- Shortest path: A -> D -> H -> E -> J -> L with cost 20.\n- Edge weights: 4 + 9 + 4 + 2 + 1 = 20.\n- Min-heap relaxation runs in O((V + E) log V) time.\n- Validated against Floyd-Warshall.',
     ('Why does Dijkstra require edge weights to be non-negative?',
      'Dijkstra operates on a greedy invariant: once a vertex is extracted from the min-heap, its shortest path is assumed finalized. A negative edge could later offer a cheaper detour, invalidating the finalized distance.'))

# ==========================================
# SLIDE 16: PROBLEM 4: FIGURE 2 ANOMALY & ERROR HANDLING
# ==========================================
s = slide('Figure 2: Handout Anomaly & Defensive Architecture.', section='Graphs', role='Presenter 4')
heading(s, 'Figure 2 Handout Anomaly:\nVertex L Does Not Exist.', w=6.5, h=1.5)

g2, p2, dist2, _, _ = draw_graph(s, 'Figure 2', 6.6, 1.45, 5.9, 5.3, mode='path', custom_path=['A', 'I', 'J'])

panel(s, 0.8, 2.8, 5.4, 1.9, 'light_coral')
text(s, 'The Assignment Anomaly:\n• Handout asks for A → L on Figure 2.\n• Figure 2 only has vertices {A, B, C, D, E, F, G, H, I, J}.\n• Target vertex L is completely absent.', 1.0, 3.0, 5.0, 1.5, 15, True)

panel(s, 0.8, 4.85, 5.4, 2.0, 'light_yellow')
text(s, 'Defensive Engineering Solution:\n• Software verifies vertex existence dynamically.\n• Returns "Target L not found in Figure 2".\n• Does NOT hallucinate or silently fake vertex L.\n\nDemonstration Path on Figure 2:\n• Shortest path to farthest vertex J: A → I → J\n• Total cost = 9 + 1 = 10.', 1.0, 5.0, 5.0, 1.7, 14)

note(s, 'Presenter 4', '60 seconds',
     'This is a crucial slide for our viva defense. When analyzing Figure 2, we noticed a printing defect or typo in the original assignment handout: the question asks for shortest path from A to L on Figure 2, but Figure 2 only contains 10 vertices: A through J. Vertex L does not exist. Rather than silently crashing or inventing a fake vertex L, our program incorporates defensive error handling. It detects that L is absent from the vertex set and raises a clean, informative status. To prove Dijkstra works correctly on Figure 2, we demonstrated the shortest path to vertex J, which traverses A to I to J with a cost of 10.',
     '- Academic honesty: Flagged the handout typo rather than faking data.\n- Defensive coding: Input validation checks whether source and target exist.\n- Farthest node J verified: A -> I -> J costs 10.',
     ('If an examiner argues that vertex L should have been added, how do you respond?',
      'Adding an arbitrary vertex L with invented edge weights would be academically dishonest and ungrounded. Robust software must validate its inputs against the formal graph specification and handle missing targets gracefully.'))

# ==========================================
# SLIDE 17: PROBLEM 4: MINIMUM SPANNING TREES (PRIM VS KRUSKAL)
# ==========================================
s = slide('Minimum Spanning Trees: Prim vs Kruskal.', section='Graphs', role='Presenter 4')
heading(s, 'Minimum Spanning Trees:\nFigure 1 = 35 · Figure 2 = 42.', w=7.8, h=1.5)

# Dual mini-graphs
_, _, _, edges1, total1 = draw_graph(s, 'Figure 1', 0.8, 2.7, 5.5, 3.2, mode='mst', small=True)
text(s, f"Figure 1 MST Weight = {total1}", 0.8, 2.35, 5.5, 0.35, 18, True)

_, _, _, edges2, total2 = draw_graph(s, 'Figure 2', 6.8, 2.7, 5.5, 3.2, mode='mst', small=True)
text(s, f"Figure 2 MST Weight = {total2}", 6.8, 2.35, 5.5, 0.35, 18, True)

panel(s, 0.8, 6.05, 11.7, 0.75, 'mint')
text(s, 'Figure 1: 11 edges connect 12 vertices with total weight 35   ·   Figure 2: 9 edges connect 10 vertices with total weight 42\nIndependent Cross-Check: Kruskal’s Disjoint-Set Union algorithm confirms identical MST totals from every vertex.', 1.0, 6.2, 11.3, 0.45, 15, True)

note(s, 'Presenter 4', '60 seconds',
     'Next, we examine Minimum Spanning Trees using Prim’s algorithm. An MST connects all vertices in a connected graph using exactly V minus 1 edges while minimizing the total sum of edge weights. For Figure 1, the MST selects 11 edges with a total weight of 35. For Figure 2, the MST selects 9 edges with a total weight of 42. We independently implemented Kruskal’s algorithm using Disjoint Set Union-Find, and tested Prim starting from every possible vertex. Every single execution converged to the exact same total weights: 35 and 42.',
     '- Prim MST totals: Figure 1 = 35; Figure 2 = 42.\n- Number of edges in MST is strictly V - 1 (11 edges for Fig 1, 9 edges for Fig 2).\n- Tested from all starting vertices; verified against independent Kruskal implementation.',
     ('How does Prim’s algorithm compare to Kruskal’s algorithm?',
      'Prim grows a single tree vertex-by-vertex from a start node using a min-heap (best for dense graphs). Kruskal sorts all edges globally and adds lightest cycle-free edges using Union-Find (best for sparse graphs). Both produce identical total MST weights.'))

# ==========================================
# SLIDE 18: PROBLEM 4: DIJKSTRA VS PRIM DEEP DIVE
# ==========================================
s = slide('Dijkstra vs Prim: Shortest Path ≠ MST.', section='Graphs', role='Presenter 4')
heading(s, 'The Critical Distinction:\nShortest Path Tree ≠ Minimum Spanning Tree.', w=8.5, h=1.5)

panel(s, 0.8, 2.8, 5.6, 2.9, 'light_mint')
text(s, 'DIJKSTRA (Shortest Paths)\n• Objective: Minimize distance from SOURCE to each vertex.\n• Heap Key: Accumulated distance dist[u] + weight.\n• Figure 1 Result: Path A → L = 20.\n• Total SPT Edge Weight: 43!\n• Why it fails as an MST: Overspends globally to keep individual paths short.', 1.0, 3.0, 5.2, 2.5, 15)

panel(s, 6.8, 2.8, 5.6, 2.9, 'light_yellow')
text(s, 'PRIM (Minimum Spanning Tree)\n• Objective: Minimize TOTAL EDGE WEIGHT of the entire tree.\n• Heap Key: Single crossing edge weight.\n• Figure 1 Result: Total MST Weight = 35.\n• Path A → L along MST: 24 (4+3+4+6+4+2+1)!\n• Why it fails as Shortest Path: Takes circuitous detours to save edge weight.', 7.0, 3.0, 5.2, 2.5, 15)

panel(s, 0.8, 5.9, 11.6, 0.9, 'pale')
text(s, 'Examiner Viva Proof on Figure 1: MST total is 35 (cheaper than SPT 43), but A-to-L route in MST costs 24 (slower than Dijkstra 20).\nConclusion: Prim CANNOT be used to find shortest paths, and Dijkstra CANNOT be used to build an MST.', 1.0, 6.05, 11.2, 0.6, 14, True)

note(s, 'Presenter 4', '60 seconds',
     'One of the most frequent examination traps is confusing Shortest Path Trees with Minimum Spanning Trees. Figure 1 provides a mathematical proof that they are fundamentally distinct. Dijkstra finds a path from A to L costing 20, but the total edge weight of the full Shortest Path Tree is 43. In contrast, Prim finds an MST with total weight of only 35. However, if you travel from A to L along that MST, the distance is 24! Dijkstra optimizes locally for each vertex relative to source A. Prim optimizes globally for total network wire length. They solve two different problems.',
     '- Concrete proof from Figure 1: SPT total weight = 43; MST total weight = 35.\n- A-to-L path length: Dijkstra = 20; MST path = 24.\n- Heap key difference: Dijkstra uses accumulated distance; Prim uses raw edge weight.',
     ('Under what condition would a Shortest Path Tree happen to be identical to an MST?',
      'Only in special graph topologies, such as a simple path graph (line) or star graph where the cheapest global edges naturally coincide with shortest source distances.'))

# ==========================================
# SLIDE 19: TESTING & QUALITY ASSURANCE
# ==========================================
s = slide('19 Unit Tests & Algorithmic Cross-Validation.', section='Overview', role='Presenter 4 & Team')
heading(s, '19 Automated Unit Tests:\nMulti-Angle Verification.', w=7.8, h=1.5)

test_rows = [
    ['Assignment Domain', 'Implementation Target', 'Independent Verification Method', 'Status'],
    ['Hanoi', 'Recursive generator solve()', 'Automated legal-state simulation (n=0…8)', '✓ 100% Pass'],
    ['Trees', 'TreeNode & 4 traversals', 'Exact expected sequences + structural invariants', '✓ 100% Pass'],
    ['Huffman', 'heapq min-heap & codec', 'Round-trip encode/decode + exhaustive code lengths', '✓ 100% Pass'],
    ['Dijkstra', 'Single-source shortest path', 'All-pairs Floyd–Warshall (every source, both graphs)', '✓ 100% Pass'],
    ['Prim', 'Minimum spanning tree', 'Kruskal’s algorithm (every start node, both graphs)', '✓ 100% Pass']
]
table(s, test_rows, 0.8, 2.7, 11.7, 2.8, widths=[1.8, 2.8, 5.3, 1.8], size=14, header_color='mint')

code_box(s, 'python -m unittest discover -s tests -v\n# 19 tests in 0.042s · Seeded random graphs (sizes 2..10) · CLI recovery', 0.8, 5.75, 8.2, 0.95, 14)

panel(s, 9.2, 5.75, 3.3, 0.95, 'yellow')
text(s, 'Zero Test Failures\nAll checks automated', 9.4, 5.9, 2.9, 0.65, 15, True, align=PP_ALIGN.CENTER)

note(s, 'Presenter 4 & Team', '45 seconds',
     'Software reliability requires rigorous validation. Our test suite contains 19 automated unittest methods executed via standard Python unittest discover. Rather than merely comparing against hardcoded values, we implemented independent alternative algorithms for cross-checking: Dijkstra was verified against Floyd-Warshall across all node pairs; Prim was cross-verified against Kruskal; Hanoi was tested with a state simulator; and Huffman was tested with full string round trips. All 19 tests pass in under 0.05 seconds.',
     '- 19 unittest methods pass with zero failures.\n- Independent verification: Floyd-Warshall for Dijkstra, Kruskal for Prim.\n- Edge cases tested: n=0 disks, disconnected components, malformed strings.',
     ('Why is independent cross-verification superior to snapshot testing?',
      'Snapshot testing only checks if code output has not changed; if the original logic was flawed, the test still passes. Cross-verifying with Floyd-Warshall and Kruskal mathematically proves the output is correct according to different algorithmic principles.'))

# ==========================================
# SLIDE 20: LIVE DEMONSTRATION GUIDE
# ==========================================
s = slide('Interactive CLI & Live Demonstration Guide.', section='Overview', role='Presenter 1 & Team')
heading(s, 'Live Demonstration:\nInteractive CLI & Command Line.', w=7.8, h=1.5)

code_box(s, '# 1. Interactive terminal menu\npython main.py\n\n# 2. Batch execution of all four problems\npython main.py --all --disks 3\n\n# 3. Execute all 19 automated unit tests\npython -m unittest discover -s tests -v', 0.8, 2.8, 6.2, 2.7, 15)

panel(s, 7.3, 2.8, 5.2, 2.7, 'pale')
text(s, 'Demonstration Capabilities:\n• Interactive menu with input validation.\n• Real-time Hanoi step playback.\n• 31-node traversal prints.\n• Huffman custom text encoder/decoder.\n• Dijkstra & Prim route traces.\n• Graceful handling of invalid inputs (e.g. --disks -1).', 7.5, 3.0, 4.8, 2.3, 15)

panel(s, 0.8, 5.8, 11.7, 0.95, 'light_mint')
text(s, 'The CLI is completely runnable live right now during our presentation. All outputs match the generated outputs/results.json trace file exactly.', 1.0, 6.0, 11.3, 0.55, 15, True)

note(s, 'Presenter 1 & Team', '45 seconds',
     'Our program features a dual-mode interface. Running python main.py opens an interactive menu allowing the user to select and inspect each problem individually. Running with the --all flag executes the entire pipeline in automated batch mode. If the examination panel requests a live demonstration of any algorithm or test, we can execute it immediately in the terminal.',
     '- main.py supports interactive menu and scriptable batch flags.\n- Live demo ready for any panel request.\n- Strict exit codes and input sanitization.',
     ('How does the CLI handle user error, such as entering negative disks or invalid letters?',
      'The CLI uses defensive try-except blocks and argument validation. It displays human-readable error messages and re-prompts the user rather than crashing with unhandled tracebacks.'))

# ==========================================
# SLIDE 21: VIVA DEFENSE SECTION DIVIDER
# ==========================================
s = slide('Comprehensive Viva Defense & Examiner Q&A.', section='Defense', role='All Presenters')
motif(s, 0.8, 1.4, 0.48)
heading(s, 'Viva Defense &\nExaminer Q&A Strategy.', y=2.15, w=7.5, h=2.5, size=40)
text(s, 'Detailed, bulletproof responses prepared for all technical viva questions.\nCovering edge cases, mathematical proofs, and architectural decisions.', 0.8, 5.0, 7.0, 1.0, 18, color='gray')

panel(s, 8.2, 1.8, 4.3, 4.8, 'pale')
text(s, 'Examiner Hotspots Covered:\n\n1. Graph Theory & Figure 2 Anomaly\n   (Missing vertex L, Dijkstra invariants)\n\n2. Trees & Traversal Mechanics\n   (Level-order queue vs DFS stack)\n\n3. Greedy Choice & Compression\n   (Huffman optimality & prefix-free)\n\n4. Recurrence & Complexity Proofs\n   (Hanoi induction, Big-O Matrix)\n\n5. Real-World Systems Applications\n   (Production networking & storage)', 8.4, 2.0, 3.9, 4.4, 15)

note(s, 'All Presenters', '30 seconds',
     'We now transition to the Viva Defense portion of our presentation. We have prepared detailed, mathematically grounded answers for all expected examiner questions across all four problem domains. Each team member will address questions in their respective specialization.',
     '- Formal transition to examiner defense phase.\n- Demonstrates thorough team preparation and confidence.\n- Pre-empts common examiner traps.',
     ('Are all team members prepared to answer questions on any part of the project?',
      'Yes. While we partitioned primary presentation roles, every team member studied the complete codebase, mathematical proofs, and test suite.'))

# ==========================================
# SLIDE 22: VIVA DEFENSE: GRAPH THEORY & ANOMALIES
# ==========================================
s = slide('Viva Defense: Graph Theory & Discrepancies.', section='Defense', role='Presenter 4')
heading(s, 'Viva Defense:\nGraph Theory & Handout Discrepancies.', w=8.5, h=1.5)

panel(s, 0.8, 2.7, 5.6, 1.9, 'light_coral')
text(s, 'Q1: Why does Figure 2 lack vertex L?\nA: Figure 2 has only 10 vertices (A…J). Our code detects vertex membership and reports A-to-L as Not Applicable. We demonstrated A-to-J (cost 10) to confirm Dijkstra correctness on Figure 2.', 1.0, 2.85, 5.2, 1.6, 14, True)

panel(s, 6.8, 2.7, 5.6, 1.9, 'light_yellow')
text(s, 'Q2: Can Dijkstra handle negative weights?\nA: No. Dijkstra assumes finalized distances from the min-heap can never be reduced. A negative edge breaks this greedy invariant. Negative cycles require Bellman-Ford or Johnson’s algorithm.', 7.0, 2.85, 5.2, 1.6, 14, True)

panel(s, 0.8, 4.85, 5.6, 2.0, 'light_mint')
text(s, 'Q3: What if the graph is disconnected?\nA: In Dijkstra, unreachable nodes retain distance infinity. In Prim, a disconnected graph cannot span all vertices; our implementation detects this and raises an explicit DisconnectedGraphError.', 1.0, 5.0, 5.2, 1.7, 14, True)

panel(s, 6.8, 4.85, 5.6, 2.0, 'pale')
text(s, 'Q4: How do cycles affect Dijkstra and Prim?\nA: Non-negative cycles do not affect Dijkstra because distances only increase. Prim naturally avoids cycles because it maintains a visited set and never adds edges connecting two visited vertices.', 7.0, 5.0, 5.2, 1.7, 14, True)

note(s, 'Presenter 4', '60 seconds',
     'Examiners frequently probe graph edge cases. First, on Figure 2 missing L: we explain our defensive detection. Second, on negative weights: Dijkstra fails because once a node is settled, it is never reconsidered; negative edges require Bellman-Ford with O(V*E) runtime. Third, on disconnected graphs: Dijkstra leaves unreachable nodes at infinity, while Prim raises an error because a spanning tree must cover all vertices. Fourth, on cycles: non-negative cycles are harmless to Dijkstra, while Prim’s visited set prevents cycles by design.',
     '- Q1: Handout typo handled with input validation.\n- Q2: Negative edges break greedy settlement; need Bellman-Ford.\n- Q3: Disconnected graphs raise error in Prim.\n- Q4: Visited sets prevent cycle formation in MST.',
     ('Could we run Dijkstra with negative weights by adding a constant to make all weights positive?',
      'No! Adding a constant k penalizes paths with more edges more heavily than paths with fewer edges, changing which path is shortest. Johnson’s algorithm uses vertex reweighting via Bellman-Ford potentials, which preserves shortest path equivalence.'))

# ==========================================
# SLIDE 23: VIVA DEFENSE: TREES & GREEDY COMPRESSION
# ==========================================
s = slide('Viva Defense: Trees, Queues & Greedy Compression.', section='Defense', role='Presenter 2 & 3')
heading(s, 'Viva Defense:\nTree Traversal Mechanics & Greedy Proofs.', w=8.5, h=1.5)

panel(s, 0.8, 2.7, 5.6, 2.0, 'light_mint')
text(s, 'Q5: Why MUST Level-Order use a Queue?\nA: BFS processes nodes in arrival order across horizontal depth levels. A FIFO queue guarantees first-discovered nodes are expanded first. A stack would invert this to Depth-First Search (DFS).', 1.0, 2.85, 5.2, 1.7, 14, True)

panel(s, 6.8, 2.7, 5.6, 2.0, 'light_yellow')
text(s, 'Q6: Why is Huffman Greedy Choice Optimal?\nA: Mathematical proof by induction (Huffman 1952). The two lowest frequencies MUST be sibling leaves at the deepest level of an optimal prefix tree; combining them preserves optimal substructure.', 7.0, 2.85, 5.2, 1.7, 14, True)

panel(s, 0.8, 4.95, 5.6, 1.9, 'pale')
text(s, 'Q7: Why is Inorder traversal not sorted?\nA: Because this binary tree is indexed in level order (left child 2i, right child 2i+1), not arranged as a Binary Search Tree (BST). Inorder on this tree produces: 16, 8, 17, 4, 18, 9, 19, 2…', 1.0, 5.1, 5.2, 1.6, 14, True)

panel(s, 6.8, 4.95, 5.6, 1.9, 'light_coral')
text(s, 'Q8: What guarantees Prefix-Free decoding?\nA: In a Huffman tree, all data symbols reside strictly at the LEAVES. Internal nodes contain frequencies, not symbols. Therefore, no path to a symbol can be a prefix of another path.', 7.0, 5.1, 5.2, 1.6, 14, True)

note(s, 'Presenter 2 & 3', '60 seconds',
     'On tree mechanics: Level-order traversal requires a FIFO queue because breadth-first exploration requires visiting nodes in the exact order they were discovered layer by layer. On Huffman optimality: David Huffman proved in 1952 that an optimal prefix tree must place the two lowest frequency symbols as siblings at maximum depth. Furthermore, because all symbols are stored at leaf nodes, no code can possibly be a prefix of another, enabling instantaneous decoding without delimiters.',
     '- Q5: FIFO queue is essential for BFS level-by-level exploration.\n- Q6: Huffman greedy choice property & optimal substructure.\n- Q7: Sequential labeling 2i, 2i+1 does not satisfy BST invariant.\n- Q8: Leaf-only symbols guarantee prefix-free condition.',
     ('How does the decoder know when a symbol code ends without delimiters?',
      'Because the code is prefix-free, the decoder reads bits sequentially down the tree from the root. The instant it reaches a leaf node, it emits that symbol and resets to the root. There is zero ambiguity.'))

# ==========================================
# SLIDE 24: VIVA DEFENSE: HANOI INDUCTION & BIG-O MATRIX
# ==========================================
s = slide('Viva Defense: Recurrence Induction & Complexity Matrix.', section='Defense', role='Presenter 1')
heading(s, 'Viva Defense:\nMathematical Proof & Complexity Matrix.', w=8.5, h=1.5)

panel(s, 0.8, 2.7, 4.6, 4.1, 'light_coral')
text(s, 'Hanoi Induction Proof:\n\n• Base Case: n = 1\n  T(1) = 2¹ − 1 = 1 move (A → C). True.\n\n• Inductive Hypothesis:\n  Assume T(k) = 2ᵏ − 1 moves.\n\n• Inductive Step for k + 1 disks:\n  1. Move k disks to spare: T(k) moves\n  2. Move disk k+1 to target: 1 move\n  3. Move k disks to target: T(k) moves\n\n  Total = 2·T(k) + 1\n        = 2(2ᵏ − 1) + 1\n        = 2ᵏ⁺¹ − 2 + 1\n        = 2ᵏ⁺¹ − 1  ∎ Q.E.D.', 1.0, 2.85, 4.2, 3.8, 14, True)

comp_rows = [
    ['Problem', 'Algorithm', 'Time Complexity', 'Aux Space'],
    ['Hanoi', 'Recursive generator', 'Θ(2ⁿ) exponential', 'O(n) call stack'],
    ['Trees', 'DFS traversals', 'O(V) linear', 'O(h) stack'],
    ['Trees', 'Level-order BFS', 'O(V) linear', 'O(w) queue'],
    ['Huffman', 'Build min-heap', 'O(k log k)', 'O(k) tree'],
    ['Huffman', 'Encode / Decode', 'O(n) message len', 'O(k) codebook'],
    ['Dijkstra', 'Binary min-heap', 'O((V + E) log V)', 'O(V + E)'],
    ['Prim', 'Binary min-heap', 'O((V + E) log V)', 'O(V + E)']
]
table(s, comp_rows, 5.7, 2.7, 6.8, 4.1, widths=[1.3, 1.7, 2.2, 1.6], size=13, header_color='mint')

note(s, 'Presenter 1', '60 seconds',
     'Here is our formal mathematical proof by induction for the Tower of Hanoi. For base case n equals 1, 2 to the 1 minus 1 equals 1 move, which is correct. Assuming it holds for k, moving k plus 1 disks requires moving k disks to auxiliary, moving the largest disk, then moving the k disks to the target. This gives 2 times 2 to the k minus 1 plus 1, which simplifies to 2 to the k plus 1 minus 1, completing the proof. Beside it, our comprehensive Big-O complexity matrix summarizes the exact asymptotic time and space complexities across all 4 problem implementations.',
     '- Complete mathematical induction proof for T(n) = 2^n - 1.\n- Rigorous Big-O summary matrix covering time and auxiliary space for all algorithms.\n- Demonstrates theoretical mastery alongside practical code.',
     ('Can Dijkstra or Prim be improved to O(E + V log V)?',
      'Yes! By replacing a standard binary min-heap with a Fibonacci heap, the decrease-key operation drops from O(log V) to O(1) amortized, achieving O(E + V log V). However, binary heaps have lower constant factors and simpler implementations in practice.'))

# ==========================================
# SLIDE 25: VIVA DEFENSE: REAL-WORLD APPLICATIONS
# ==========================================
s = slide('Viva Defense: Real-World Industry Applications.', section='Defense', role='All Presenters')
heading(s, 'Viva Defense:\nReal-World Software Engineering Mapping.', w=8.5, h=1.5)

apps = [
    ('Tower of Hanoi', 'Backup rotation grandfather-father-son algorithms, recursive state-space backtracking, and stack memory profiling.', 'coral'),
    ('Binary Trees', 'DOM trees in web browsers, abstract syntax trees (ASTs) in Python compilers, and database indexing.', 'mint'),
    ('Huffman Coding', 'Core entropy coding stage in JPEG image compression, MP3 audio encoding, and DEFLATE in Gzip / ZIP archives.', 'yellow'),
    ('Dijkstra Algorithm', 'OSPF / IS-IS interior gateway network routing, packet forwarding, Google Maps road navigation networks.', 'purple'),
    ('Prim & Kruskal MST', 'Fiber optic telecommunication cable layouts, electrical power grid routing, and clustering in machine learning.', 'dark_purple')
]

for i, (title_str, text_str, col) in enumerate(apps):
    yy = 2.65 + i * 0.85
    panel(s, 0.8, yy, 11.7, 0.75, 'pale')
    shape(s, MSO_SHAPE.RECTANGLE, 0.8, yy, 0.12, 0.75, col)
    text(s, title_str, 1.1, yy + 0.12, 2.5, 0.3, 16, True)
    text(s, text_str, 3.8, yy + 0.12, 8.5, 0.55, 14, color='gray')

note(s, 'All Presenters', '45 seconds',
     'Lecturers often ask: Where are these data structures used in modern industry? We have mapped each assignment problem to real-world software engineering: Tower of Hanoi governs grandfather-father-son backup rotation schemes; Binary Trees form the foundation of browser DOM rendering and compiler ASTs; Huffman coding is an integral entropy stage in JPEG, MP3, and Gzip; Dijkstra powers OSPF internet packet routing; and Prim’s MST optimizes physical telecommunication cable and electrical power grids.',
     '- Real-world practical applications demonstrated for all 4 assignment topics.\n- Connects academic algorithms to modern engineering systems.',
     ('How does Gzip combine Huffman with other algorithms?',
      'Gzip uses the DEFLATE algorithm, which first applies LZ77 to eliminate duplicate strings by replacing them with distance-length pointers, then applies Huffman coding to compress the resulting literal and distance tokens.'))

# ==========================================
# SLIDE 26: CONCLUSION & REPOSITORY ACCESS
# ==========================================
s = slide('Project Wrap-Up, Repository Access & Q&A.', section='Overview', role='Presenter 1 & Team')
heading(s, 'Project Wrap-Up &\nOpen for Examiner Questions.', w=6.8, h=1.5)
motif(s, 0.8, 4.8, 0.48)

panel(s, 0.8, 2.8, 5.6, 1.8, 'light_mint')
text(s, 'Key Verified Deliverables:\n• 7 Hanoi Moves · 31-Node Tree · 4 Traversals\n• 96 Huffman Bits (30.4% compression savings)\n• Dijkstra A → L = 20 · MST Figure 1 = 35 / Figure 2 = 42\n• 19 Unit Tests Passing · 39-Page Printable Report', 1.0, 3.0, 5.2, 1.4, 15, True)

panel(s, 6.8, 2.8, 5.7, 3.8, 'pale')
text(s, 'Repository & Submission Link:\nhttps://github.com/Eager1337/Data-Structure\n\nSubmission Readiness Checklist:\n✓ Clean source in src/algorithms.py\n✓ Verified test suite with 100% pass rate\n✓ Canonical JSON results & execution logs\n✓ Complete 26-slide presentation with Morph\n✓ Add team member names & IDs before final submission\n✓ Invite lecturer GitHub username to private repo', 7.0, 3.0, 5.3, 3.4, 14)

panel(s, 0.8, 5.7, 5.6, 0.9, 'yellow')
text(s, 'Thank you! We are now open for questions from Lecturer Coker and the examination panel.', 1.0, 5.85, 5.2, 0.6, 16, True, align=PP_ALIGN.CENTER)

note(s, 'Presenter 1 & Team', '45 seconds',
     'In conclusion, we have implemented, verified, and analyzed all four assignment problems in a production-ready, zero-dependency Python package. Every calculation—from the 7 Hanoi moves to the 96 Huffman bits and the 35/42 MST totals—has been independently verified with mathematical cross-checks. Our repository is accessible on GitHub at Eager1337/Data-Structure. On behalf of our entire team, thank you for your time, and we now welcome any questions from Lecturer Coker and the examination panel.',
     '- Formal closing thanking the lecturer and panel.\n- Final callout to GitHub repository Eager1337/Data-Structure.\n- Immediate readiness for examiner Q&A.',
     ('Final concluding remarks ready.', 'Team stands ready for panel questions.'))

# ==========================================
# SAVE PRESENTATION & EXPORT NOTES
# ==========================================
assert len(P.slides) == 26, f"Expected 26 slides, got {len(P.slides)}"
P.core_properties.title = 'DCOMP320 — Data Structures and Algorithm Final Project (Team Presentation & Viva Defense)'
P.core_properties.subject = '26 editable slides with Morph transitions, animations, speaker scripts and complete viva defense'
P.core_properties.author = 'DCOMP320 Project Team · Limkokwing University of Creative Technology'

deck_path = OUTPUT_DIR / "presentation.pptx"
P.save(deck_path)
print(f"Successfully generated and saved master deck to: {deck_path} ({len(P.slides)} slides)")

# Save markdown speaker notes
notes_md_path = OUTPUT_DIR / "speaker-notes.md"
notes_content = [
    "# DCOMP320 — Slide-by-Slide Speaker Notes & Viva Defense Guide\n\n"
    "**Course**: DCOMP320 Data Structures and Algorithms\n"
    "**Institution**: Limkokwing University of Creative Technology, Sierra Leone\n"
    "**Lecturer**: Amandus Benjamin Coker\n"
    "**Deck**: 26 Slides with Native Morph Transitions, Presenter Roles, and Examiner Viva Q&A\n\n"
    "---\n"
]

for i, (title, role, sl) in enumerate(zip(TITLES, ROLES, P.slides), 1):
    notes_content.append(f"## Slide {i:02d}: {title}\n")
    notes_content.append(f"**Presenter Role**: {role}\n\n")
    if sl.has_notes_slide and sl.notes_slide.notes_text_frame:
        notes_content.append(sl.notes_slide.notes_text_frame.text)
    notes_content.append("\n\n---\n")

notes_md_path.write_text("\n".join(notes_content))
print(f"Successfully exported detailed speaker notes to: {notes_md_path}")

# Update outline.md
outline_md_path = OUTPUT_DIR / "outline.md"
outline_content = [
    "# DCOMP320 — 26-Slide Presentation & Viva Defense Outline\n\n"
    "## Overview & Purpose\n"
    "A comprehensive, beginner-friendly and mathematically rigorous English presentation deck designed for a team of students presenting to Lecturer Amandus Benjamin Coker and examination panels at Limkokwing University of Creative Technology, Sierra Leone.\n\n"
    "## Key Upgrades & Features\n"
    "- **Morph Transitions & Visual Glides**: Applied across sequential states (Tower of Hanoi step-by-step moves, Huffman tree building, graph path highlights).\n"
    "- **Team Presentation Blueprint**: Clear presenter badges (`Presenter 1` through `Presenter 4`), timing guides, and speaking scripts.\n"
    "- **Dedicated Viva Defense Section**: 5 dedicated slides addressing the most difficult examiner viva questions (Figure 2 anomaly, Dijkstra vs Prim proof, Level-order FIFO vs DFS LIFO, Huffman greedy proof, Hanoi induction proof).\n"
    "- **Cross-Verification**: 19 automated unit tests, Floyd-Warshall and Kruskal independent validations.\n\n"
    "## Slide Structure (26 Slides)\n"
]

for i, (title, role) in enumerate(zip(TITLES, ROLES), 1):
    outline_content.append(f"{i:02d}. **{title}** (`{role}`)\n")

outline_md_path.write_text("\n".join(outline_content))
print(f"Successfully updated outline to: {outline_md_path}")
