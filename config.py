##########################################
# CONFIG
# Change your parameters here
##########################################

import datetime

##########################################
# Main Parameters
##########################################

final_year = 50
title = f"MY LIFE BEFORE {final_year}"
subtitle = f"Each dot is a week. Live meaningful days."
birthday = datetime.date(1994, 8, 13)

##########################################
# Detailed Parameters
##########################################

# File
svg_name = 'output/life calendar.svg'
out_name = 'output/life calendar.pdf'

# Dates
today = datetime.date.today()

# Title
title_size = 170
title_offset = 130
title_color = '#151515'

# Subtitle
subtitle_size = 30
subtitle_offset = 80
subtitle_color = '#A0A0A0'

# Canvas
canvas_x = 2100
canvas_y = 2970
margin_left = 250
margin_right = 170
margin_top = 400
margin_bottom = 260

# Cells
week_color = '#4A4A4A'
birthday_color = '#FF4A91'
new_year_color = '#00D8BE'
border_width = 1
border_width_special_weeks = 2
cell_size = 13
last_cell_size = 25
last_cell_border_width = 4

# Dates on the left
line_header_color = '#151515'
line_header_size = 17
line_header_distance = 30

# Layout of the cell grid
n_x = 52                    # How many dots per line?
group_size_x = 4            # How many dots per horizontal group?
group_size_y = 10           # How many dots per vertical group?
group_density_x = .35       # (0 = no grouping, 1 = cells merged together)
group_density_y = .15       # (0 = no grouping, 1 = cells merged together)