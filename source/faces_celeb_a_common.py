import os
from PIL import Image

def for_each_img(func):
    input_img_dir = '/home/aditya/data/celeb_a/raw/img_align_celeba'
    output_img_dir = 'output/celeb_a_cropped'

    assert not os.path.exists(output_img_dir)
    os.mkdir(output_img_dir)

    counter = 0

    for img_name in os.listdir(input_img_dir):
        if img_name[0] == '.' or img_name[-1] == '~':
            continue

        counter = counter + 1
        print("Working on image {}.".format(counter))

        input_path  = os.path.join(input_img_dir, img_name)
        output_path = os.path.join(output_img_dir, img_name)

        img = Image.open(input_path)
        new_img = func(img)

        if new_img:
            new_img.save(output_path, format='jpeg', subsampling=0, quality=100)
