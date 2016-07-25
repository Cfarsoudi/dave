''' 
generator.py

Generates sentences through predicting the next possible word in sentence
based on the context of its preceding words. The next word selected is based
on conditional frequency distributions of n-grams found in the text, with 
(1<k<n) fallback k-grams.
'''

import nltk, random, itertools, bisect
from collections import defaultdict, Counter
# from numpy import random as npr

TERMINAL_PUNCT = ['.', '!', '?', '\n\n']
SPLIT_PUNCT = [',', ';']
CLAUSE_TERMINALS = TERMINAL_PUNCT + SPLIT_PUNCT
STOPWORDS = nltk.corpus.stopwords.words('english')

class sentGenerator(object):

    def __init__(self, corpa, *args, **kwargs):
        if isinstance(corpa, str):
            self.words = nltk.word_tokenize(corpa)
            self.sents = nltk.sent_tokenize(corpa)
            self.starts = []
            self.ends = []
            self.pause = []
            self.resume = []
            for sent in self.sents:
                sent = nltk.word_tokenize(sent)
                self.starts.append(sent[0])
                self.ends.append(sent[-1])
                for punct in SPLIT_PUNCT:
                    split = ' '.join(sent).split(punct)
                    if len(split) > 1:
                        for clause in split:
                            clause = clause.split()
                            self.pause.append(clause[-1])
                            self.resume.append(clause[0])

    
    def __call__(self, word=None):    
        n = 15 
        self.ngrams = self.__makeNgrams(n)

        def gen(seed=None):
            if not seed:
                seed = random.choice(self.starts)            
            return self.__markovGen(self.ngrams, n, 1000, seed)

        return gen()

    def __makeNgrams(self, n):
        """
        Generate n-grams from corpus
        Returns a dictionary of k-grams (from 2 to nth degree)
        """
        cfds = []
        ngrams = dict()
        itergrams = dict()

        for k in range(2,n+1):
            itergrams[k] = list(nltk.ngrams(self.words, k))

        for k, grams in itergrams.items():
            kgrams = defaultdict(Counter)
            for gram in grams:                
                kgram = list(gram)
                key = ' '.join(kgram[:k-1])
                kgrams[key].update({kgram[-1]})
            ngrams[k] = kgrams
        return ngrams

    # Generates sentences using a n degree Markov model
    def __markovGen(self, ngrams, n, length, start):
        """
        Param:
            ngrams : dict
                Dictionary of n-grams
                Each key is a word in the corpus
                Each value are possible n-grams with the starting word

            length : int
                Sentence length

            start : string
                Starting word for the generated sentence
                Randomly chosen if not specified
        """
        sent = [start]
        prev = start
        for i in range(length):
            k = len(sent)+1 if len(sent)+1 < n else n
            while not ngrams[k][prev] and k > 2:
                k -= 1
            prev = ' '.join(sent[-k+1:])

            if prev in SPLIT_PUNCT:
                weightedChoices = [(candidate, weight) for (candidate, weight) \
                                    in ngrams[k][prev].most_common(10)
                                    if candidate in self.resume]
            else:
                weightedChoices = [(candidate, weight) for (candidate, weight) \
                                   in ngrams[k][prev].most_common(10)]
            
            # Choose next candidate word based on a cumulative weight distribution
            choices, weights = zip(*weightedChoices)
            cumdist = list(itertools.accumulate(weights))
            choice = random.random() * cumdist[-1]
            next = choices[bisect.bisect(cumdist, choice)]
            sent.append(next)
            
        ret = ' '.join(sent)
        cleanPunct = CLAUSE_TERMINALS + ['\'','n\'t',':',')']
        for punct in cleanPunct:
            ret = ret.replace(' %s' % punct, punct)
        ret = ret.replace('%s ' % '(', '(')
        return ret

    # Gets list of clause terminals
    def getTerminalPunct(self):
        return CLAUSE_TERMINALS



