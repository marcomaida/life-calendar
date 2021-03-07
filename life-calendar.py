import svgwrite
import datetime
from datetime import date
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

##########################################
# Helpers
##########################################

def cell(dwg, x, y, size, is_gone, is_birthday, is_new_year):
    # choose style
    fill = 'black' if is_gone else 'white'
    if is_new_year: fill = 'grey'
    if is_birthday: fill = 'red'

    dwg.add(dwg.circle(center=(x,y),
        r=size, 
        stroke=svgwrite.rgb(15, 15, 15, '%'),
        fill=fill)
    )

def title (dwg, x, y, text):
    dwg.add(dwg.text(text, insert=(x, y), font_size='100pt', fill='black', text_anchor='middle'))

def text (dwg, x, y, text):
    dwg.add(dwg.text(text, insert=(x, y), fill='black'))

def line_header (dwg, x, y, text):
    dwg.add(dwg.text(text, insert=(x, y), fill='black', text_anchor='end'))

def setup_canvas (filename, width, height):
    dwg = svgwrite.Drawing(svg_name, profile='tiny', size=(width,height))
    dwg.add(dwg.rect((0,0), (width, height),fill='white'))

    return dwg

def export (dwg, svg_name, pdf_name):
    dwg.save()

    drawing = svg2rlg(svg_name)
    renderPDF.drawToFile(drawing, pdf_name)

##########################################
# Parameters
##########################################

today = datetime.date.today()
birthday = datetime.date(1994, 8, 13)
#birthday = datetime.date(2000, 1, 1)

svg_name = 'output/out.svg'
out_name = 'output/out.pdf'
canvasx = 2100
canvasy = 2970
size = 10
nx = 52
ny = 90
line_header_distance = 30
marginleft = 200
marginright = 100
marginup = 250
marginbottom = 100
distancex = (canvasx - marginleft - marginright) / nx
distancey = (canvasy - marginup - marginbottom) / ny

##########################################
# Drawing
##########################################

dwg = setup_canvas(svg_name, canvasx, canvasy)

startx = marginleft + size/2
starty = marginup + size/2
date = birthday
next_birthday = birthday
week = datetime.timedelta(days=7)
for y in range(ny):
    y = starty + y * distancey
    
    # Drawing year to the left of each row
    # Check if this row will contain one or two years, set variable accordingly
    this_year = date.year
    last_cell_year = (date + (nx-1) * week).year
    if this_year == last_cell_year:
        year_header = str(this_year)
    else:
        year_header = f"{this_year}-{last_cell_year}"
    line_header(dwg, startx - line_header_distance, y+ size/2, year_header)

    for x in range(nx):
        is_gone = date + week < today

        # Birthday management
        is_birthday = date <= next_birthday and next_birthday <= date + week

        if is_birthday:
            next_birthday = datetime.date(next_birthday.year+1, next_birthday.month, next_birthday.day)

        # New year's eve management
        is_new_year = date.year < (date+week).year

        cell (dwg, startx + x * distancex, y, size,is_gone, is_birthday, is_new_year)

        date += week


title (dwg, canvasx/2, 150, "MY LIFE IN WEEKS")
export(dwg, svg_name, out_name)


"""
dwg.add(dwg.line((20, 20), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line((10, 10), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
"""