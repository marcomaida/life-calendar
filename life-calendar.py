import svgwrite, datetime, math
from datetime import date
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

##########################################
# Helpers
##########################################

def cell(dwg, x, y, cell_size, is_gone, is_birthday, is_new_year):
    # choose style
    fill = 'black' if is_gone else 'white'
    if is_new_year: fill = 'grey'
    if is_birthday: fill = 'red'

    dwg.add(dwg.circle(center=(x,y),
        r=cell_size, 
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
canvas_x = 2100
canvas_y = 2970
cell_size = 7
n_x = 52
n_y = 90
line_header_distance = 30
margin_left = 200
margin_right = 100
margin_top = 250
margin_bottom = 100

# Cells are grouped horizontally and vertically
group_size_x = 4
group_size_y = 10

# How close are cells of the same group
group_density_x = .2
group_density_y = .6 

assert 0 <= group_density_x and group_density_x <= 1, "Group density should be in the range [0,1]"
assert 0 <= group_density_y and group_density_y <= 1, "Group density should be in the range [0,1]"

# Calculating distance of the dots 
total_space_x = canvas_x - margin_left - margin_right
total_space_y = canvas_y - margin_top - margin_bottom

n_spaces_x = n_x - 1
n_group_spaces_x = math.ceil(n_x / group_size_x) - 1
n_cell_spaces_x = n_spaces_x - n_group_spaces_x
assert n_group_spaces_x + n_cell_spaces_x == n_spaces_x

distance_cells_x = total_space_x / n_spaces_x * (1-group_density_x)
distance_groups_x = (total_space_x - (distance_cells_x * n_cell_spaces_x)) / n_group_spaces_x

distance_y = total_space_y / n_y

##########################################
# Drawing
##########################################

dwg = setup_canvas(svg_name, canvas_x, canvas_y)

startx = margin_left + cell_size/2
starty = margin_top + cell_size/2
date = birthday
next_birthday = birthday
week = datetime.timedelta(days=7)
for y in range(n_y):
    y = starty + y * distance_y
    
    # Drawing year to the left of each row
    # Check if this row will contain one or two years, set variable accordingly
    this_year = date.year
    last_cell_year = (date + (n_x-1) * week).year
    if this_year == last_cell_year:
        year_header = str(this_year)
    else:
        year_header = f"{this_year}-{last_cell_year}"
    line_header(dwg, startx - line_header_distance, y+ cell_size/2, year_header)

    x_pos = startx

    for x in range(n_x):
        is_gone = date + week < today

        # Birthday management
        is_birthday = date <= next_birthday and next_birthday <= date + week

        if is_birthday:
            next_birthday = datetime.date(next_birthday.year+1, next_birthday.month, next_birthday.day)

        # New year's eve management
        is_new_year = date.year < (date+week).year

        cell (dwg, x_pos, y, cell_size,is_gone, is_birthday, is_new_year)

        if (x+1) % group_size_x == 0:
            x_pos += distance_groups_x
        else:
            x_pos += distance_cells_x

        date += week


title (dwg, canvas_x/2, 150, "MY LIFE IN WEEKS")
export(dwg, svg_name, out_name)


"""
dwg.add(dwg.line((20, 20), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line((10, 10), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
"""