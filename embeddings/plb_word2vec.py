import sys
from collections import Counter
import math
import random
import os
import pickle


class Corpus(object):
    def __init__(self, filepath):
        with open(filepath) as f:
            self.words = f.read().split()
            self.update()

    def update(self):
        self.counts = Counter(self.words)

        total = len(self.words)
        self.frequencies = {
            word: count / total for word, count in self.counts.most_common()
        }

        self.word2index = {}
        self.index2word = []

        for i, t in enumerate(self.counts.most_common()):
            word = t[0]
            self.word2index[word] = i
            self.index2word.append(word)

    def eliminate_below_frequency(self, frequency):
        self.words = [
            word for word in self.words if self.counts[word] > frequency
        ]
        self.update()

    def subsample(self):
        self.words = [
            word for word in self.words if self.should_keep(word)
        ]

    def keep_probability(self, word):
        s = 0.001
        z = self.frequencies[word]
        return (math.sqrt(z / s) + 1) * (s / z)

    def should_keep(self, word):
        return random.random() < self.keep_probability(word)

    def encoded_words(self):
        for word in self.words:
            yield self.word2index[word]



if __name__ == '__main__':
    data_filepath = './data-plb/text8'
    preprocessed_filepath = './data-plb/text8-preprocessed.pickle'

    if os.path.isfile(preprocessed_filepath):
        with open(preprocessed_filepath, 'rb') as f:
            corpus = pickle.load(f)
    else:
        corpus = Corpus(data_filepath)
        corpus.eliminate_below_frequency(5)
        corpus.subsample()
        with open(preprocessed_filepath, 'wb') as f:
            pickle.dump(corpus, f)

    print(len(corpus.words))
