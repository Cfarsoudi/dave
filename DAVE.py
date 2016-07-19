import zipfile, argparse, os, nltk, operator, re, sys, random
from collections import defaultdict
from nltk.text import ContextIndex
from nltk.parse.stanford import StanfordParser
from generator import sentGenerator

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('i')
parser.add_argument('o')
args = parser.parse_args()

if __name__ == '__main__':

    base_text = open(args.i, 'rU', encoding='utf-8').read()
    base_sents = nltk.sent_tokenize(base_text)
    gen = sentGenerator(base_text)
    output = open(args.o, 'w', encoding="utf-8")
    text = gen()
    output.write(text)

    # text = nltk.Text(base_text)
    # text.generate()



