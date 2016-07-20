from birds_common import *

dst_size = 64
dst_img = Image.new(mode='RGB', size=(dst_size, dst_size))
dst_draw = Image.draw(dst_img)

total_count = 0
skipped_count = 0

def process_img(img, bb):
    x, y, w, h = bb
    img_width, img_height = img.size
    img_count = img_count + 1

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

    dst_draw.rectangle(xy=[(0, 0), dst_img.size], fill='black')

for_each_img_and_bb(process_img, save=True)
