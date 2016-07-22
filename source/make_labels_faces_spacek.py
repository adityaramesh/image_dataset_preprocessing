import os
from itertools import chain

output_path = 'output/faces_spacek_labels.csv'
assert not os.path.exists(output_path)

faces_dir = '/home/aditya/data/faces_spacek/raw'
dataset_paths = [os.path.join(faces_dir, dataset) for dataset in os.listdir(faces_dir)]
names = set(chain.from_iterable([id_ for id_ in os.listdir(dp)] for dp in dataset_paths))

with open(output_path, 'w') as f:
    for i, name in enumerate(names):
        print('{},{}'.format(i + 1, name), file=f)
