import math
from faces_spacek_common import *

# Grayish.
mean_color = 'rgb(80,81,76)'

src_width = 180
src_height = 200
dst_size = 64

new_width = math.ceil(dst_size * src_width / src_height)
extra_space = dst_size - new_width
left = math.floor(extra_space / 2)

dst_img = Image.new(size=(dst_size, dst_size), mode='RGB', color=mean_color)
dst_draw = ImageDraw.Draw(dst_img)

def process_img(img):
    dst_draw.rectangle([(0, 0), dst_img.size], fill=mean_color)
    img = img.resize(size=(new_width, dst_size), resample=Image.LANCZOS)
    dst_img.paste(im=img, box=(left, 0))
    return dst_img

for_each_img(process_img)
