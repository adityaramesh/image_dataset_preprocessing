from birds_common import *

img_count = 0
border_count = 0

def process_img(img, bb):
    global img_count, border_count

    x, y, w, h = bb
    img_width, img_height = img.size
    img_count = img_count + 1

    if w != h:
        if w < h:
            extra_space = img_width - w
            if w + extra_space < h:
                border_count = border_count + 1
        else:
            extra_space = img_height - h
            if h + extra_space < w:
                border_count = border_count + 1

    """
    # Draws the bounding box on the image.

    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=[(x, y), (x + w, y + h)], fill=None, outline='green')
    del draw
    """

for_each_img_and_bb(process_img, save=False)

print("Images requiring borders after cropping: {} / {} ({}%).".format(border_count, img_count,
    100 * border_count / img_count))
