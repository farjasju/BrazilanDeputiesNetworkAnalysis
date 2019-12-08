import numpy as np
import random
import os
import json
import re
import csv
import sys
from collections import defaultdict

from string import punctuation, digits

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from custom_stopwords import custom_stopwords

content = "Boa notícia: 🇧🇷 e 🇩🇪 firmam acordo de 40 milhões de euros para apoiar agropecuária sustentável. Os recursos serão destinados a iniciativas relacionadas à bioeconomia, inovação das cadeias produtivas na Amazônia e implementação do Cadastro Ambiental Rural."

DATA_DIR = os.path.join('data', 'deputies_tweets')
OUT_DIR = os.path.join('data', 'deputies_words')

START_YEAR = 2015


def progressBar(value, endvalue, bar_length=50):

    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(
        arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def tweets_to_list_of_words(tweets, stemming=True):
    words = []
    for tweet in tweets:
        text = tweet['full_text']
        text = re.sub(r'http\S+', '', text)  # Removing links
        if int(tweet['created_at'][-4:]) >= START_YEAR:
            words = words + tokenize(text, stemming)
    return words


def tokenize(text, stemming=True):
    words = word_tokenize(text.lower())
    table = str.maketrans('', '', punctuation)
    stripped = [w.translate(table) for w in words]  # Removing ponctuation
    stopwords_pt = set(stopwords.words('portuguese') +
                       list(punctuation) + list(digits) + custom_stopwords)
    if stemming:
        stemmer = nltk.stem.RSLPStemmer()
        words_without_stopwords = [
            stemmer.stem(word) for word in words if word not in stopwords_pt]
    else:
        words_without_stopwords = [
            word for word in words if word not in stopwords_pt]
    return words_without_stopwords


def most_common_words(words, nb=50):
    fdist = FreqDist(words)
    most_common = fdist.most_common(nb)
    return [word[0] for word in most_common]


def main():
    common_dict = []
    nb_deputies = sum([len(files) for r, d, files in os.walk(DATA_DIR)])

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    file_num = 0
    for filename in os.listdir(DATA_DIR):
        file_num += 1
        with open(os.path.join(DATA_DIR, filename), 'r') as f:
            tweets = json.load(f)
            words = tweets_to_list_of_words(tweets, stemming=False)
            common_words = most_common_words(words, nb=50)
        #     with open(os.path.join(OUT_DIR, filename.split('.')[0] + '.csv'), 'w') as csv_file:
        #         writer = csv.writer(csv_file)
        #         writer.writerow(
        #             ['word', 'frequency'])
        #         for word in meaningful_words:
        #             writer.writerow(word)
        progressBar(file_num, nb_deputies, bar_length=50)
        common_dict += common_words
    print(most_common_words(common_dict, 100))


if __name__ == '__main__':
    main()
