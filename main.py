#! /usr/bin/python3
from math import sqrt, cos, pi
from os import listdir

import numpy as np
from PIL import Image

NEW_IMAGE_SIZE = 32
CHECKING_SUB_IMAGE_SIZE = 8

HAAR_FEATURE_SIZE = 4

HAMMING_DISTANCE_THRESHOLD = 12


def p_hash(px):
    # getting average color value
    average_color = 0
    for i in range(CHECKING_SUB_IMAGE_SIZE):
        for j in range(CHECKING_SUB_IMAGE_SIZE):
            if i == j == 0:
                continue
            average_color += px[i, j]
    average_color /= CHECKING_SUB_IMAGE_SIZE * CHECKING_SUB_IMAGE_SIZE - 1
    # converting the image to bits array
    bits_list = []
    for i in range(CHECKING_SUB_IMAGE_SIZE):
        for j in range(CHECKING_SUB_IMAGE_SIZE):
            bits_list.append(1 if px[i, j] > average_color else 0)
    return bits_list


def dct_func(u, v, pixels):
    def c(i):
        return sqrt(1 / NEW_IMAGE_SIZE) if i == 0 else sqrt(2 / NEW_IMAGE_SIZE)

    s = 0
    for k in range(NEW_IMAGE_SIZE):
        for l in range(NEW_IMAGE_SIZE):
            s += pixels[k, l] * cos((2 * k + 1) * u * pi / (2 * NEW_IMAGE_SIZE)) * cos(
                (2 * l + 1) * v * pi / (2 * NEW_IMAGE_SIZE))
    return s * c(u) * c(v)


def dct(pixels):
    res = {}
    for i in range(NEW_IMAGE_SIZE):
        for j in range(NEW_IMAGE_SIZE):
            res[i, j] = dct_func(i, j, pixels)
    return res


# def haar(pixels, size):
#     sum_area_table = {}
#
#     def I(x, y):
#         return 0 if x < 0 or y < 0 else sum_area_table[x, y]
#
#     # calculation sum area table
#     for i in range(size):
#         for j in range(size):
#             sum_area_table[i, j] = pixels[i, j] + I(i, j - 1) + I(i - 1, j) + I(i - 1, j - 1)
#     # building matrix of sums pixels in HAAR_FEATURE_SIZE blocks
#     for i in range()
#         return sum_area_table


def get_pixels(image_path):
    im = Image.open(image_path)
    im = im.resize((NEW_IMAGE_SIZE, NEW_IMAGE_SIZE)).convert("L")
    return im.load()


def hamming_distance(bits1, bits2):
    distance = 0
    for i, j in zip(bits1, bits2):
        distance += abs(i - j)
    return distance


def load_images_p_hash(root_path):
    r = []
    for filename in listdir(root_path):
        cur_image_path = root_path + "/" + filename
        pixels = get_pixels(cur_image_path)
        print("Processing %s ........" % cur_image_path, end="")
        dct_pixels = dct(pixels)
        print("[DONE]")
        r.append((filename, p_hash(dct_pixels)))
    return r


def find_similar(images_p_hash):
    similar_pairs = []
    for i in range(len(images_p_hash)):
        for j in range(i + 1, len(images_p_hash)):
            image1_p_hash = images_p_hash[i][1]
            image2_p_hash = images_p_hash[j][1]
            distance = hamming_distance(image1_p_hash, image2_p_hash)
            print("Distance between %s and %s = %d" % (images_p_hash[i][0], images_p_hash[j][0], distance))
            if distance <= HAMMING_DISTANCE_THRESHOLD:
                similar_pairs.append((images_p_hash[i][0], images_p_hash[j][0]))
    return similar_pairs


def convert_image(src_path, dst_path):
    pixels = get_pixels(src_path)
    d = dct(pixels)
    data = np.zeros((CHECKING_SUB_IMAGE_SIZE, CHECKING_SUB_IMAGE_SIZE), dtype=np.uint8)
    # calculation average pixel value
    av = 0
    for i in range(CHECKING_SUB_IMAGE_SIZE):
        for j in range(CHECKING_SUB_IMAGE_SIZE):
            av += d[i, j]
    av /= CHECKING_SUB_IMAGE_SIZE * CHECKING_SUB_IMAGE_SIZE
    for i in range(CHECKING_SUB_IMAGE_SIZE):
        for j in range(CHECKING_SUB_IMAGE_SIZE):
            data[i, j] = 0 if d[i, j] < av else 255

    img = Image.fromarray(data, 'L')
    img.save(dst_path)


#
# if __name__ == "__main__":
#     images_p_hash = load_images_p_hash("dev_dataset")
#     similar_pairs = find_similar(images_p_hash)
#     print("============================== SIMILAR PAIRS ==============================")
#     for p in similar_pairs:
#         print(p)


if __name__ == "__main__":
    from sys import argv

    src_path = argv[1]
    dst_path = argv[2]
    convert_image(src_path, dst_path)
