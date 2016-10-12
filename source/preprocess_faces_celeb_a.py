import math
from PIL import Image, ImageDraw
from faces_celeb_a_common import for_each_img

# All images in the aligned CelebA dataset have the same dimensions.
src_width  = 178
src_height = 218

final_size = 64
dst_height = math.ceil(src_height * final_size / src_width)

crop_right  = final_size
extra_space = dst_height - final_size
crop_top    = math.floor(extra_space / 2)
crop_bottom = crop_top + final_size

dst_img  = Image.new(size=(final_size, final_size), mode='RGB')
dst_draw = ImageDraw.Draw(dst_img)

def process_img(img):
    img = img.resize(size=(final_size, dst_height), resample=Image.LANCZOS)
    return img.crop(box=(0, crop_top, crop_right, crop_bottom))

for_each_img(process_img)
