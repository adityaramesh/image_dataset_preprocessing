import math
from cars_common import *

# Grayish.
mean_color = 'rgb(119,116,114)'

dst_size = 64
dst_img = Image.new(size=(dst_size, dst_size), mode='RGB', color=mean_color)
dst_draw = ImageDraw.Draw(dst_img)

def process_img(img, bb):
    x1, y1, x2, y2 = bb
    w = x2 - x1 + 1
    h = y2 - y1 + 1

    img_width, img_height = img.size
    assert x1 >= 0
    assert y1 >= 0

    # Just in case the coordinates are somehow outside the image.
    x2 = min(x2, img_width - 1)
    y2 = min(y2, img_height - 1)

    dst_draw.rectangle([(0, 0), dst_img.size], fill=mean_color)
    img = img.crop(box=(x1, y1, x2, y2))

    if w >= h:
        new_height = math.ceil(dst_size * h / w)
        img = img.resize(size=(dst_size, new_height), resample=Image.LANCZOS)
        top = math.floor((dst_size - new_height) / 2)
        dst_img.paste(im=img, box=(0, top))
    else:
        new_width = math.ceil(dst_size * w / h)
        img = img.resize(size=(new_width, dst_size), resample=Image.LANCZOS)
        left = math.floor((dst_size - new_width) / 2)
        dst_img.paste(im=img, box=(left, 0))

    return dst_img

for_each_img_and_bb(process_img, save=True)
