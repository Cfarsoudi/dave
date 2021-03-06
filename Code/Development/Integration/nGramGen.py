"""
nGramGen.py

Generates dictionary containing (2<k<=n)-gram distributions for all action 
and dialogue files in the current directory.
"""

import nltk, os, time, itertools, pickle
from collections import defaultdict, Counter

def makeNgrams(filename, words, n):
    """
    Generate n-grams from corpus
    Returns a dictionary of k-grams (from 2 to nth degree)
    """
    start_time = time.time()
    ngrams = dict()
    itergrams = dict()

    for k in range(2,n+1):
        itergrams[k] = list(nltk.ngrams(words, k))

    for k, grams in itergrams.items():
        kgrams = defaultdict(Counter)
        for gram in grams:                
            kgram = list(gram)
            key = ' '.join(kgram[:k-1])
            kgrams[key].update({kgram[-1]})
        ngrams[k] = kgrams
        print ('finish gen ', k, 'grams at ', time.time()-start_time)
    pickle.dump(ngrams, open(filename, 'wb'))

if __name__ == '__main__':

    dataset_dict = {}

    # iterate through all the files in the current directory
    for filename in os.listdir("."):
        if filename.endswith('.Actions') or filename.endswith('.Dialogue'):
            dataset_dict[filename] = open(filename, 'rU', encoding='utf-8').read()

    for filename, infile in dataset_dict.items():
        filename = filename + ".pickle"
        words = nltk.word_tokenize(infile)
        ngrams = makeNgrams(filename, words, 5)
        


