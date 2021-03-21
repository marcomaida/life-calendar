import svgwrite, datetime, math
from datetime import date
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

##########################################
# Helpers
##########################################

def circle(dwg, x, y, size, stroke_color, fill_color, border_width):
    assert size > 0
    dwg.add(dwg.circle(center=(x,y),
        r=size/2, 
        stroke=stroke_color,
        stroke_width=border_width,
        fill=fill_color))

def text (dwg, x, y, text, color, font_size, style='normal',text_anchor='middle'):
    text_style = f"""
        font-family: helvetica;
        font-style: {style};
        """

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

##########################################
# Parameters
##########################################

today = datetime.date.today()
birthday = datetime.date(1994, 8, 13) # MM
# birthday = datetime.date(1997, 11, 24) # MP
# birthday = datetime.date(2000, 1, 1) # First

svg_name = 'output/out.svg'
out_name = 'output/out.pdf'

title_color = '#151515'
subtitle_color = '#909090'
line_header_color = '#151515'
week_color = '#4A4A4A'
birthday_color = '#FF4A91'
new_year_color = '#00D8BE'
border_width = 1
border_width_special_weeks = 2
canvas_x = 2100
canvas_y = 2970

final_year = 50
title = f"MY LIFE BEFORE {final_year}"
title_size = 170
title_offset = 130
subtitle = f"Each dot is a week. Spend them wisely."
subtitle_size = 30
subtitle_offset = 80
cell_size = 13
last_cell_size = 25
border_width_last_cell = 4
n_x = 52
line_header_size = 17
line_header_distance = 30
margin_left = 250
margin_right = 170
margin_top = 400
margin_bottom = 260

# Cells are grouped horizontally and vertically
group_size_x = 4
group_size_y = 10

# How close are cells of the same group
group_density_x = .35
group_density_y = .15

assert 0 <= group_density_x and group_density_x <= 1, "Group density should be in the range [0,1]"
assert 0 <= group_density_y and group_density_y <= 1, "Group density should be in the range [0,1]"

last_birthday = datetime.date(birthday.year + final_year, birthday.month, birthday.day)
total_weeks = math.ceil((last_birthday - birthday).days / 7)
n_y = math.ceil(total_weeks / n_x)

# Calculating distance of the dots 
total_space_x = canvas_x - margin_left - margin_right
total_space_y = canvas_y - margin_top - margin_bottom

n_spaces_x = n_x - 1
n_spaces_y = n_y - 1

n_group_spaces_x = math.ceil(n_x / group_size_x) - 1
n_group_spaces_y = math.ceil(n_y / group_size_y) - 1

n_cell_spaces_x = n_spaces_x - n_group_spaces_x
n_cell_spaces_y = n_spaces_y - n_group_spaces_y

assert n_group_spaces_x + n_cell_spaces_x == n_spaces_x
assert n_group_spaces_y + n_cell_spaces_y == n_spaces_y

distance_cells_x = total_space_x / n_spaces_x * (1-group_density_x)
distance_cells_y = total_space_y / n_spaces_y * (1-group_density_y)

distance_groups_x = (total_space_x - (distance_cells_x * n_cell_spaces_x)) / n_group_spaces_x
distance_groups_y = (total_space_y - (distance_cells_y * n_cell_spaces_y)) / n_group_spaces_y

##########################################
# Drawing
##########################################

dwg = setup_canvas(svg_name, canvas_x, canvas_y)

one_week = datetime.timedelta(days=7)
start_x = margin_left + cell_size/2
start_y = margin_top + cell_size/2
age = -1
date = birthday
next_birthday = birthday
y_pos = start_y
for y in range(n_y):
    # Drawing year to the left of each row
    # Check if this row will contain one or two years, set variable accordingly
    assert age < final_year, "Trying to draw after the final birthday"

    this_year = date.year
    last_cell_year = (date + (n_x-1) * one_week).year
    if this_year == last_cell_year:
        year_header = str(this_year)
    else:
        year_header = f"{this_year} ➤ {last_cell_year}"
    text(dwg, start_x - line_header_distance, y_pos + cell_size/2, year_header, line_header_color, line_header_size, 'normal','end')

    x_pos = start_x

    for x in range(n_x):
        is_gone = date + one_week < today

        # Birthday management
        is_birthday = date <= next_birthday and next_birthday <= date + one_week

        if is_birthday:
            next_birthday = datetime.date(next_birthday.year+1, next_birthday.month, next_birthday.day)
            age +=1

        # New year's eve management
        is_new_year = date.year < (date+one_week).year

        if is_birthday: 
            fill = birthday_color if is_gone else 'white'
            is_last_one = age == final_year
            current_cell_size = last_cell_size if is_last_one else cell_size
            current_border_width = border_width_last_cell if is_last_one else border_width_special_weeks
            circle (dwg, x_pos, y_pos, current_cell_size, birthday_color, fill, current_border_width)
        elif is_new_year: 
            fill = new_year_color if is_gone else 'white'
            circle (dwg, x_pos, y_pos, cell_size, new_year_color, fill, border_width_special_weeks)
        else: # normal week
            fill = week_color if is_gone else 'white'
            circle (dwg, x_pos, y_pos, cell_size, week_color, fill, border_width)

        
        if age == final_year: break


        if (x+1) % group_size_x == 0:
            x_pos += distance_groups_x
        else:
            x_pos += distance_cells_x

        date += one_week
    
    if (y+1) % group_size_y == 0:
        y_pos += distance_groups_y
    else:
        y_pos += distance_cells_y

#Draw title 
text(dwg, canvas_x/2, margin_top - title_offset, title, title_color, title_size)
text(dwg, canvas_x/2, margin_top - subtitle_offset, subtitle, subtitle_color, subtitle_size, 'italic')

export(dwg, svg_name, out_name)

"""
dwg.add(dwg.line((20, 20), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line((10, 10), (2000, 2000), stroke=svgwrite.rgb(10, 10, 16, '%')))
"""

"""
size = size / math.sqrt(2) # we are making a diamond
box = dwg.rect((x-size/2,y-size/2),(size,size),
    stroke=birthday_color,
    fill=fill)
box.rotate(45, center=(x,y))
dwg.add(box)
"""
'''
dwg.add(dwg.rect((x-size/2,y-size/2),(size,size),
    stroke=new_year_color,
    fill=fill))
'''