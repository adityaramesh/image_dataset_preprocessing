import os
import math
import numpy as np
from cars_common import *

mean = np.zeros(3)
total_count = 0

def process_img(img, bb):
    global mean, total_count

    arr = np.array(img)
    if len(arr.shape) < 3:
        return

    pixel_count = arr.shape[0] * arr.shape[1]
    mean = mean + arr.reshape(pixel_count, 3).sum(0)
    total_count = total_count + pixel_count

for_each_img_and_bb(process_img, save=False)

mean = mean / total_count
print(mean)
# [ 118.98718109  116.14844854  114.46902993]
