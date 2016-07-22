import os
import h5py
import numpy as np
from PIL import Image

faces_dir = 'output/padded_faces'
output_path = 'output/faces_spacek_v1.hdf5'

assert os.path.isdir(faces_dir)
assert not os.path.exists(output_path)

label_file = '/home/aditya/data/faces_spacek/labels.csv'
parts = [line.split(',') for line in open(label_file, 'r').readlines()]
person_to_label = {info[1].rstrip() : int(info[0]) for info in parts}

def count_images():
    def count_files(path):
        return len([1 for _ in os.listdir(path)])
    return sum(count_files(os.path.join(faces_dir, species)) for species in os.listdir(faces_dir))

image_size = 64
image_count = count_images()

output_file = h5py.File(output_path, 'w')
images = output_file.create_dataset('images', (image_count, 3, image_size, image_size), dtype='f')
targets = output_file.create_dataset('targets', (image_count,), dtype='u2')

counter = 0

for person in os.listdir(faces_dir):
    label = person_to_label[person]
    person_path = os.path.join(faces_dir, person)

    for img_name in os.listdir(person_path):
        print("Working on image {} / {}.".format(counter + 1, image_count))

        img_path = os.path.join(person_path, img_name)
        img = np.array(Image.open(img_path))

        assert(len(img.shape) == 3)
        img = np.transpose(img, axes=(2, 0, 1))
        img = img / 255

        images[counter] = img
        targets[counter] = label
        counter = counter + 1

output_file.close()
