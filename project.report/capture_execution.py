"""Capture real xterm windows after actual program execution.

Run with xvfb-run -a python project.report/capture_execution.py.
Uses a FIFO and terminal cursor-position response, not timed sleeps.
"""
from pathlib import Path
import os
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "project.report/screenshots"
OUT.mkdir(exist_ok=True)
cases = {
    "hanoi": ("python main.py --all --disks 3 | sed -n '1,9p'", 16),
    "tree": ("python main.py --all --disks 3 | sed -n '11,15p'", 14),
    "huffman": ("python main.py --all --disks 3 | sed -n '17,30p'", 22),
    "graph1": ("python main.py --all --disks 3 | sed -n '47,85p'", 43),
    "graph2": ("python main.py --all --disks 3 | sed -n '100,134p'", 40),
    "tests": ("python -m unittest discover -s tests -v", 30),
}
for name,(command,rows) in cases.items():
    with tempfile.TemporaryDirectory() as temp:
        fifo = Path(temp)/"ready"
        os.mkfifo(fifo)
        script = (f"cd {shlex.quote(str(ROOT))}; "
                  f"printf '%s\\n\\n' {shlex.quote('$ '+command)}; {command}; "
                  "stty -echo; printf '\\033[?25l\\033[6n'; IFS= read -r -s -d R response; "
                  f"printf ready > {shlex.quote(str(fifo))}; read -r answer")
        proc = subprocess.Popen(["xterm","-fa","DejaVu Sans Mono","-fs","10",
                                 "-geometry",f"140x{rows}+0+0", "-bg","white","-fg","#172c42",
                                 "-title","DCOMP320 execution: "+name,"-e","bash","-c",script])
        with open(fifo) as signal:
            signal.read()
        subprocess.run(["import","-window","root",str(OUT/(name+".png"))],check=True)
        proc.terminate()
        proc.wait(timeout=5)
        # Crop unused Xvfb desktop without touching execution text.
        from PIL import Image
        image=Image.open(OUT/(name+".png")).convert("RGB")
        from PIL import ImageChops
        bbox=ImageChops.difference(image,Image.new("RGB",image.size,"black")).getbbox()
        if bbox:
            image=image.crop(bbox)
        content=ImageChops.difference(image,Image.new("RGB",image.size,"white")).getbbox()
        if content:
            left,top,right,bottom=content
            image=image.crop((max(0,left-8),max(0,top-8),min(image.width,right+8),min(image.height,bottom+8)))
        image.save(OUT/(name+".png"))
    print("Captured",name)