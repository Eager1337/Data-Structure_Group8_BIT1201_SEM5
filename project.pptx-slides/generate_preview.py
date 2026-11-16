"""Build one native, editable preview slide; full deck waits for approval."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement

ROOT = Path(__file__).resolve().parent
C = dict(black='111111', gray='505050', mint='A6D8C8', yellow='F4CD59',
         purple='8B78CD', coral='F16F54', pale='F5F6F5', white='FFFFFF')

def text(slide, value, x, y, w, h, size=20, bold=False, color='black',
         font='DM Sans', align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(value.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor.from_string(C.get(color, color))
        p.space_after = Pt(5)
    return box

def shape(slide, kind, x, y, w, h, color):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(C[color])
    s.line.fill.background()
    s._element.spPr.append(OxmlElement('a:effectLst'))
    return s

def motif(slide, x, y, size=.40):
    for i, (kind, color) in enumerate([(MSO_SHAPE.OVAL, 'coral'),
            (MSO_SHAPE.ISOSCELES_TRIANGLE, 'purple'),
            (MSO_SHAPE.RECTANGLE, 'mint'), (MSO_SHAPE.OVAL, 'yellow')]):
        s = shape(slide, kind, x+i*size, y, size, size, color)
        if i == 1:
            s.rotation = 90

def node(slide, label, x, y, leaf=False, code=None):
    d = .68 if leaf else .57
    s = shape(slide, MSO_SHAPE.OVAL, x-d/2, y-d/2, d, d, 'mint' if leaf else 'pale')
    s.text_frame.text = label
    s.text_frame.word_wrap = False
    s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    s.text_frame.margin_left = s.text_frame.margin_right = 0
    s.text_frame.margin_top = s.text_frame.margin_bottom = 0
    for p in s.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.name = 'DM Sans'; p.font.size = Pt(15 if leaf else 16); p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(C['black'])
    if code is not None:
        text(slide, code, x-.45, y+.32, .9, .25, 13, True, 'purple', 'Roboto Mono', PP_ALIGN.CENTER)

def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(C['white'])
    text(slide, 'DCOMP320', .75, .52, 2.2, .25, 11, True, font='Poppins')
    for name, x in [('Hanoi', 4.1), ('Trees', 6.3), ('Huffman', 8.45), ('Graphs', 10.8)]:
        text(slide, name, x, .52, 1.1, .25, 11, name=='Huffman',
             'purple' if name=='Huffman' else 'black')
    text(slide, 'Huffman makes\nfrequent symbols\ncheaper.', .75, 1.47, 5.45, 2.0,
         36, True, font='Poppins')
    shape(slide, MSO_SHAPE.RECTANGLE, .78, 3.75, .035, 1.05, 'purple')
    text(slide, 'Merge the two smallest frequencies.\nRepeat until one tree remains.\nLeft = 0. Right = 1.', 1.0, 3.72, 4.65, 1.25, 19, color='gray')
    text(slide, '2 + 4 = 6    →    6 + 8 = 14\n14 + 16 = 30    →    16 + 30 = 46',
         .78, 5.07, 5.4, .75, 18, True)
    motif(slide, .78, 6.3, .42)
    # Editable connectors, weight labels and leaf codes; exact project tie policy.
    coords = {'root':(9.25,1.65), 'e':(7.7,2.7), '30':(10.4,2.7),
              '14':(9.4,3.75), 'd':(11.7,3.75), '6':(8.5,4.8),
              'c':(10.4,4.8), 'a':(7.7,5.72), 'b':(9.2,5.72)}
    edges = [('root','e','0'),('root','30','1'),('30','14','0'),('30','d','1'),
             ('14','6','0'),('14','c','1'),('6','a','0'),('6','b','1')]
    for a,b,bit in edges:
        x1,y1=coords[a]; x2,y2=coords[b]
        line=slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        line.line.color.rgb=RGBColor.from_string(C['purple']); line.line.width=Pt(1.75)
        mx=(x1+x2)/2; my=(y1+y2)/2
        shape(slide, MSO_SHAPE.OVAL, mx-.12, my-.13, .24, .26, 'white')
        text(slide, bit, mx-.12, my-.13, .24, .26, 13, color='purple', align=PP_ALIGN.CENTER)
    for key,label,code in [('root','46',None),('30','30',None),('14','14',None),('6','6',None),
                            ('e','e:16','0'),('d','d:16','11'),('c','c:8','101'),
                            ('a','a:2','1000'),('b','b:4','1001')]:
        node(slide,label,*coords[key],leaf=code is not None,code=code)
    panel=shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.3, 6.32, 6.25, .62, 'mint')
    panel.adjustments[0]=.18
    text(slide, '96 bits', 6.6, 6.40, 1.55, .4, 23, True, font='Poppins')
    text(slide, 'vs 138 fixed-width · 30.4% less', 8.35, 6.45, 3.9, .33, 17)
    shape(slide, MSO_SHAPE.OVAL, 6.03, 1.33, 1.03, 1.03, 'yellow')
    text(slide, '46\nsymbols', 6.06, 1.48, .97, .67, 15, True, align=PP_ALIGN.CENTER)
    text(slide, 'Payload only; codebook/header excluded.', .78, 7.10, 6.9, .22, 10, color='gray')
    text(slide, '07 / 14', 11.85, 7.10, .73, .22, 10, color='gray', align=PP_ALIGN.RIGHT)
    slide.notes_slide.notes_text_frame.text = (
        'Slide 7 of the planned 14-slide DCOMP320 presentation. Suggested speaking time: 45 seconds.\n'
        'Huffman assigns shorter codes to more frequent symbols. Begin with a=2, b=4, c=8, d=16, e=16. '
        'A min-heap repeatedly removes the two smallest weights: 2+4=6, 6+8=14, 14+16=30, 16+30=46. '
        'The implementation uses sorted symbols and an insertion serial to resolve ties. Left branches are 0; right branches are 1. '
        'Read each leaf path: e=0, d=11, c=101, a=1000, b=1001. '
        'The weighted length is 2×4 + 4×4 + 8×3 + 16×2 + 16×1 = 96 bits. '
        'The merge sum is also 6+14+30+46=96. Five symbols need three bits in a fixed-width code: 46×3=138. '
        'Savings: 42 bits, about 30.4%. These are payload bits only, not a complete compressed file. '
        'Frequencies do not specify message order. Alternative tie decisions may give different but equally optimal codes.\n'
        'Source: src/algorithms.py huffman; outputs/results.json; project report. '
        'This deck and preparation notes are generated assistance; students must verify, understand and disclose use as required by course policy. '
        'No student contribution or personal reflection is being claimed.'
    )
    prs.core_properties.title = 'DCOMP320 — Huffman design preview'
    prs.core_properties.subject = 'One editable preview slide for design approval'
    prs.save(ROOT/'preview.pptx')
    print(ROOT/'preview.pptx')

if __name__ == '__main__':
    build()