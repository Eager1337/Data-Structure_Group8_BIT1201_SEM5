"""Rebuild the approved 14-slide deck using native PowerPoint objects.

Requires python-pptx. Algorithm data and code excerpts come from the project.
Run from any directory: python project.pptx-slides/generate_deck.py
"""
from pathlib import Path
from copy import deepcopy
import inspect
import sys
import textwrap
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from generate_preview import text, shape, motif, C

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from src import algorithms as alg

P=Presentation()
P.slide_width=Inches(13.333333); P.slide_height=Inches(7.5)
TITLES=[]

def slide(title, section='', foot='Source: project Python implementation and verified outputs.'):
    s=P.slides.add_slide(P.slide_layouts[6]); TITLES.append(title)
    s.background.fill.solid(); s.background.fill.fore_color.rgb=RGBColor.from_string(C['white'])
    text(s,'DCOMP320',.75,.52,2,.25,11,True,font='Poppins')
    for name,x in [('Hanoi',4.1),('Trees',6.3),('Huffman',8.45),('Graphs',10.8)]:
        text(s,name,x,.52,1.1,.25,11,name==section,'purple' if name==section else 'black')
    text(s,foot,.75,7.1,10.6,.22,10,color='gray')
    text(s,f'{len(P.slides):02d} / 14',11.85,7.1,.73,.22,10,color='gray',align=PP_ALIGN.RIGHT)
    return s

def heading(s,title,x=.75,y=1.25,w=11.8,h=1.3,size=34):
    text(s,title,x,y,w,h,size,True,font='Poppins')

def panel(s,x,y,w,h,color='mint'):
    r=shape(s,MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h,color); r.adjustments[0]=.12
    return r

def note(s,body,source='src/algorithms.py; outputs/results.json; tests/test_algorithms.py'):
    s.notes_slide.notes_text_frame.text=body+'\nSources: '+source+(
        '\nPreparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. '
        'No personal contribution, student identity or university submission is claimed.')

def line(s,x,y,xx,yy,color='purple',width=1.5):
    c=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x),Inches(y),Inches(xx),Inches(yy))
    c.line.color.rgb=RGBColor.from_string(C.get(color,color)); c.line.width=Pt(width)

def circle(s,label,x,y,d=.46,color='mint',size=17):
    q=shape(s,MSO_SHAPE.OVAL,x-d/2,y-d/2,d,d,color)
    tf=q.text_frame; tf.text=str(label); tf.word_wrap=False
    tf.margin_top=tf.margin_bottom=tf.margin_left=tf.margin_right=0
    tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER
    p.font.name='DM Sans'; p.font.size=Pt(size); p.font.bold=True
    p.font.color.rgb=RGBColor.from_string(C['black'])

def code(s,value,x,y,w,h,size=16):
    panel(s,x,y,w,h,'pale')
    box=text(s,value,x+.22,y+.20,w-.44,h-.35,size,font='Roboto Mono')
    for p in box.text_frame.paragraphs: p.space_after=Pt(0)

def excerpt(fn,start,end=None):
    src=inspect.getsource(fn)
    if end is None: return textwrap.dedent(src[src.index(start):]).rstrip()
    return textwrap.dedent(src[src.index(start):src.index(end)]).rstrip()

def table(s,rows,x,y,w,h,widths=None,size=18):
    t=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(h)).table
    if widths:
        for col,v in zip(t.columns,widths): col.width=Inches(v)
    for i,row in enumerate(rows):
        for j,value in enumerate(row):
            cell=t.cell(i,j); cell.text=str(value)
            cell.fill.solid(); cell.fill.fore_color.rgb=RGBColor.from_string(C['mint' if i==0 else ('white' if i%2==0 else 'pale')])
            cell.margin_left=Inches(.15); cell.margin_right=Inches(.1)
            cell.vertical_anchor=MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.font.name='DM Sans'; p.font.size=Pt(size); p.font.bold=i==0
                p.font.color.rgb=RGBColor.from_string(C['black'])
    return t

POS={
 'Figure 1':{'A':(0,4),'B':(2.2,4),'C':(4.4,4),'D':(1.25,2.85),'E':(3.3,2.85),
 'F':(-.65,1.65),'G':(.55,1.65),'H':(2,1.65),'I':(3.3,1.65),'J':(4.4,1.65),'K':(1.25,.25),'L':(4.4,.25)},
 'Figure 2':{'A':(0,4.5),'B':(1.7,4.5),'C':(3.5,4.5),'D':(1,3.15),'E':(2.25,3.15),
 'F':(4.5,3.15),'G':(2.2,1.7),'H':(3.45,1.7),'I':(1.1,.2),'J':(3.7,.2)}}

def graph(s,name,x,y,w,h,mode='path',small=False):
    g=alg.assignment_graphs()[name]; pos=POS[name]
    xs=[v[0] for v in pos.values()]; ys=[v[1] for v in pos.values()]
    pts={k:(x+.3+(a-min(xs))/(max(xs)-min(xs))*(w-.6),
            y+.3+(max(ys)-b)/(max(ys)-min(ys))*(h-.6)) for k,(a,b) in pos.items()}
    dist,prev,_=alg.dijkstra(g,'A'); mst,total,_=alg.prim(g)
    target='L' if 'L' in g else 'J'; path=alg.reconstruct_path(prev,'A',target)
    sel={frozenset((a,b)) for a,b in zip(path,path[1:])} if mode=='path' else {frozenset((a,b)) for a,b,_ in mst}
    edges=[(a,b,weight) for a in g for b,weight in g[a].items() if a<b]
    for a,b,weight in edges:
        if mode=='mst' and frozenset((a,b)) not in sel: continue
        ax,ay=pts[a]; bx,by=pts[b]; chosen=frozenset((a,b)) in sel
        line(s,ax,ay,bx,by,'purple' if chosen else 'BBBBBB',3 if chosen else 1)
        dx=bx-ax; dy=by-ay; length=(dx*dx+dy*dy)**.5
        mx=(ax+bx)/2-dy/length*.10; my=(ay+by)/2+dx/length*.10
        shape(s,MSO_SHAPE.OVAL,mx-.14,my-.13,.28,.26,'white')
        text(s,str(weight),mx-.14,my-.13,.28,.26,12 if small else 14,chosen,align=PP_ALIGN.CENTER)
    for k,(xx,yy) in pts.items(): circle(s,k,xx,yy,.38 if small else .48,'mint' if k in path and mode=='path' else 'pale',14 if small else 18)
    return g,path,dist,mst,total

def tree(s,x,y,w,h):
    pts={}
    def place(i,lo,hi,depth):
        pts[i]=(x+(lo+hi)/2*w,y+depth*h/4)
        if i<16: place(2*i,lo,(lo+hi)/2,depth+1); place(2*i+1,(lo+hi)/2,hi,depth+1)
    place(1,0,1,0)
    for i in range(1,16):
        for j in (2*i,2*i+1): line(s,*pts[i],*pts[j],color='purple',width=1.2)
    for i,(xx,yy) in pts.items(): circle(s,i,xx,yy,.36,'mint' if i>=16 else 'pale',12)

def hanoi_state(s,state,x,y,w,h):
    for k,peg in enumerate('ABC'):
        xx=x+(k+.5)*w/3
        shape(s,MSO_SHAPE.RECTANGLE,xx-.018,y,.036,h-.28,'purple')
        shape(s,MSO_SHAPE.RECTANGLE,xx-w/7,y+h-.29,w/3.5,.035,'black')
        for level,disk in enumerate(state[peg]):
            dw=(.24+.14*disk)*w/3
            shape(s,MSO_SHAPE.ROUNDED_RECTANGLE,xx-dw/2,y+h-.45-level*.20,dw,.18,['coral','mint','yellow'][disk-1])
            text(s,str(disk),xx-dw/2,y+h-.45-level*.20,dw,.18,10,True,align=PP_ALIGN.CENTER)
        text(s,peg,xx-.2,y+h-.22,.4,.22,13,True,align=PP_ALIGN.CENTER)

# 1: editorial cover, algorithm-native visual instead of unrelated photography.
s=slide('Data structures & algorithms, made visible.',foot='Limkokwing University of Creative Technology · Sierra Leone')
motif(s,.8,1.4,.48)
heading(s,'Data structures\n& algorithms,\nmade visible.',y=2.15,w=7.0,h=2.8,size=42)
text(s,'DCOMP320 · Final project\nSeptember 2026–February 2027',.8,5.35,6.7,.8,20,color='gray')
text(s,'Lecturer: Amandus Benjamin Coker',.8,6.48,6.9,.3,16)
for label,sub,x,y,col in [('01','Recursion',8.35,1.6,'coral'),('02','Trees',10.7,2.7,'mint'),('03','Compression',8.35,4,'yellow'),('04','Graphs',10.7,5.1,'purple')]:
    circle(s,label,x,y,1.05,col,30); text(s,sub,x-.95,y+.7,1.9,.45,18,True,align=PP_ALIGN.CENTER)
note(s,'Introduce the four assignment problems and explain that the program is a runnable Python implementation. Target total duration 8–10 minutes. '
     'Student names and IDs are intentionally not fabricated; add the real group details before submission. The printed brief gives the deadline as Week 4 only.',
     'Supplied DCOMP320 assignment; README.md')

# 2: four native rows, project map.
s=slide('Four problems. One reproducible program.')
heading(s,'Four problems.\nOne reproducible program.',w=6.3,h=1.6)
text(s,'Each data structure does a different job.',.8,3.4,5.3,.7,21,color='gray')
code(s,'main.py\nsrc/algorithms.py\ntests/test_algorithms.py\noutputs/results.json',.8,4.45,5.25,1.9,18)
for i,(name,ds,col) in enumerate([('Tower of Hanoi','Recursion / call stack','coral'),('Tree traversals','Binary tree / FIFO queue','mint'),('Huffman coding','Min-heap / prefix tree','yellow'),('Shortest paths + MST','Weighted graph / min-heap','purple')]):
    yy=1.5+i*1.25; circle(s,f'{i+1:02d}',7.05,yy+.28,.60,col,20)
    text(s,name,7.65,yy,4.7,.4,23,True); text(s,ds,7.65,yy+.49,4.7,.42,18,color='gray')
note(s,'Point to main.py as the entry point. Algorithms return data instead of printing directly, which allows tests to verify them independently of the CLI. '
     'The JSON output keeps complete results and traces. No third-party dependencies are needed for the algorithms or their tests.')

# 3: all seven moves in a table alongside native initial and final states.
s=slide('Three disks need seven legal moves.','Hanoi')
heading(s,'Three disks need\nseven legal moves.',w=6.1,h=1.7)
text(s,'Initial state',.8,3.1,2.6,.35,18,True); hanoi_state(s,{'A':[3,2,1],'B':[],'C':[]},.8,3.65,4.9,1.0)
text(s,'After move 7',.8,4.98,2.6,.35,18,True); hanoi_state(s,{'A':[],'B':[],'C':[3,2,1]},.8,5.47,4.9,1.0)
moves=list(alg.hanoi(3)); table(s,[['Step','Disk','Move']]+[[i,d,f'{a} → {b}'] for i,(d,a,b) in enumerate(moves,1)],6.9,1.5,5.5,4.45,[1.25,1.25,3],19)
panel(s,6.9,6.15,5.5,.65,'yellow'); text(s,'2ⁿ − 1  →  2³ − 1 = 7',7.2,6.28,5,.35,22,True)
note(s,'Explain the rules: move one top disk at a time and never place a larger disk on a smaller disk. Lists store pegs bottom-to-top and disk 1 is the smallest. '
     'Read the seven displayed moves. The CLI simulates and validates the moves. The test suite checks legal simulation, count and final state for n=0 through n=8. '
     'The algorithm also accepts n=0 and distinct custom peg names.')

# 4: exact recursive implementation and explanation.
s=slide('Recursion solves a smaller version first.','Hanoi')
heading(s,'Recursion solves a\nsmaller version first.',h=1.4)
code(s,excerpt(alg.hanoi,'    def solve','    return solve'),.8,3.0,7.55,2.65,17)
text(s,'1  Move n−1 disks to spare\n2  Move the largest disk\n3  Move n−1 disks to target',8.75,3.05,3.8,1.75,21,True)
panel(s,8.65,5.0,3.85,1.35,'mint'); text(s,'Base case: k = 0\nStack depth: O(n)',8.95,5.25,3.25,.85,20)
text(s,'T(n) = 2T(n−1) + 1  ·  number of moves = 2ⁿ − 1',.8,6.2,7.5,.5,21,True)
note(s,'Read the exact nested solve function in hanoi. A zero-disk problem yields no moves. yield from delegates to smaller generators; yield emits the move of disk k. '
     'Core recursive move-generation work is Θ(2^n), with O(n) call stack. The nested Python yield-from dispatch can add a factor up to n, so do not describe measured traced Python runtime as only move count. '
     'The wrapper rejects negative/noninteger/bool n and repeated peg names. CLI limits disks to 0..15 to control output.')

# 5: complete native perfect binary tree.
s=slide('A perfect binary tree has five levels.','Trees')
heading(s,'A perfect binary tree\nhas five levels.',w=8.8,h=1.5)
circle(s,'31',11.6,1.8,1.15,'yellow',32); text(s,'nodes',10.95,2.45,1.3,.35,18,True,align=PP_ALIGN.CENTER)
tree(s,.85,3.1,11.7,2.7)
panel(s,.8,6.25,11.75,.62,'mint'); text(s,'Children: 2i, 2i + 1    ·    16 leaves    ·    height = 4 edges    ·    not a BST',1.04,6.39,11.2,.35,19,True)
note(s,'This is the exact assignment tree: node labels 1 to 31 in level order. Internal nodes 1 to 15 have children 2i and 2i+1. '
     'All leaves are at depth four: five levels, height four edges, 16 leaves and 15 internal nodes. It is perfect, full and complete, but not a binary search tree. '
     'A left child can have a larger numeric label than its parent; inorder is therefore not sorted. assignment_tree constructs one object per node and links them.')

# 6: native table; complete sequences in speaker notes.
s=slide('Traversal changes order—not the tree.','Trees')
heading(s,'Traversal changes order—\nnot the tree.',h=1.45)
root=alg.assignment_tree(); sequences={k:fn(root) for k,fn in [('Preorder',alg.preorder),('Inorder',alg.inorder),('Postorder',alg.postorder),('Level order',alg.levelorder)]}
rules=['Root → left → right','Left → root → right','Left → right → root','Level by level (FIFO)']
table(s,[['Traversal','Rule','First eight visits']]+[[name,rule,', '.join(map(str,vals[:8]))+' …'] for (name,vals),rule in zip(sequences.items(),rules)],.8,3.05,11.75,2.35,[2.2,4.05,5.5],18)
code(s,'node = queue.popleft()\nresult.append(node.value)',.8,5.72,5.6,1.02,17)
text(s,'Recursive traversals append once per node.\nLevel order uses deque: append + popleft.',6.75,5.9,5.65,.85,19,color='gray')
note(s,'Compare where root is visited relative to its subtrees. Each recursive traversal appends into one shared result list, avoiding costly repeated list concatenation. '
     'Level order uses collections.deque, a FIFO queue, with approximately O(1) append and popleft. All traversals take O(n) work and O(n) returned-list storage. '
     'Recursive auxiliary stack is O(h); the queue can store O(width) nodes. Complete actual sequences:\n'+ '\n'.join(k+': '+', '.join(map(str,v)) for k,v in sequences.items()))

# 7: approved native preview retained without rebuilding its composition.
preview=Presentation(HERE/'preview.pptx'); s=P.slides.add_slide(P.slide_layouts[6])
for el in preview.slides[0].shapes:
    s.shapes._spTree.insert_element_before(deepcopy(el._element),'p:extLst')
s.notes_slide.notes_text_frame.text=preview.slides[0].notes_slide.notes_text_frame.text
TITLES.append('Huffman makes frequent symbols cheaper.')

# 8: actual code and native codebook table.
s=slide('A min-heap builds a prefix-free code.','Huffman')
heading(s,'A min-heap builds\na prefix-free code.',h=1.4)
code(s,excerpt(alg.huffman,'    while len(heap) > 1:','        label ='),.8,3.0,7.2,1.8,16)
code(s,excerpt(alg.huffman,'    def walk','    walk(root'),.8,4.98,7.2,1.96,14)
_,codes,_=alg.huffman(dict(zip('abcde',[2,4,8,16,16])))
table(s,[['Symbol','Code','Bits']]+[[a,codes[a],f'{f} × {len(codes[a])}'] for a,f in zip('abcde',[2,4,8,16,16])],8.4,3.0,4.1,2.9,[1.35,1.35,1.4],17)
panel(s,8.4,6.1,4.1,.62,'yellow'); text(s,'"ab" → 10001001 → "ab"',8.57,6.26,3.85,.3,16,True,font='Roboto Mono')
note(s,'Symbols are leaves, so no symbol code can be a prefix of another. Read the heap code: pop two minima, form a parent, push it back. '
     'Code walking appends 0 to the left and 1 to the right; single-symbol input gets code 0. The project implements encode and decode with validation. '
     'Sorted leaf symbols and a serial insertion key produce stable equal-frequency ties. The two symbols a and b encode as 1000 + 1001 and round-trip to ab. '
     'This short message is an illustration, not the 46-symbol frequency input. The full grouped demonstration has 96 payload bits (12 packed bytes, no padding), excluding headers. '
     'Huffman construction uses O(k log k) heap work for k distinct symbols; message encoding and decoding are proportional to processed symbols/bits.')

# 9–10: full graphs with all exact weights, highlighted shortest paths.
for name,target,total in [('Figure 1','L',20),('Figure 2','J',10)]:
    isone=name=='Figure 1'
    s=slide('Figure 1: the shortest A-to-L route costs 20.' if isone else 'Figure 2 has no vertex L.','Graphs')
    heading(s,'Figure 1: the shortest\nA-to-L route costs 20.' if isone else 'Figure 2 has\nno vertex L.',w=6.0,h=1.9,size=32 if isone else 36)
    text(s,'12 vertices · 19 undirected edges' if isone else '10 vertices · 19 undirected edges',.8,3.42,5.0,.65,19,color='gray')
    if isone:
        panel(s,.8,4.55,5.45,1.3,'mint'); text(s,'A → D → H → E → J → L\n4 + 9 + 4 + 2 + 1 = 20',1.03,4.82,5,.82,22,True)
    else:
        panel(s,.8,4.42,5.2,.78,'yellow'); text(s,'A → L: not applicable',1.05,4.6,4.7,.4,23,True)
        text(s,'Separate example: A → I → J\n9 + 1 = 10',.8,5.57,5.3,.87,22,True)
    g,path,dist,mst,weight=graph(s,name,6.75,1.48,5.7,5.25)
    motif(s,.8,6.62,.26) if isone else None
    note(s,f'{name}: each drawn edge is undirected because the handout shows no arrowheads. The graph contains exactly {len(g)} vertices and 19 edges. '
         + ('Dijkstra yields A-D-H-E-J-L with cost 20. Purple edges mark that route, not an MST. ' if isone else 'There is no L in the input. A-to-L is not applicable, not a merely unreachable target. Do not invent L or silently replace it. A-I-J with cost 10 is a separately labelled demonstration. ')
         +'Distances from A: '+', '.join(f'{k}={v}' for k,v in dist.items())+'. '
         +'Dijkstra maintains tentative distances and predecessor pointers. Nonnegative weights justify finalizing the smallest unsettled distance. Complete settlement/update traces are in outputs/results.json.')

# 11: selected-edge native MSTs with exact totals.
s=slide('Shortest route ≠ cheapest spanning tree.','Graphs')
heading(s,'Shortest route ≠\ncheapest spanning tree.',h=1.4)
for name,x,col in [('Figure 1',.9,'mint'),('Figure 2',7.0,'yellow')]:
    _,_,_,edges,total=graph(s,name,x,3.07,5.2,2.95,mode='mst',small=True)
    text(s,f'{name} · MST weight {total}',x,2.65,5.2,.35,21,True)
panel(s,.8,6.42,11.7,.47,'mint'); text(s,'Figure 1: shortest-path tree = 43  ·  MST = 35  ·  A-to-L along MST = 24',1.02,6.51,11.25,.3,18,True)
note(s,'Prim minimizes total edge weight while connecting every vertex without cycles. Only the chosen MST edges are drawn here. '
     'Figure 1 selected edges: '+str(alg.prim(alg.assignment_graphs()['Figure 1'])[0])+'. '
     'Figure 2 selected edges: '+str(alg.prim(alg.assignment_graphs()['Figure 2'])[0])+'. '
     'Totals are 35 and 42. A shortest-path tree rooted at A has total edge weight 43 in Figure 1, not 35. '
     'The MST path A-D-G-K-H-E-J-L costs 4+3+4+6+4+2+1=24, while the shortest route costs 20. '
     'This is why Prim must not be reported as a shortest-path algorithm. Independent Kruskal tests confirm both MST totals from all starts.')

# 12: exact core excerpts, different greedy priorities.
s=slide('Dijkstra and Prim use the heap differently.','Graphs')
heading(s,'Same heap.\nDifferent greedy decisions.',h=1.4)
text(s,'DIJKSTRA · distance from source',.8,2.88,5.65,.35,20,True)
code(s,'candidate = distance + weight\nif (v not in settled and\n    candidate < distances[v]):\n    distances[v], previous[v] = candidate, u\n    heapq.heappush(heap, (candidate, v))',.8,3.42,5.65,1.77,13)
text(s,'PRIM · lightest crossing edge',6.9,2.88,5.65,.35,20,True)
code(s,excerpt(alg.prim,'        weight, u, v =','        total +='),6.9,3.42,5.65,1.77,15)
text(s,'Adjacency lists store neighbors + weights.\nMatrix: diagonal 0; no direct edge = ∞.',.8,5.52,5.65,.85,19,color='gray')
text(s,'Core heap work: O((V + E) log V)\nEducational snapshots add O(V²).',6.9,5.52,5.65,.85,19,color='gray')
panel(s,.8,6.45,11.75,.45,'yellow'); text(s,'Dijkstra optimizes a route. Prim optimizes the whole tree.',1.05,6.52,11.2,.3,19,True)
note(s,'The Dijkstra display reproduces the core relaxation logic with a line-wrapped condition; old-distance trace logging is omitted. distance is an accumulated source-to-u cost. Relaxation tries distance + weight and pushes an improved candidate. '
     'In Prim the heap key is one edge weight; edges leading to already-visited vertices are skipped. '
     'The graph is a dict of neighbor dicts; make_graph adds both directions and validates symmetry, finite nonnegative weights and no duplicates/self-loops. '
     'An adjacency matrix uses zero on the diagonal and infinity for absent edges; exported JSON uses null for infinity. '
     'Core heap work is O((V+E) log V) for these simple graphs; heap/list storage depends on edges and vertices. '
     'Copying distances and recording visited snapshots adds O(V²) time/storage. Negative weights are rejected for this project; disconnected Prim raises an error.')

# 13: evidence matrix; no fabricated screenshot.
s=slide('19 test methods pass—with independent checks.')
heading(s,'19 test methods pass.\nIndependent checks matter.',h=1.4)
table(s,[['Problem','Independent check'],['Hanoi','Legal-state simulation · n = 0…8'],['Tree','Exact sequences + shape / edge cases'],['Huffman','Round trip + exhaustive feasible code lengths'],['Dijkstra','Floyd–Warshall · every source, both graphs'],['Prim','Kruskal · every start, both graphs']],.8,3.0,11.7,2.6,[2.65,9.05],19)
code(s,'python -m unittest discover -s tests -v',.8,5.95,8.0,.79,17)
text(s,'Also: 9 seeded random graphs\nCLI invalid-input recovery',9.1,5.98,3.45,.76,16,color='gray')
note(s,'19 unittest methods pass, with additional parameterized subtests. The builder does not fabricate a terminal screenshot; the actual output logs are in outputs/test-results.txt and execution screenshots in project.report/screenshots. '
     'Graph tests compare against independent Floyd–Warshall and Kruskal implementations, not only hard-coded expectations. Random connected graphs cover sizes 2 through 10 with seed 320. '
     'Huffman exhaustive feasible five-symbol code-length combinations confirm minimum 96 bits. Invalid input, empty/single/skew trees, disconnected/zero-weight/single-vertex graphs and malformed Huffman streams are checked. '
     'CLI smoke checks include all menu choices, invalid-input recovery, zero disks and --disks -1 returning exit code 2. Run the displayed command live if time permits.')

# 14: executable next steps, clear submission caveats and live hyperlink.
s=slide('Run it. Explain it. Verify it.',foot='Sources: Python heapq/deque docs · Princeton Algorithms, shortest paths / MST · supplied assignment')
heading(s,'Run it.\nExplain it.\nVerify it.',w=6.5,h=2.55,size=42)
motif(s,.8,4.75,.48)
text(s,'7 Hanoi moves · 96 Huffman bits\nRoutes: 20 / 10 · MSTs: 35 / 42',.8,5.55,5.75,.9,21,True)
code(s,'python main.py\npython main.py --all --disks 3\npython -m unittest discover -s tests -v',6.35,1.6,6.2,1.95,15)
text(s,'Read START_HERE.md first.',6.55,4.0,5.6,.5,24,True)
box=text(s,'github.com/Eager1337/\ndcomp320-final-project',6.55,4.7,5.6,.86,21,color='purple')
for p in box.text_frame.paragraphs:
    for r in p.runs: r.hyperlink.address='https://github.com/Eager1337/dcomp320-final-project'
text(s,'Before submission: real names/IDs, lecturer\naccess, printing and your own explanation.',6.55,5.9,5.65,.83,18,color='gray')
note(s,'Close with the key results and invite questions. The repository is private, so lecturer access needs an invitation to a verified GitHub username. '
     'The report is 39 A4 pages with the required Tahoma body formatting; print and submit as instructed. Deadline is Week 4 in the brief—no exact date is specified. '
     'Add real student names/IDs, disclose assistance as required, and do not claim invented group contributions. '
     'The beginner walkthrough explains every concept and command; the final editable deck, builder and complete ZIP are included. '
     'Reference URLs: https://docs.python.org/3/library/heapq.html ; https://docs.python.org/3/library/collections.html ; '
     'https://algs4.cs.princeton.edu/44sp/ ; https://algs4.cs.princeton.edu/43mst/ .',
     'README.md; START_HERE.md; SUBMISSION_CHECKLIST.md; supplied assignment; project.report/report-portable.md')

assert len(P.slides)==14
P.core_properties.title='DCOMP320 — Data Structures and Algorithm Final Project'
P.core_properties.subject='14 editable slides with speaker notes, verified code and native diagrams'
P.core_properties.author='DCOMP320 project group — add real student details'
P.save(HERE/'presentation.pptx')
(HERE/'speaker-notes.md').write_text('# DCOMP320 — slide-by-slide speaker notes\n\n'+ '\n\n'.join(
    f'## {i}. {title}\n\n'+sl.notes_slide.notes_text_frame.text for i,(title,sl) in enumerate(zip(TITLES,P.slides),1)))
print('Built',HERE/'presentation.pptx','—',len(P.slides),'slides, native objects and speaker notes.')