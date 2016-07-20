import re
import os
from PIL import Image, ImageDraw

def for_each_img_and_bb(func, save):
    data_dir = '/home/aditya/data'
    birds_dir = os.path.join(data_dir, 'birds')

    output_dir = 'output/birds_with_bb'
    assert not os.path.exists(output_dir)
    os.mkdir(output_dir)

    print("Creating image ID to path mapping.")

    id_to_img = dict()
    id_to_img_file = os.path.join(birds_dir, 'images.txt')

    with open(id_to_img_file, 'r') as f:
        for line in f:
            img_id, img_path = line.split()
            id_to_img[img_id] = img_path

    print("Creating image to bounding box mapping.")

    img_to_bb = dict()
    bb_file = os.path.join(birds_dir, 'bounding_boxes.txt')

    with open(bb_file, 'r') as f:
        for line in f:
            img_id, x, y, w, h = line.split()
            assert img_id in id_to_img
            img_to_bb[id_to_img[img_id]] = (int(x), int(y), int(w), int(h))

    seen_classes = set()
    birds_img_dir = os.path.join(birds_dir, 'images')

    for i, item in enumerate(img_to_bb.items()):
        img_path, bb = item
        print("Working on image {} / {}.".format(i + 1, len(img_to_bb)))

        img_class, img_id = img_path.split('/')
        input_class_dir = os.path.join(birds_img_dir, img_class)
        output_class_dir = os.path.join(output_dir, img_class)

        if not img_class in seen_classes:
            os.mkdir(output_class_dir)
            seen_classes.add(img_class)

        input_path = os.path.join(input_class_dir, img_id)
        output_path = os.path.join(output_class_dir, re.sub('\..+', '.png', img_id))

        img = Image.open(input_path)
        func(img, bb)

        if save:
            img.save(output_path, 'png')
