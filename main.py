#! /usr/bin/python3
from PIL import Image
from os import listdir

NEW_SIZE = (8, 8)

HAMMING_DISTANCE_THRESHOLD = 5


def phash(image_path):
    im = Image.open(image_path)
    im = im.resize(NEW_SIZE).convert("L")
    px = im.load()
    # getting average color value
    average_color = 0
    for i in range(NEW_SIZE[0]):
        for j in range(NEW_SIZE[1]):
            average_color += px[i, j]
    average_color = NEW_SIZE[0] * NEW_SIZE[1]
    # converting the image to bits array
    bits_list = []
    for i in range(NEW_SIZE[0]):
        for j in range(NEW_SIZE[1]):
            bits_list.append(1 if px[i, j] > average_color else 0)
    return bits_list


def hamming_distance(bits1, bits2):
    distance = 0
    for i, j in zip(bits1, bits2):
        distance += abs(i - j)
    return distance


def load_images_phash(root_path):
    r = []
    for filename in listdir(root_path):
        r.append((filename, phash(root_path + "/" + filename)))
    return r


def find_similar(images_phash):
    similar_pairs = []
    for i in range(len(images_phash)):
        for j in range(i + 1, len(images_phash)):
            image1_phash = images_phash[i][1]
            image2_phash = images_phash[j][1]
            distance = hamming_distance(image1_phash, image2_phash)
            #print("Distance between %s and %s = %d" % (images_phash[i][0], images_phash[j][0], distance))
            if distance <= HAMMING_DISTANCE_THRESHOLD:
                similar_pairs.append((images_phash[i][0], images_phash[j][0]))
    return similar_pairs


if __name__ == "__main__":
    images_phash = load_images_phash("dev_dataset")
    similar_pairs = find_similar(images_phash)
    for p in similar_pairs:
        print(p)
