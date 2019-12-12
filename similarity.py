import os
import csv
import math
import numpy as np
from collections import Counter
from itertools import combinations

DATA_DIR = os.path.join('data', 'deputies_words')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def words_to_vector(filename):
    word_vec = dict()
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        reader = csv.reader(f)
        f.readline()
        for word in reader:
            word_vec[word[0]] = int(word[1])
    return word_vec


def main():
    for filename1, filename2 in combinations(os.listdir(DATA_DIR), 2):
        vec1 = words_to_vector(filename1)
        vec2 = words_to_vector(filename2)
        sim = get_cosine(vec1, vec2)
        print(filename1, filename2, sim)


if __name__ == '__main__':
    main()
