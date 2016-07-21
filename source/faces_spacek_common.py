import re
import os
from PIL import Image, ImageDraw

duplicated_people = 0

def for_each_img(func):
    global duplicated_people

    counter = 0
    input_img_dir = '/home/aditya/data/faces_spacek/raw'
    output_img_dir = 'output/padded_faces'

    assert not os.path.exists(output_img_dir)
    os.mkdir(output_img_dir)
    seen_ids = set()

    for dataset_dir in os.listdir(input_img_dir):
        dataset_path = os.path.join(input_img_dir, dataset_dir)

        for person_id in os.listdir(dataset_path):
            if person_id in seen_ids:
                duplicated_people = duplicated_people + 1
                continue

            # XXX: there are duplicated people across different datasets.
            # assert not person_id in seen_ids
            seen_ids.add(person_id)

            output_dir = os.path.join(output_img_dir, person_id)
            os.mkdir(output_dir)
            person_path = os.path.join(dataset_path, person_id)

            for img_name in os.listdir(person_path):
                if img_name[0] == '.' or img_name[-1] == '~':
                    continue

                counter = counter + 1
                print("Working on image {}.".format(counter))

                input_path = os.path.join(person_path, img_name)
                output_path = os.path.join(output_dir, re.sub('.jpg', '.png', img_name))

                img = Image.open(input_path)
                new_img = func(img)

                if new_img:
                    new_img.save(output_path, 'png')

    print("Number of duplicated people: {}.".format(duplicated_people))
