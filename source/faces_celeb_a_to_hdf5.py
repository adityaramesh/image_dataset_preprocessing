import os
import h5py
import numpy as np

input_path  = 'output/celeb_a_data.bin'
output_path = 'output/celeb_a_data.hdf5'

data = bytearray(open(input_path, 'rb').read())

with h5py.File(output_path, 'w') as f:
    f.create_dataset('data', data=np.array(data))
