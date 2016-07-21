import math
from birds_common import *

dst_size = 64
total_count = 0
skipped_count = 0

def process_img(img, bb):
    global total_count, skipped_count

    x, y, w, h = bb
    img_width, img_height = img.size
    total_count = total_count + 1

    assert x >= 0
    assert y >= 0

    # These assertions can fail, so we need to threshold the width and height of the bounding box.
    # assert x + w - 1 <= img_width
    # assert y + h - 1 <= img_height
    
    w = min(w, img_width - x - 1)
    h = min(h, img_height - y - 1)

    """
    We skip over images for which it is not possible to obtain a square region containing the
    bounding box that can be resized to `dst_size`. The fraction of such images is 7988 / 48562
    (about 16.45% of the dataset).

    TODO: cropping with spatial reflection padding?
    """
    x1, y1, x2, y2 = None, None, None, None

    if w != h:
        if w < h:
            if img_width < h:
                skipped_count = skipped_count + 1
                return

            extra_width = h - w
            y1, y2 = y, y + h - 1

            # We need to determine the left and right endpoints of the region containing the
            # bounding box, so that the region's width comes out to `h`.
            if x <= (img_width - 1) - (x + w - 1):
                # There is more space to the right of the bounding box than to the left. Try to take
                # up to `floor(h / 2)` pixels from the left, and all the rest from the right.
                x1 = max(0, x - math.floor(extra_width / 2))
                x2 = (x + w - 1) + (extra_width - (x - x1))
                assert x2 <= img_width - 1
                assert x2 - x1 + 1 == h
            else:
                # There is more space to the left of the bounding box than to the right. Try to take
                # up to `floor(h / 2)` pixels from the right, and all the rest from the left.
                x2 = min(img_width - 1, (x + w - 1) + math.floor(extra_width / 2))
                x1 = x - (extra_width - (x2 - (x + w - 1)))
                assert x1 >= 0
                assert x2 - x1 + 1 == h
        else:
            if img_height < w:
                skipped_count = skipped_count + 1
                return

            extra_width = w - h
            x1, x2 = x, x + w - 1

            if y <= (img_height - 1) - (y + h - 1):
                y1 = max(0, y - math.floor(extra_width / 2))
                y2 = (y + h - 1) + (extra_width - (y - y1))
                assert y2 <= img_height - 1
                assert y2 - y1 + 1 == w
            else:
                y2 = min(img_height - 1, (y + h - 1) + math.floor(extra_width / 2))
                y1 = y - (extra_width - (y2 - (y + h - 1)))
                assert y1 >= 0
                assert y2 - y1 + 1 == w
    else:
        x1, y1, x2, y2 = x, y, x + w - 1, y + h - 1

    img = img.crop(box=(x1, y1, x2, y2))
    img = img.resize(size=(dst_size, dst_size), resample=Image.LANCZOS)

for_each_img_and_bb(process_img, save=False)

print("Fraction of images skipped: {} / {} ({}%).".format(skipped_count, total_count,
    100 * skipped_count / total_count))
