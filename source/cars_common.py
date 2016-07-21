import re
import os
import numpy as np
from PIL import Image, ImageDraw

def for_each_img_and_bb(func, save):
    data_dir = '/home/aditya/data'
    cars_dir = os.path.join(data_dir, 'cars')

    output_img_dir = 'output/cars_with_bb'
    assert not os.path.exists(output_img_dir)
    os.mkdir(output_img_dir)

    print("Creating image info mapping.")

    annotations_file = os.path.join(cars_dir, 'annotations.csv')
    annotations = np.loadtxt(fname=annotations_file, skiprows=1, delimiter=',',
        dtype={'names': ('rel_img_path', 'x1', 'y1', 'x2', 'y2', 'class', 'is_test_image'),
        'formats': ('S64', 'u2', 'u2', 'u2', 'u2', 'u1', 'b')})

    input_img_dir = os.path.join(cars_dir, 'raw/images')

    for i, entry in enumerate(annotations):
        rel_img_path, x1, y1, x2, y2, _, _ = entry
        print("Working on image {} / {}.".format(i + 1, len(annotations)))

        img_id = rel_img_path.decode('ascii').split('/')[1]
        input_path = os.path.join(input_img_dir, img_id)
        output_path = os.path.join(output_img_dir, re.sub('\..+', '.png', img_id))

        img = Image.open(input_path)
        new_img = func(img, (x1, y1, x2, y2))

        if new_img:
            new_img.save(output_path, 'png')
