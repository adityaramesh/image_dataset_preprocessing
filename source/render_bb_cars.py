from cars_common import *

total_count = 0
skipped_count = 0
small_count = 0

def process_img(img, bb):
    global total_count, skipped_count, small_count

    x1, y1, x2, y2 = bb
    img_width, img_height = img.size
    total_count = total_count + 1

    w = x2 - x1 + 1
    h = y2 - y1 + 1

    if w != h:
        if w < h:
            if img_width < h:
                skipped_count = skipped_count + 1
        else:
            if img_height < w:
                skipped_count = skipped_count + 1

    if max(w, h) < 64:
        small_count = small_count + 1

    # Draws the bounding box on the image.

    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=[(x1, y1), (x2, y2)], fill=None, outline='green')
    del draw
    return img

for_each_img_and_bb(process_img, save=True)

print("Images requiring borders after cropping: {} / {} ({}%).".format(skipped_count, total_count,
    100 * skipped_count / total_count))

print("Bounding boxes with largest dimension less than 64: {}.".format(small_count))
