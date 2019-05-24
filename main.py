#! /usr/bin/python3
from PIL import Image
from os import listdir
from math import sqrt, cos, pi

NEW_IMAGE_SIZE = 32
CHECKING_SUB_IMAGE_SIZE = 8

HAMMING_DISTANCE_THRESHOLD = 12


def phash(px):
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
        print("Processing %s ........" % cur_image_path, end="")
        dct_pixels = dct(pixels)
        print("[DONE]")
        r.append((filename, phash(dct_pixels)))
    return r


def find_similar(images_phash):
    similar_pairs = []
    for i in range(len(images_phash)):
        for j in range(i + 1, len(images_phash)):
            image1_phash = images_phash[i][1]
            image2_phash = images_phash[j][1]
            distance = hamming_distance(image1_phash, image2_phash)
            print("Distance between %s and %s = %d" % (images_phash[i][0], images_phash[j][0], distance))
            if distance <= HAMMING_DISTANCE_THRESHOLD:
                similar_pairs.append((images_phash[i][0], images_phash[j][0]))
    return similar_pairs


if __name__ == "__main__":
    images_phash = load_images_phash("dev_dataset")
    similar_pairs = find_similar(images_phash)
    print("============================== SIMILAR PAIRS ==============================")
    for p in similar_pairs:
        print(p)
