from birds_common import *

dst_size = 64
dst_img = Image.new(mode='RGB', size=(dst_size, dst_size), color='black')
dst_draw = Image.draw(dst_img)

total_count = 0
skipped_count = 0

def process_img(img, bb):
    x, y, w, h = bb
    img_width, img_height = img.size
    total_count = total_count + 1

    """
    We skip over images for which it is not possible to obtain a square region containing the
    bounding box that can be resized to `dst_size`. The fraction of such images is 7990 / 48562
    (about 16.45% of the dataset).

    TODO: cropping with spatial reflection padding?
    """
    extra_space = 0

    if w != h:
        if w < h:
            extra_space = img_width - w
            if w + extra_space < h:
                return
        else:
            extra_space = img_height - h
            if h + extra_space < w:
                return

    # TODO: compute crop parameters

    # Should not be necessary.
    # dst_draw.rectangle(xy=[(0, 0), dst_img.size], fill='black')

for_each_img_and_bb(process_img, save=True)
