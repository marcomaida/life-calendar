#!/usr/bin/env python 
##########################################
# LIFE CALENDAR GENERATOR
# Customize the calendar by changing the config file
##########################################

import math
import helpers
from config import *

##########################################
# Performing some basic checks
##########################################

assert 0 <= group_density_x and group_density_x <= 1, "Group density should be in the range [0,1]"
assert 0 <= group_density_y and group_density_y <= 1, "Group density should be in the range [0,1]"
assert final_year > 0, "There must be at least one year"
assert n_x > 0, "There must be at least one cell in each row"

##########################################
# The cells are organized into GROUPS, whose DENSITY is set in the config. 
# We therefore need to calculate the SIZE of the GAP between two cells of 
# the same group, and of the gap between two groups.
##########################################

# Calculating the total number of rows 
last_birthday = datetime.date(birthday.year + final_year, birthday.month, birthday.day)
total_weeks = math.ceil((last_birthday - birthday).days / 7)
n_y = math.ceil(total_weeks / n_x)

# Total space available, excluding the margins 
total_space_x = canvas_x - margin_left - margin_right
total_space_y = canvas_y - margin_top - margin_bottom

# Total number of gaps
n_gaps_x = n_x - 1
n_gaps_y = n_y - 1

# Number of gaps between cells and number of gaps between groups
n_group_gaps_x = math.ceil(n_x / group_size_x) - 1
n_group_gaps_y = math.ceil(n_y / group_size_y) - 1
n_cell_gaps_x = n_gaps_x - n_group_gaps_x
n_cell_gaps_y = n_gaps_y - n_group_gaps_y
assert n_group_gaps_x + n_cell_gaps_x == n_gaps_x
assert n_group_gaps_y + n_cell_gaps_y == n_gaps_y

# Size of the gap between two cells and between two groups
cell_gap_size_x = total_space_x / n_gaps_x * (1-group_density_x)
cell_gap_size_y = total_space_y / n_gaps_y * (1-group_density_y)
group_gap_size_x = (total_space_x - (cell_gap_size_x * n_cell_gaps_x)) / n_group_gaps_x
group_gap_size_y = (total_space_y - (cell_gap_size_y * n_cell_gaps_y)) / n_group_gaps_y

##########################################
# Drawing the big grid.
# We iterate starting from the birthday and we stop when
# we reach the final birthday.
##########################################

dwg = helpers.setup_canvas(svg_name, canvas_x, canvas_y)

one_week = datetime.timedelta(days=7)
start_x = margin_left + cell_size/2
y_pos = margin_top + cell_size/2
age = -1
date = birthday
next_birthday = birthday
for y in range(n_y):
    assert age < final_year, "Trying to draw after the final birthday"

    # Drawing the years of the current row
    this_year = date.year
    last_cell_year = (date + (n_x-1) * one_week).year
    if this_year == last_cell_year:
        year_header = str(this_year)
    else:
        year_header = f"{this_year} • {last_cell_year}"

    text_height = line_header_size * .75 # Rough estimation of the actual size. Cannot move the anchor to the center, because the PDF converter ignores the dominant baseline attribute
    helpers.text(dwg, start_x - line_header_distance, y_pos + text_height/2, year_header, line_header_color, line_header_size, 'normal','end')

    # Drawing a row
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

        # Drawing a single cell
        if is_birthday: 
            fill = birthday_color if is_gone else 'white'
            is_last_one = age == final_year # The last cell is different
            current_cell_size = last_cell_size if is_last_one else cell_size
            current_border_width = last_cell_border_width if is_last_one else border_width_special_weeks
            helpers.circle (dwg, x_pos, y_pos, current_cell_size, birthday_color, fill, current_border_width)
        elif is_new_year: 
            fill = new_year_color if is_gone else 'white'
            helpers.circle (dwg, x_pos, y_pos, cell_size, new_year_color, fill, border_width_special_weeks)
        else: # normal week
            fill = week_color if is_gone else 'white'
            helpers.circle (dwg, x_pos, y_pos, cell_size, week_color, fill, border_width)

        if age == final_year: break

        date += one_week

        # Next cell - advancing the drawing position for x
        space_group_x = (x+1) % group_size_x == 0
        x_pos += group_gap_size_x if space_group_x else cell_gap_size_x
    
    # Next row - advancing the drawing position for y
    space_group_y = (y+1) % group_size_y == 0
    y_pos += group_gap_size_y if space_group_y else cell_gap_size_y

##########################################
# Drawing title and subtitle
##########################################

helpers.text(dwg, canvas_x/2, margin_top - title_offset, title, title_color, title_size)
helpers.text(dwg, canvas_x/2, margin_top - subtitle_offset, subtitle, subtitle_color, subtitle_size, 'italic')

##########################################
# Creating SVG and PDF 
##########################################

helpers.export(dwg, svg_name, out_name)