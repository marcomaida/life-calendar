##########################################
# HELPERS
# Abstracting away some of the complexity of the SVG creation
##########################################

import svgwrite, datetime, math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from config import *

def circle(dwg, x, y, size, stroke_color, fill_color, border_width):
    assert size > 0
    dwg.add(dwg.circle(center=(x,y),
        r=size/2, 
        stroke=stroke_color,
        stroke_width=border_width,
        fill=fill_color))

def text (dwg, x, y, text, color, font_size, style='normal',text_anchor='middle'):
    text_style = f"""
        font-family: {font_family}; 
        font-style: {style}; 
        """ # Font style is not working in the PDF 

    text = dwg.text(text, 
    insert=(x, y), 
    fill=color,
    style=text_style,
    font_size=font_size,
    text_anchor=text_anchor)

    dwg.add(text)

def setup_canvas (filename, width, height):
    dwg = svgwrite.Drawing(svg_name, size=(width,height))
    dwg.add(dwg.rect((0,0), (width, height),fill='white'))

    return dwg

def export (dwg, svg_name, pdf_name):
    dwg.save()

    drawing = svg2rlg(svg_name)
    renderPDF.drawToFile(drawing, pdf_name)