"""Generate exact, data-driven assignment diagrams, not stock imagery."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.algorithms import *

HERE = Path(__file__).resolve().parent
OUT = HERE / "diagrams"
OUT.mkdir(exist_ok=True)
BLUE, INK, GREEN, GRAY = "#205a91", "#162c43", "#148069", "#a7b2bd"
plt.rcParams.update({"font.family":"Tahoma", "font.size":10})


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def tower_diagram():
    pegs = {"A":[3,2,1],"B":[],"C":[]}
    states = [("Initial", {k:v.copy() for k,v in pegs.items()})]
    for i,(disk,u,v) in enumerate(hanoi(3),1):
        pegs[u].pop(); pegs[v].append(disk)
        states.append((f"{i}. Disk {disk}: {u} -> {v}", {k:v.copy() for k,v in pegs.items()}))
    fig, axes = plt.subplots(2,4,figsize=(12,5.3))
    for ax,(title,state) in zip(axes.flat,states):
        for x,peg in enumerate("ABC"):
            ax.plot([x,x],[.18,1.5],color=GRAY,lw=2)
            ax.plot([x-.42,x+.42],[.17,.17],color=INK,lw=2)
            for y,disk in enumerate(state[peg]):
                width=.2+.19*disk
                ax.add_patch(plt.Rectangle((x-width/2,.2+y*.24),width,.2,
                             color=[BLUE,GREEN,"#bb7732"][disk-1]))
                ax.text(x,.3+y*.24,str(disk),ha="center",va="center",color="white",fontsize=9)
            ax.text(x,-.02,peg,ha="center",color=INK)
        ax.set_title(title,fontsize=10,color=INK)
        ax.set(xlim=(-.55,2.55),ylim=(-.2,1.7)); ax.axis("off")
    fig.suptitle("Tower of Hanoi • all seven legal moves for n = 3",fontsize=15,color=INK)
    fig.tight_layout()
    save(fig,"hanoi.png")


def tree_diagram(sequence=None, title="Provided binary tree • 31 nodes, five levels", name="tree.png"):
    pos = {}
    def place(i, lo, hi, depth):
        pos[i] = ((lo+hi)/2, -depth)
        if i<16:
            place(2*i,lo,(lo+hi)/2,depth+1)
            place(2*i+1,(lo+hi)/2,hi,depth+1)
    place(1,0,16,0)
    fig,ax=plt.subplots(figsize=(12,4.6))
    for i in range(1,16):
        for child in (2*i,2*i+1):
            ax.plot([pos[i][0],pos[child][0]],[pos[i][1],pos[child][1]],color=GRAY,lw=1.2)
    order={value:index for index,value in enumerate(sequence or [],1)}
    for i,(x,y) in pos.items():
        ax.scatter(x,y,s=410,color="white",edgecolor=BLUE,lw=1.4,zorder=3)
        ax.text(x,y,str(i),ha="center",va="center",color=INK,fontsize=10,zorder=4)
        if order:
            ax.text(x+.14,y+.26,f"#{order[i]}",fontsize=8,color=GREEN,ha="center",
                    bbox=dict(facecolor="white",edgecolor="none",pad=.4),zorder=5)
    ax.set(xlim=(-.3,16.3),ylim=(-4.65,.65));ax.axis("off")
    ax.set_title(title+ ("\nGreen # labels are visitation positions; circles retain original node labels." if order else ""),fontsize=12,color=INK,pad=15)
    save(fig,name)


def huffman_diagram():
    root,codes,_=huffman(dict(zip("abcde",[2,4,8,16,16])))
    positions={}; leaves=[]
    def locate(node,depth):
        if node.symbol is not None:
            x=len(leaves);leaves.append(node)
        else:
            x=(locate(node.left,depth+1)+locate(node.right,depth+1))/2
        positions[id(node)]=(x,-depth,node)
        return x
    locate(root,0)
    fig,ax=plt.subplots(figsize=(8,5))
    for x,y,node in positions.values():
        if node.symbol is None:
            for bit,child in [("0",node.left),("1",node.right)]:
                cx,cy,_=positions[id(child)]
                ax.plot([x,cx],[y,cy],color=GRAY,lw=1.5)
                ax.text((x+cx)/2,(y+cy)/2,bit,color=GREEN,
                        bbox=dict(facecolor="white",edgecolor="none",pad=2))
        ax.scatter(x,y,s=1000,color="white",edgecolor=BLUE,zorder=3)
        label=str(node.frequency) if node.symbol is None else f"{node.symbol}:{node.frequency}"
        ax.text(x,y,label,ha="center",va="center",color=INK,zorder=4)
        if node.symbol:
            ax.text(x,y-.42,codes[node.symbol],color=GREEN,ha="center",fontsize=10)
    ax.set(xlim=(-.5,4.5),ylim=(-4.75,.65));ax.axis("off")
    ax.set_title("Huffman tree • left = 0, right = 1 • payload = 96 bits",color=INK,fontsize=13,pad=15)
    save(fig,"huffman.png")


POSITIONS = {
    "Figure 1":{"A":(0,4),"B":(2.2,4),"C":(4.4,4),"D":(1.25,2.85),
                "E":(3.3,2.85),"F":(-.65,1.65),"G":(.55,1.65),
                "H":(2,1.65),"I":(3.3,1.65),"J":(4.4,1.65),"K":(1.25,.25),"L":(4.4,.25)},
    "Figure 2":{"A":(0,4.5),"B":(1.7,4.5),"C":(3.5,4.5),
                "D":(1,3.15),"E":(2.25,3.15),"F":(4.5,3.15),
                "G":(2.2,1.7),"H":(3.45,1.7),"I":(1.1,.2),"J":(3.7,.2)}
}


def graph_diagram(name, graph, mode):
    pos=POSITIONS[name]
    distances,previous,_=dijkstra(graph,"A")
    mst,total,_=prim(graph,"A")
    target="L" if "L" in graph else "J"
    path=reconstruct_path(previous,"A",target)
    highlighted = {frozenset((u,v)) for u,v in zip(path,path[1:])} if mode=="path" else (
        {frozenset((u,v)) for u,v,w in mst} if mode=="mst" else set())
    fig,ax=plt.subplots(figsize=(8.6,6.1))
    for u in graph:
        for v,w in graph[u].items():
            if u>=v:continue
            x,y=pos[u];xx,yy=pos[v]
            highlight=frozenset((u,v)) in highlighted
            ax.plot([x,xx],[y,yy],color=GREEN if highlight else GRAY,lw=3 if highlight else 1.3,zorder=1)
            # Move weight labels slightly off the line to separate them.
            dx,dy=xx-x,yy-y
            length=(dx*dx+dy*dy)**.5
            offset=.12
            ax.text((x+xx)/2-dy/length*offset,(y+yy)/2+dx/length*offset,str(w),
                    ha="center",va="center",color=INK,fontsize=10,
                    bbox=dict(facecolor="white",edgecolor="none",pad=1),zorder=2)
    for v,(x,y) in pos.items():
        ax.scatter(x,y,s=1000,color="#e5f3ed" if v in ("A",target) and mode=="path" else "white",edgecolor=BLUE,lw=1.5,zorder=3)
        ax.text(x,y,v,ha="center",va="center",color=INK,fontsize=13,zorder=4)
    subtitle = (f"Shortest A -> {target} path: cost {distances[target]}" if mode=="path" else
                f"Prim minimum spanning tree: total weight {total}" if mode=="mst" else
                f"Transcribed from handout • {len(graph)} vertices, 19 undirected edges")
    ax.set_title(name+" • "+subtitle,fontsize=12,color=INK,pad=20)
    ax.set(xlim=(-1.2,5),ylim=(-.4,5));ax.axis("off")
    save(fig,name.lower().replace(" ","_")+"_"+mode+".png")


if __name__=="__main__":
    tower_diagram();tree_diagram()
    root=assignment_tree()
    for title,fn in [("Pre-order",preorder),("In-order",inorder),("Post-order",postorder),("Level-order",levelorder)]:
        tree_diagram(fn(root),title+" traversal",title.lower()+".png")
    huffman_diagram()
    for name,graph in assignment_graphs().items():
        for mode in ("graph","path","mst"):
            graph_diagram(name,graph,mode)
    print("Generated 13 exact diagrams.")