import os
import math
import numpy as np
from faces_spacek_common import *

mean = np.zeros(3)
total_count = 0

def process_img(img):
    global mean, total_count

    arr = np.array(img)
    if len(arr.shape) < 3:
        return

    pixel_count = arr.shape[0] * arr.shape[1]
    mean = mean + arr.reshape(pixel_count, 3).sum(0)
    total_count = total_count + pixel_count

for_each_img(process_img)

mean = mean / total_count
print(mean)
#
