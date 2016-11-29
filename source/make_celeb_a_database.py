"""
Creates two files:
- The first file contains an entry for each face in the second file. This file is necessary in order
  to determine (1) the offset into the second file of the JPG data for a given face, and (2) the
  list of faces corresponding to a given identity.
- The second file consists of the JPG data for all of the faces, concatenated together.

Format of first file:
- uint32: The total number of entries.
- uint32[]: Array consisting of two consecutive integers for each entry. The first is the identity
  of the face; the second is the size of the JPG data of the corresponding image. Since the entries
  are listed in order, the offsets for the entries into the second file can be obtained by computing
  the cumulative sums.

Order of things to try for IO:
- First try reading the file synchronously directly in Lua; we can decode JPG data using
  `image.decompressJPG`.
- Only resort to C++ if this is too slow.
"""

import os
import struct

img_dir        = 'output/celeb_a_cropped'
id_file_path   = '/home/aditya/data/celeb_a/raw/identity_CelebA.txt'
info_file_path = 'output/celeb_a_info.bin'
data_file_path = 'output/celeb_a_data.bin'

assert os.path.isdir(img_dir)
assert os.path.isfile(id_file_path)
assert not os.path.exists(info_file_path)
assert not os.path.exists(data_file_path)

def parse_line(line):
    delim_index = line.find(' ')
    assert delim_index > 0

    name = line[:delim_index]
    id_  = int(line[delim_index + 1:]) - 1
    assert len(name) == 10
    assert id_ >= 0

    entry = int(os.path.splitext(name)[0]) - 1
    assert entry >= 0
    return entry, id_

info_file = open(info_file_path, 'wb')
data_file = open(data_file_path, 'wb')

entry_to_id  = dict(parse_line(line) for line in open(id_file_path, 'r').read().splitlines())
entry_count  = len(entry_to_id)
opened_paths = set()

info_file.write(struct.pack('I', entry_count))

for i, pair in enumerate(sorted(entry_to_id.items())):
    print("Working on entry {} / {}.".format(i + 1, entry_count))
    entry, id_ = pair

    img_name = str(entry + 1)
    img_path = '{}/{}.jpg'.format(img_dir, (6 - len(img_name)) * '0' + img_name)

    assert os.path.isfile(img_path)
    assert img_path not in opened_paths
    opened_paths.add(img_path)

    data = bytearray(open(img_path, 'rb').read())
    info_file.write(struct.pack('II', id_, len(data)))
    data_file.write(data)
