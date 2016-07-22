import os
import re
import h5py
import numpy as np
from PIL import Image

new_cars_dir = 'output/cars_with_bb'
output_path = 'output/cars_v1.hdf5'

assert os.path.isdir(new_cars_dir)
assert not os.path.exists(output_path)

old_data_dir = '/home/aditya/data'
old_cars_dir = os.path.join(old_data_dir, 'cars')

print("Creating image to class mapping.")

annotations_file = os.path.join(old_cars_dir, 'annotations.csv')
annotations = np.loadtxt(fname=annotations_file, skiprows=1, delimiter=',',
    dtype={'names': ('rel_img_path', 'x1', 'y1', 'x2', 'y2', 'class', 'is_test_image'),
    'formats': ('S64', 'u2', 'u2', 'u2', 'u2', 'u1', 'b')})

def extract_name(path):
    return re.sub('\..+', '.png', path.decode('ascii').split('/')[1])

image_size = 64
img_to_class = {extract_name(path) : class_ for path, _, _, _, _, class_, _ in annotations}
image_count = sum([1 for _ in os.listdir(new_cars_dir)])

output_file = h5py.File(output_path, 'w')
images = output_file.create_dataset('images', (image_count, 3, image_size, image_size), dtype='f')
targets = output_file.create_dataset('targets', (image_count,), dtype='u2')

for i, img_name in enumerate(os.listdir(new_cars_dir)):
    print("Working on image {} / {}.".format(i + 1, image_count))

    img_path = os.path.join(new_cars_dir, img_name)
    img = np.array(Image.open(img_path))

    assert(len(img.shape) == 3)
    img = np.transpose(img, axes=(2, 0, 1))
    img = img / 255

    images[i] = img
    targets[i] = img_to_class[img_name]

output_file.close()
