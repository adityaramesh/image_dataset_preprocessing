import os
import h5py
import numpy as np
from PIL import Image

birds_dir = 'output/birds_with_bb'
output_path = 'output/birds_v1.hdf5'

assert os.path.isdir(birds_dir)
assert not os.path.exists(output_path)

def count_images():
    def count_files(path):
        return len([1 for _ in os.listdir(path)])
    return sum(count_files(os.path.join(birds_dir, species)) for species in os.listdir(birds_dir))

image_size = 64
image_count = count_images()

output_file = h5py.File(output_path, 'w')
images = output_file.create_dataset('images', (image_count, 3, image_size, image_size), dtype='f')
targets = output_file.create_dataset('targets', (image_count,), dtype='u2')

counter = 0

for species in os.listdir(birds_dir):
    label = int(species)
    species_path = os.path.join(birds_dir, species)

    for img_name in os.listdir(species_path):
        print("Working on image {} / {}.".format(counter + 1, image_count))

        img_path = os.path.join(species_path, img_name)
        img = np.array(Image.open(img_path))

        assert(len(img.shape) == 3)
        img = np.transpose(img, axes=(2, 0, 1))
        img = img / 255

        images[counter] = img
        targets[counter] = label
        counter = counter + 1

output_file.close()
