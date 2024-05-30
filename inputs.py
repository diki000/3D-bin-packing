import numpy as np
from objekti import Bin

Bin_Length = 100 # length of the bin
Bin_Height = 100 # height of the bin
Bin_Width = 100 # width of the bin

numbers_of_bins = 20 # number of bins
number_of_boxes = 10 # number of boxes

boxes = []
for i in range(number_of_boxes):
    box = [np.random.uniform(1/6*Bin_Length, 1/4*Bin_Length), np.random.uniform(1/6*Bin_Height, 1/4*Bin_Height), np.random.uniform(1/6*Bin_Width, 1/4*Bin_Width)]
    boxes.append(box)
bins = [Bin([Bin_Length, Bin_Height, Bin_Width]) for _ in range(numbers_of_bins)] # bins to pack boxes into