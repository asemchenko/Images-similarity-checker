#! /usr/bin/python3
from math import sqrt, cos, pi
from os import listdir

import numpy as np
from PIL import Image

NEW_IMAGE_SIZE = 32

HAMMING_DISTANCE_THRESHOLD = 10


def p_hash(px):
    # getting average color value
    average_color = 0
    amount = 0
    for i in range(8):
        for j in range(8):
            if i == 0:
                continue
            average_color += px[i][j]
            amount += 1
    average_color /= amount
    # converting the image to bits array
    bits_list = []
    for i in range(8):
        for j in range(8):
            bits_list.append(1 if px[i][j] > average_color else 0)
    return bits_list


C = [cos(pi / 16 * i) for i in range(8)]
S = [1 / (4 * val) for val in C]
S[0] = 1 / (2 * sqrt(2))
A = [
    None,
    C[4],
    C[2] - C[6],
    C[4],
    C[6] + C[2],
    C[6],
]


# DCT type II, scaled. Algorithm by Arai, Agui, Nakajima, 1988.
# See: https://web.stanford.edu/class/ee398a/handouts/lectures/07-TransformCoding.pdf#page=30
def transform(m):
    vector = np.array([np.array([m[i, j] for j in range(8)]) for i in range(8)])
    v0 = vector[0] + vector[7]
    v1 = vector[1] + vector[6]
    v2 = vector[2] + vector[5]
    v3 = vector[3] + vector[4]
    v4 = vector[3] - vector[4]
    v5 = vector[2] - vector[5]
    v6 = vector[1] - vector[6]
    v7 = vector[0] - vector[7]

    v8 = v0 + v3
    v9 = v1 + v2
    v10 = v1 - v2
    v11 = v0 - v3
    v12 = -v4 - v5
    v13 = (v5 + v6) * A[3]
    v14 = v6 + v7

    v15 = v8 + v9
    v16 = v8 - v9
    v17 = (v10 + v11) * A[1]
    v18 = (v12 + v14) * A[5]

    v19 = -v12 * A[2] - v18
    v20 = v14 * A[4] - v18

    v21 = v17 + v11
    v22 = v11 - v17
    v23 = v13 + v7
    v24 = v7 - v13

    v25 = v19 + v24
    v26 = v23 + v20
    v27 = v23 - v20
    v28 = v24 - v19

    return [
        S[0] * v15,
        S[1] * v26,
        S[2] * v21,
        S[3] * v28,
        S[4] * v16,
        S[5] * v25,
        S[6] * v22,
        S[7] * v27,
    ]


def get_pixels(image_path):
    im = Image.open(image_path)
    im = im.resize((NEW_IMAGE_SIZE, NEW_IMAGE_SIZE)).convert("L")
    return im.load()


def hamming_distance(bits1, bits2):
    distance = 0
    for i, j in zip(bits1, bits2):
        distance += abs(i - j)
    return distance


def load_images_phash(root_path):
    r = []
    for filename in listdir(root_path):
        cur_image_path = root_path + "/" + filename
        pixels = get_pixels(cur_image_path)
        dct_pixels = transform(pixels)
        r.append((filename, p_hash(dct_pixels)))
    return r


def find_similar(images_phash):
    similar_pairs = []
    for i in range(len(images_phash)):
        for j in range(i + 1, len(images_phash)):
            image1_phash = images_phash[i][1]
            image2_phash = images_phash[j][1]
            distance = hamming_distance(image1_phash, image2_phash)
            if distance <= HAMMING_DISTANCE_THRESHOLD:
                similar_pairs.append((images_phash[i][0], images_phash[j][0]))
    return similar_pairs


def show_help():
    print('''usage: solution.py [-h] --path PATH
    arguments:
        -h show this message and exit
        --path PATH folder with images
    ''')


if __name__ == "__main__":
    from sys import argv

    if len(argv) != 3:
        show_help()
    elif argv[1] == "--path":
        path = argv[2]
        images_phash = load_images_phash(path)
        similar_pairs = find_similar(images_phash)
        for p in similar_pairs:
            print(p[0], p[1])
    else:
        show_help()
