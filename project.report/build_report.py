"""Build matched Markdown and A4 PDF report with full source appendices."""
from pathlib import Path
import os
import sys
import textwrap
from html import escape
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.algorithms import *
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
regular = os.environ.get("TAHOMA_REGULAR", str(Path.home()/".local/share/fonts/tahoma/tahoma.ttf"))
bold = os.environ.get("TAHOMA_BOLD", str(Path.home()/".local/share/fonts/tahoma/tahomabd.ttf"))
if not Path(regular).exists() or not Path(bold).exists():
    raise SystemExit("Tahoma fonts not found. Set TAHOMA_REGULAR and TAHOMA_BOLD to licensed TTF files.")
pdfmetrics.registerFont(TTFont("Tahoma", regular))
pdfmetrics.registerFont(TTFont("TahomaBold", bold))
WIDTH = A4[0] - 112
INK, BLUE, LIGHT = HexColor("#162c43"), HexColor("#205a91"), HexColor("#edf3f8")
styles = {
    "body": ParagraphStyle("body",fontName="Tahoma",fontSize=10,leading=11.5,
                            alignment=TA_JUSTIFY,spaceAfter=7,textColor=INK),
    "heading": ParagraphStyle("heading",fontName="TahomaBold",fontSize=10,leading=11.5,
                               spaceBefore=12,spaceAfter=7,textColor=BLUE,keepWithNext=True),
    "title": ParagraphStyle("title",fontName="TahomaBold",fontSize=16,leading=20,
                             alignment=TA_CENTER,spaceAfter=12,textColor=INK),
    "cell": ParagraphStyle("cell",fontName="Tahoma",fontSize=10,leading=11.5,
                            alignment=TA_LEFT,textColor=INK),
    "caption": ParagraphStyle("caption",fontName="Tahoma",fontSize=10,leading=11.5,
                               alignment=TA_LEFT,spaceAfter=10,textColor=BLUE),
    "code": ParagraphStyle("code",fontName="Tahoma",fontSize=10,leading=11.5,
                            alignment=TA_LEFT,spaceAfter=0,textColor=INK),
}
story, md = [], []


def p(text):
    md.append(text+"\n")
    story.append(Paragraph(escape(text),styles["body"]))


def heading(text, level=2, newpage=False):
    if newpage: story.append(PageBreak())
    md.append("#"*level+" "+text+"\n")
    story.append(Paragraph(escape(text),styles["heading"]))


def table(headers, rows, widths=None):
    md.append("| "+" | ".join(map(str,headers))+" |")
    md.append("| "+" | ".join("---" for _ in headers)+" |")
    for row in rows: md.append("| "+" | ".join(map(str,row))+" |")
    md.append("")
    cells = [[Paragraph(escape(str(c)), styles["cell"]) for c in row]
             for row in [headers]+list(rows)]
    t=Table(cells,colWidths=widths or [WIDTH/len(headers)]*len(headers),repeatRows=1,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),LIGHT),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LINEBELOW",(0,0),(-1,0),.7,BLUE),
        ("LINEBELOW",(0,1),(-1,-1),.3,HexColor("#ccd5de")),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]))
    story.extend([t,Spacer(1,8)])


def image(relative,caption,maxheight=335):
    path=HERE/relative
    md.append(f"![{caption}]({path})\n")
    w,h=PILImage.open(path).size
    scale=min(WIDTH/w,maxheight/h)
    story.append(KeepTogether([Image(str(path),width=w*scale,height=h*scale),
                              Paragraph(escape(caption),styles["caption"])]))


def code(text, language="text", numbered=False):
    md.append("```"+language+"\n"+text.rstrip()+"\n```\n")
    wrapped=[]
    for i,line in enumerate(text.splitlines(),1):
        prefix=f"{i:03}  " if numbered else ""
        remaining=prefix+line.expandtabs(4)
        # Width-based soft wrapping preserves 10 pt Tahoma without clipping.
        while pdfmetrics.stringWidth(remaining,"Tahoma",10) > WIDTH-8:
            end=len(remaining)
            while end>1 and pdfmetrics.stringWidth(remaining[:end],"Tahoma",10)>WIDTH-8:
                end-=1
            wrapped.append(remaining[:end])
            remaining="       "+remaining[end:]
        wrapped.append(remaining)
    story.extend([Preformatted("\n".join(wrapped),styles["code"]),Spacer(1,8)])


def fmt(v):return "inf" if v==inf else str(v)


def footer(canvas,doc):
    canvas.setTitle("DCOMP320 Data Structures and Algorithm Final Project")
    canvas.setAuthor("Group members to be completed before submission")
    canvas.setFont("Tahoma",8)
    canvas.setFillColor(BLUE)
    canvas.drawString(50,28,"DCOMP320 | Data Structures and Algorithm")
    canvas.drawRightString(A4[0]-50,28,f"Page {doc.page}")


# Cover
md.append("# DCOMP320 — Data Structures and Algorithm Final Project\n")
story.extend([Spacer(1,70),Paragraph("DATA STRUCTURES AND ALGORITHM<br/>FINAL PROJECT",styles["title"]),Spacer(1,15)])
p("Limkokwing University of Creative Technology — Sierra Leone")
p("Department of Information and Communication Technology")
p("Module: DCOMP320 | Project: Tower of Hanoi and related data-structure problems")
p("Semester: September 2026 to February 2027 | Lecturer: Amandus Benjamin Coker")
p("Prepared: 14 November 2026 | Deadline in brief: Week 4 (calendar date to be confirmed)")
table(["Group member's actual name","Student ID"],[["____________________________","________________"] for _ in range(4)], [WIDTH*.65,WIDTH*.35])
p("Add or remove rows as needed. No identities, signatures, personal contributions or submission actions are invented in this report.")
p("Formatting: Tahoma 10 pt body; line spacing 1.15 (11.5 pt); justified paragraphs. Diagrams, tables and source listings use appropriate non-justified alignment. Headings and cover title provide navigation.")

heading("Contents and result summary",newpage=True)
table(["Section","Contents"],[
    ["1","Introduction, requirements and assumptions"],
    ["2","Tower of Hanoi: recursive solution and all moves"],
    ["3","Binary tree structure and all four traversals"],
    ["4","Huffman construction, codes and encoded length"],
    ["5","Graph transcription, matrices, Dijkstra and Prim on both figures"],
    ["6","Complexity, validation and execution evidence"],
    ["7","Conclusion, reflection guidance and submission"],
    ["References","Assignment and authoritative algorithm/library sources"],
    ["Appendix A","Full Python algorithm source and explanation"],
    ["Appendix B","Full interactive/batch CLI source and explanation"],
    ["Appendix C","Full independent-oracle test source and explanation"],
],[65,WIDTH-65])
table(["Problem","Verified result"],[
    ["Hanoi, n=3","7 moves; all moves legal"],
    ["Tree","31 nodes visited exactly once in each traversal"],
    ["Huffman","96 payload bits; 12 packed payload bytes"],
    ["Figure 1 shortest path","A-D-H-E-J-L; total cost 20"],
    ["Figure 1 MST","35 total edge weight"],
    ["Figure 2 shortest path","L does not exist; A-I-J demonstration has cost 10"],
    ["Figure 2 MST","42 total edge weight"],
    ["Testing","19 passing test methods, with additional parameterized subtests"],
],[WIDTH*.36,WIDTH*.64])

heading("1. Introduction, requirements and assumptions",newpage=True)
p("The supplied final-project brief asks for Python implementations of recursive Tower of Hanoi, four traversals of a supplied binary tree, Huffman coding for five supplied symbol frequencies, and weighted-graph algorithms for two figures. It also requires diagrams, step-by-step explanations, execution screenshots, source appendices, GitHub soft-copy submission and a printed report. The solutions below reproduce the supplied data and make each result independently testable. [1]")
heading("1.1 Why these data structures matter",3)
p("Recursion models a problem through smaller instances and uses Python's call stack to retain unfinished work. Hanoi pegs are LIFO stacks: a disk is removed from or added to the top. Binary-tree nodes organize hierarchical relationships. A FIFO deque supports breadth-first traversal without shifting an entire list. A min-heap chooses the next lowest-frequency Huffman node or lowest-cost graph candidate. An adjacency list stores weighted neighbors, while an adjacency matrix provides a complete, auditable representation of the figures. Python's deque and heapq documentation explain the queue and priority-queue operations used here. [2,3]")
heading("1.2 Scope decisions and ambiguities",3)
table(["Issue in the brief","Treatment in this project"],[
    ["Graphs have no arrowheads","Treat every drawn edge as undirected and record it in both directions."],
    ["Figure 2 has no vertex L","Report A-to-L as not applicable, not unreachable. Compute paths to every actual vertex; show A-to-J as an explicitly separate example."],
    ["Brief groups Prim with shortest paths","Use Dijkstra for source-to-all shortest paths. Implement Prim separately for the MST on both figures. These objectives are not interchangeable. [4,5]"],
    ["Only Huffman frequencies are given","Choose a grouped demonstration message; do not claim that its order was supplied. Weighted encoded length is determined by the frequencies and code lengths."],
    ["Equal Huffman frequencies","Use stable heap insertion order, sorted symbols and left=0/right=1."],
    ["Assessment mentions stacks","Explain the Hanoi peg stacks and recursive call stack; do not invent an additional problem not described in the brief."],
    ["Names/IDs and GitHub account absent","Leave real identity fields for the group and provide submission instructions; do not claim publication or collaborator invitation."],
],[WIDTH*.32,WIDTH*.68])

heading("2. Tower of Hanoi — recursion and stacks",newpage=True)
p("Input n is the number of disks. Disk 1 is smallest. Initially all disks are stacked on source A, largest at the bottom. Auxiliary B and destination C are empty. A legal move transfers exactly one top disk, and no larger disk may be placed on a smaller disk.")
heading("2.1 Algorithm and correctness",3)
p("For zero disks, make no moves. For n>0: (1) move n-1 disks from A to B using C; (2) move disk n from A to C; (3) move n-1 disks from B to C using A. Each call finishes before its parent resumes. The first phase exposes the largest disk, the second places it on the empty destination, and the third puts only smaller disks above it. Induction establishes legality and completion.")
p("Any solution must move the largest disk. Before its first source-to-target transfer, all n-1 smaller disks must be on the spare peg; afterward they must move onto the largest disk. Thus the lower bound is 2T(n-1)+1, and this algorithm achieves it. With T(0)=0, the minimum is T(n)=2^n-1. For n=3, seven moves are necessary and sufficient.")
table(["Step","Move","Peg A (bottom to top)","Peg B","Peg C"],[
    [0,"Initial","3,2,1","empty","empty"],
    [1,"Disk 1: A -> C","3,2","empty","1"],
    [2,"Disk 2: A -> B","3","2","1"],
    [3,"Disk 1: C -> B","3","2,1","empty"],
    [4,"Disk 3: A -> C","empty","2,1","3"],
    [5,"Disk 1: B -> A","1","2","3"],
    [6,"Disk 2: B -> C","1","empty","3,2"],
    [7,"Disk 1: A -> C","empty","empty","3,2,1"],
],[35,140,WIDTH-285,55,55])
image("diagrams/hanoi.png","Figure H1. Initial state and every legal move, n=3.",150)
heading("2.2 Implementation and execution",3)
p("hanoi() yields moves without storing them all. The CLI maintains three list-based peg stacks, checks each pop/append for legality and prints every state. Invalid disk counts are rejected. The CLI permits 0..15 disks to prevent enormous output; the algorithm has no artificial maximum, but recursion and resource limits still apply.")
heading("2.3 Execution evidence",3,newpage=True)
image("screenshots/hanoi.png","Screenshot H2. Actual Python execution, including all seven moves.",245)
p("The displayed peg lists are bottom-to-top. Before each transfer, the demonstration checks that the requested disk is on top of the source and smaller than the current target top. The final state has all disks on C. Automated simulations also check n=0..8; zero disks correctly emits no moves.")

heading("3. Binary tree and traversals",newpage=True)
p("The provided figure is a perfect binary tree labelled in level order from 1 to 31. Node 1 is the root. Each internal node i=1..15 has left child 2i and right child 2i+1. Nodes 16..31 are leaves. The tree has 31 nodes, 15 internal nodes, 16 leaves and height four edges (five levels). This is not a binary search tree: numeric labels encode the pictured structure, not an ordering rule. [1]")
image("diagrams/tree.png","Figure T1. Exact reconstructed tree, including every original node label.",230)
table(["Parent","Left child","Right child"],[[i,2*i,2*i+1] for i in range(1,16)], [WIDTH/3]*3)
root=assignment_tree()
for title,fn,rule,explanation in [
    ("Pre-order",preorder,"root, left, right","Visit root 1, then complete the subtree rooted at 2 before entering the subtree rooted at 3. The first visits are 1,2,4,8,16,17."),
    ("In-order",inorder,"left, root, right","Descend to leaf 16 first, visit its parent 8 after the left subtree, then visit 17. Root 1 is visited only after all 15 nodes in its left subtree."),
    ("Post-order",postorder,"left, right, root","Visit both children before their parent. Nodes 16 and 17 precede node 8. The root is the final visit."),
    ("Level-order",levelorder,"breadth first, FIFO queue","Start with root 1 in a queue. Repeatedly dequeue a node, visit it, then enqueue its left and right children. The five levels appear in increasing label order."),
]:
    heading("3."+str(["Pre-order","In-order","Post-order","Level-order"].index(title)+1)+" "+title,3,newpage=True)
    p("Rule: "+rule+". "+explanation)
    p("Complete visitation sequence: "+", ".join(map(str,fn(root)))+".")
    image("diagrams/"+title.lower()+".png",f"Figure T{[ 'Pre-order','In-order','Post-order','Level-order'].index(title)+2}. {title}: green # labels show visit order, not replacement node values.",260)
    p("Every node is visited exactly once. The recursive traversals append into one result list, avoiding repeated list concatenation. Level-order uses collections.deque and popleft for efficient FIFO behavior. [3]")
image("screenshots/tree.png","Screenshot T6. All four actual traversal outputs.",160)

heading("4. Huffman coding",newpage=True)
freq=dict(zip("abcde",[2,4,8,16,16]))
hr,codes,merges=huffman(freq)
p("The input frequencies are a=2, b=4, c=8, d=16 and e=16, totaling 46 symbols. Huffman's greedy construction repeatedly combines the two least-frequent nodes into a new parent, until one tree remains. Codes are root-to-leaf paths. A min-heap supports each selection; serial numbers ensure equal weights never cause Python to compare non-orderable node objects. [1,2]")
heading("4.1 Step-by-step heap construction",3)
table(["Step","Two minimum nodes","Parent","Remaining weights"],[
    [1,"a:2 + b:4",6,"6,8,16,16"],
    [2,"(a+b):6 + c:8",14,"14,16,16"],
    [3,"((a+b)+c):14 + d:16",30,"16,30"],
    [4,"e:16 + (((a+b)+c)+d):30",46,"46 (root)"],
],[35,WIDTH-205,55,115])
p("For the tied frequencies of d and e, d enters the heap first because symbols are sorted. At the third merge d is therefore selected with the weight-14 subtree. At the last merge e is the left child. Other valid tie choices can produce different bit strings with the same optimal weighted cost. The resulting code is prefix-free because symbols occur only at leaves.")
image("diagrams/huffman.png","Figure C1. Complete Huffman tree, including frequencies, edge bits and symbol codes.",330)
heading("4.2 Final codes and encoded payload length",3)
table(["Symbol","Frequency","Code","Length (bits)","Contribution (bits)"],
      [[s,freq[s],codes[s],len(codes[s]),freq[s]*len(codes[s])] for s in sorted(freq)],
      [60,80,95,100,WIDTH-335])
p("Weighted encoded length = 2(4)+4(4)+8(3)+16(2)+16(1) = 8+16+24+32+16 = 96 bits. The merge-sum check gives 6+14+30+46=96 as well. Average length is 96/46, approximately 2.087 bits per symbol. A fixed-length code for five symbols requires ceil(log2 5)=3 bits per symbol, giving 138 bits; Huffman saves 42 payload bits, approximately 30.4%, before any header or codebook overhead.")
message="".join(s*freq[s] for s in sorted(freq))
bits=encode(message,codes)
p("The brief does not supply an ordered message. For reproducibility only, this demonstration places a twice, b four times, c eight times, d sixteen times and e sixteen times, in grouped alphabetical order. Any other order with the same counts has the same 96-bit length but usually a different encoded bit string.")
code("Message: "+message+"\nEncoded: "+bits)
p("Decoding the encoded string reproduces the exact demonstration message. The 96-bit payload packs into 12 bytes with no padding. This is not a full compressed-file size: a file format would also store decoding information and other metadata. The Python demo prints bits as text and does not claim to implement a binary container format.")
image("screenshots/huffman.png","Screenshot C2. Actual merge sequence, codebook, 96-bit payload and round-trip check.",235)

heading("5. Weighted graphs — Dijkstra and Prim",newpage=True)
p("Both source figures are transcribed as simple undirected weighted graphs. Figure 1 has vertices A..L and Figure 2 has vertices A..J; each has 19 edges. Every weight used by the algorithms is listed below and appears in the diagrams and matrices. Algorithm tests validate the computations on this transcription; visually checking the transcription against the scanned handout is a separate step. [1]")
e1=FIGURE_1_EDGES;e2=FIGURE_2_EDGES
table(["Figure 1 edge","Weight","Figure 2 edge","Weight"],
      [[u+"-"+v,w,x+"-"+y,z] for (u,v,w),(x,y,z) in zip(e1,e2)],
      [WIDTH*.35,WIDTH*.15,WIDTH*.35,WIDTH*.15])
heading("5.1 Dijkstra method and tie handling",3)
p("Initialize distance[A]=0 and all other distances to infinity. Repeatedly pop the unsettled vertex of minimum tentative distance, settle it, and relax every incident edge: if distance[u]+weight(u,v) improves distance[v], update that distance, record predecessor[v]=u and push a new heap entry. Skip entries for already settled vertices. Since all edge weights are non-negative, a settled minimum cannot later be improved through an unsettled vertex. [4]")
p("The implementation uses heap entries (distance, vertex), so alphabetic vertex order resolves equal tentative distances. Neighbors are processed alphabetically and predecessors change only for strictly smaller costs. Equal-cost alternative paths remain valid even if a different implementation reports another predecessor. The algorithm runs to completion, so it returns shortest paths from A to every actual vertex, not only the example destination.")
heading("5.2 Prim method and distinction from shortest paths",3)
p("Begin the tree at A. Put incident candidate edges into a min-heap, select the cheapest edge reaching an unvisited vertex, add that vertex and push its eligible incident edges. Discard heap entries whose destination is already visited. Each selected edge crosses the current visited/unvisited cut; the minimum such edge is safe for an MST. Heap tuples (weight, source, target) resolve ties lexicographically. A connected V-vertex graph produces V-1 tree edges. [5]")
p("Dijkstra minimizes each path's accumulated cost from A. Prim minimizes the sum of all edges connecting the graph; the start vertex is merely where construction begins. An MST is generally not a shortest-path tree. This project applies both algorithms to both figures and labels their objectives separately.")

for num,(name,graph) in enumerate(assignment_graphs().items(),1):
    heading(f"5.{num+2} {name}: graph and adjacency matrix",3,newpage=True)
    image("diagrams/figure_"+str(num)+"_graph.png",f"Figure G{num}a. Redrawn {name}, preserving all vertices, edges and weights.",320)
    vertices,matrix=adjacency_matrix(graph)
    p("Matrix convention: diagonal 0; off-diagonal inf means no direct edge, not zero cost. Symmetry records the undirected interpretation. Row and column order is alphabetical.")
    table([""]+vertices,[[v]+[fmt(w) for w in row] for v,row in zip(vertices,matrix)],
          [WIDTH/(len(vertices)+1)]*(len(vertices)+1))
    distances,prev,trace=dijkstra(graph,"A")
    heading(f"{name}: Dijkstra step-by-step",3,newpage=True)
    p("Each row settles the named vertex at its final shortest distance and records all successful relaxations after inspecting its edges. Unlisted neighbors are not improved. Stale heap entries are skipped and do not constitute an additional settlement.")
    rows=[]
    for i,step in enumerate(trace,1):
        updates="; ".join(f"{v}: {fmt(old)} -> {new} via {u}" for v,old,new,u in step["updates"])
        rows.append([i,step["vertex"],step["distance"],updates or "No improvements"])
    table(["Step","Settle","Cost","Successful relaxation(s)"],rows,[40,50,45,WIDTH-135])
    heading("Tentative distances after each settlement",3)
    table(["Step","Node"]+vertices,
          [[i,step["vertex"]]+[fmt(step["distances"][v]) for v in vertices]
           for i,step in enumerate(trace,1)], [WIDTH/(len(vertices)+2)]*(len(vertices)+2))
    heading(f"{name}: shortest paths from A",3,newpage=True)
    table(["Target","Final cost","Path"],[[v,distances[v]," -> ".join(reconstruct_path(prev,"A",v))] for v in vertices],[65,70,WIDTH-135])
    if num==1:
        p("Required destination L: the lowest-cost path is A -> D -> H -> E -> J -> L. Its total is 4+9+4+2+1=20. The intermediate predecessor chain confirms the same route when followed backward from L. The shortest-path tree rooted at A has total edge weight 43, which is not the MST's 35.")
    else:
        p("The requested A-to-L path cannot be defined on Figure 2 because L is not a vertex. This differs from an existing but unreachable vertex. No L, K or connecting edge is invented. As a separate terminal-vertex demonstration, A -> I -> J has total cost 9+1=10. Dijkstra has still computed every actual A-to-vertex shortest path.")
    image("diagrams/figure_"+str(num)+"_path.png",f"Figure G{num}b. Green edges highlight the shortest example path.",310)
    heading(f"{name}: Prim construction and MST",3,newpage=True)
    mst,total,ptrace=prim(graph,"A")
    table(["Step","Selected edge","Edge weight","Cumulative weight"],
          [[i,u+"-"+v,w,step["total"]] for i,step in enumerate(ptrace,1)
           for u,v,w in [step["edge"]]], [40,WIDTH-250,95,115])
    p(f"The resulting tree has {len(mst)} edges for {len(graph)} vertices, reaches every vertex without adding a cycle, and has total weight {total}. An independent Kruskal implementation confirms this total for every chosen starting vertex.")
    if num==1:
        p("The Figure 1 MST path from A to L is A-D-G-K-H-E-J-L, cost 4+3+4+6+4+2+1=24. It is longer than Dijkstra's cost-20 path, providing a concrete demonstration that an MST does not solve the shortest-path objective.")
    image("diagrams/figure_"+str(num)+"_mst.png",f"Figure G{num}c. Green edges are the Prim MST; total weight {total}.",310)
    heading(f"{name}: actual execution evidence",3,newpage=True)
    image("screenshots/graph"+str(num)+".png",f"Screenshot G{num}d. Actual settlements, paths and Prim results from Python execution.",490)
    p("The screenshot command filters the corresponding portion of a fresh complete run only for readability. The unfiltered run is preserved in outputs/execution.txt; the machine-readable counterpart is outputs/results.json.")

heading("6. Complexity and validation",newpage=True)
p("Notation: n disks; N tree nodes; h tree height; w maximum queue width; k Huffman symbols; L total codebook bit-string lengths; V vertices; E undirected edges. Output storage and educational tracing are distinguished from core auxiliary storage.")
table(["Operation","Time","Space / notes"],[
    ["Hanoi recursive work","Theta(2^n) calls/moves","O(n) stack. Nested Python yield-from propagation can add up to O(n) dispatch per move, so generator runtime is bounded by O(n 2^n)."],
    ["Recursive tree traversal","Theta(N)","O(h) stack plus Theta(N) result list."],
    ["Level-order traversal","Theta(N)","O(w) queue plus Theta(N) result list."],
    ["Huffman heap construction","O(k log k)","O(k) tree and heap."],
    ["Huffman code generation","O(k+L)","O(k+L) tree/code storage; depth up to k-1."],
    ["Encode/decode","Linear in input plus emitted bits/symbols","Stored bit-string and decoded output are linear in their lengths."],
    ["Graph adjacency lists","O(V+E)","O(V+E); undirected edges stored twice."],
    ["Adjacency matrix","Theta(V^2)","Theta(V^2), generated for documentation."],
    ["Dijkstra, core heap work","O((V+E) log V) on simple graphs","O(V+E) graph/heap/maps; lazy duplicate heap entries can occupy O(E)."],
    ["Prim, core lazy heap work","O((V+E) log V) on simple graphs","O(V+E) graph/heap/tree; only connected graphs accepted."],
    ["Tracing in these implementations","Additional O(V^2) time","Additional O(V^2) snapshot storage: Dijkstra distance maps and Prim visited sets."],
],[WIDTH*.29,WIDTH*.29,WIDTH*.42])
p("Hanoi's standard recursive algorithm has Theta(2^n) work; this memory-efficient Python generator additionally passes yielded moves through suspended generator frames. Materializing all moves would require Theta(2^n) storage instead. For a connected simple graph, E>=V-1 and log E=O(log V), so lazy-heap core work is commonly stated as O(E log V). Sorting neighbors for reproducible traces is within this bound. Retained per-step snapshots make the complete traced graph routines O((V+E) log V+V^2) in time and O(V+E+V^2) in storage. These bounds distinguish textbook algorithms from implementation and reporting overhead.")
heading("6.1 Test strategy",3)
table(["Area","Checks performed"],[
    ["Hanoi","Simulate every move for n=0..8; verify top-disk legality, minimum counts, final states, exact n=3 sequence and rejected invalid inputs."],
    ["Tree","Compare all four full sequences with independently specified expected lists; verify every 2i/2i+1 link, all leaves, empty and one-node trees, and a skewed tree."],
    ["Huffman","Check deterministic codes, contributions, merge sum, prefix-free property, empty/large randomized round trips, one-symbol alphabet and malformed inputs. Exhaustively enumerate feasible five-symbol lengths 1..4 under Kraft's inequality to independently confirm the optimal 96-bit cost."],
    ["Dijkstra","Compare all-source distances on both assignment graphs with independent Floyd-Warshall; validate reconstructed edge-path costs; test absent L, zero weights, disconnection and invalid graphs."],
    ["Prim","Compare totals with independent Kruskal for every start vertex on both assignment graphs; check V-1 edge counts and vertex coverage; test a singleton and disconnection."],
    ["Additional graphs","Use deterministic seed 320 to generate nine connected graphs of sizes 2..10. Cross-check paths and MSTs against the independent algorithms."],
    ["Packaging","Compile Python files; verify generated figures, execution evidence and PDF; check ZIP extraction and rerun all tests from the extracted folder."],
],[85,WIDTH-85])
p("All 19 unittest methods pass. Parameterized loops and subtests cover many more input cases than the method count. Tests can prove consistency of implementations and oracles on the chosen inputs; they do not by themselves prove the scanned image was transcribed perfectly. The explicit edge inventory and diagrams make that interpretation auditable.")
image("screenshots/tests.png","Screenshot V1. Actual passing test run; exact runtime can vary between machines.",350)
code("python -m unittest discover -s tests -v\npython main.py --all --disks 3 --json outputs/results.json")

heading("7. Conclusion, reflection and submission",newpage=True)
p("The project implements every described algorithm and reproduces the supplied tree, frequencies and weighted graphs. Hanoi demonstrates recursive decomposition and LIFO legality; tree traversal contrasts recursive depth-first order with FIFO breadth-first order; Huffman demonstrates optimal prefix coding; and the graph solutions contrast shortest-path and spanning-tree optimization. Verified numerical results are seven moves for three disks, a 96-bit Huffman payload, Figure 1 A-to-L cost 20, Figure 1 MST weight 35, and Figure 2 MST weight 42. Figure 2's missing L is stated explicitly.")
heading("7.1 Technical reflection",3)
p("The main implementation challenges are preserving the scanned graph's edge weights, handling equal-priority Huffman nodes deterministically, making base cases and invalid-input behavior explicit, and separating algorithm logic from printing. Returned data enables independent tests; generators avoid storing Hanoi's exponential output; append-based traversals keep linear runtime. The step traces improve explainability but deliberately use quadratic snapshot storage.")
p("A valid personal reflection must come from the actual group members. Before submission, add what each member genuinely learned, the changes they actually made, and any real difficulties they encountered. These technical observations are not presented as fabricated first-person experiences. Follow the university's academic-integrity and assistance-disclosure rules in the supplied brief. [1]")
heading("7.2 Submission and remaining user-side actions",3)
p("The software/report package includes source, tests, complete output logs, a printable PDF, editable Markdown, diagrams, real terminal screenshots, GitHub instructions and individual presentation notes. Fill in genuine names and IDs. Upload the ZIP and project to your own GitHub repository, invite the verified lecturer as collaborator, and submit the link. Print the report and prepare the live presentation. No GitHub upload, invitation, printing or live presentation is claimed to have occurred.")
p("The brief states Week 4 rather than a calendar deadline. Confirm the actual due date with the lecturer. SUBMISSION_CHECKLIST.md gives the upload/print checklist; PRESENTATION_NOTES.md gives an 8–10 minute demo plan and viva answers. No repository URL, lecturer username or group contribution is invented.")

heading("References",newpage=True)
for text in [
    "[1] Limkokwing University of Creative Technology, Sierra Leone. DCOMP320 Data Structures and Algorithm Final Project, supplied four-page scanned brief, semester September 2026–February 2027. Primary source for requirements, tree, frequencies and graph figures.",
    "[2] Python Software Foundation. heapq — Heap queue algorithm, including priority queue implementation notes. https://docs.python.org/3/library/heapq.html (accessed 14 November 2026).",
    "[3] Python Software Foundation. collections — Container datatypes, deque documentation. https://docs.python.org/3/library/collections.html (accessed 14 November 2026).",
    "[4] Sedgewick, R. and Wayne, K. Algorithms, 4th edition companion: 4.4 Shortest Paths. Princeton University. https://algs4.cs.princeton.edu/44sp/ (accessed 14 November 2026).",
    "[5] Sedgewick, R. and Wayne, K. Algorithms, 4th edition companion: 4.3 Minimum Spanning Trees. Princeton University. https://algs4.cs.princeton.edu/43mst/ (accessed 14 November 2026).",
]:p(text)
p("All numerical answers, traversal sequences, diagrams and traces are computed from the assignment data by the submitted Python source. Local HTML copies of external documentation are retained in project.report/sources for audit; external references support algorithm/library descriptions, not substitutes for the project's computations.")

for letter,relative,description in [
    ("A","src/algorithms.py","hanoi is the recursive generator. TreeNode and assignment_tree reconstruct the figure; the traversal functions accumulate results and levelorder uses a deque. HuffmanNode and huffman build the stable heap tree, then encode/decode demonstrate the prefix code. FIGURE_1_EDGES and FIGURE_2_EDGES are the exact graph inventory. make_graph validates symmetry and weights; adjacency_matrix documents non-edges with infinity. dijkstra settles vertices and stores predecessor/trace data; reconstruct_path follows the predecessor chain; prim selects crossing edges and records the MST."),
    ("B","main.py","The CLI accepts an interactive menu or --all batch mode. demo_hanoi maintains and validates real peg stacks, demo_tree prints all orders, demo_huffman prints merges/codes and a decoded round trip, and demo_graphs prints matrices, settlements, every path and Prim edges for both figures. The JSON option replaces infinity with null for strict JSON output. CLI disk limits protect against accidentally huge demonstrations."),
    ("C","tests/test_algorithms.py","Floyd-Warshall and Kruskal are independent oracle implementations, not calls back into Dijkstra or Prim. Test classes cover known examples, boundary/invalid inputs, full tree orders, Huffman optimality and round trips, all-source graph results and deterministically generated random graphs. The exhaustive length search uses Kraft's inequality for independent five-symbol Huffman verification."),
]:
    heading(f"Appendix {letter}. Full source: {relative}",newpage=True)
    p(description)
    p("Line numbers below are report annotations, not part of the source file. Long lines soft-wrap visually at the page width; use the original .py file when running or copying code.")
    code((ROOT/relative).read_text(),"python",numbered=True)

markdown="\n".join(md)+"\n"
HERE.joinpath("content.md").write_text(markdown)
HERE.joinpath("report-portable.md").write_text(markdown.replace(str(HERE)+"/", ""))
doc=SimpleDocTemplate(str(HERE/"report.pdf"),pagesize=A4,
                      rightMargin=50,leftMargin=50,topMargin=42,bottomMargin=45)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print("Created",HERE/"content.md","and",HERE/"report.pdf")