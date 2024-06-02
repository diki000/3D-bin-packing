import numpy as np
from objekti import Bin
from inputs import Bin_Length, Bin_Width, Bin_Height, Num_of_Bins, Num_of_Boxes, Boxes

# inputs = {
#     'p': [188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 145, 145, 145, 145, 145],
#     'q': [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 80, 80, 80, 80, 80 ],
#     'r': [58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96],
#     'L': [610, 610, 610, 610],
#     'W': [244, 244, 244, 244],
#     'H': [259, 259, 259, 259]
# }

# boxes = [[p, q, r] for p, q, r in zip(inputs['p'], inputs['q'], inputs['r'])] # boxes to pack

# bins = [Bin([610, 244, 259]) for _ in range(4)] # bins to pack boxes


# Max num of bins : 1
# Bin dimensions (L * W * H): 30 30 50

#   case_id    quantity    length    width    height
# ---------  ----------  --------  -------  --------
# 0          12          5         3        8
# 1          9           12        15       12
# 2          7           8         5        11
# 3          7           9         12       4

bins = [Bin([30,30, 50]) for _ in range(5)] # bins to pack boxes
boxes = []
for i in range(12):
    boxes.append([5, 3, 8])
for i in range(9):
    boxes.append([12, 15, 12])
for i in range(7):
    boxes.append([8, 5, 11])
for i in range(7):
    boxes.append([9, 12, 4])
#bins = [Bin([Bin_Length, Bin_Width, Bin_Height]) for _ in range(Num_of_Bins)] # bins to pack boxes
# boxes = Boxes
number_of_boxes = len(boxes)