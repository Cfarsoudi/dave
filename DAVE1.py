''' 
DAVE.py

Generates screenplay using Markov models of a genre-separated 
screenplay corpus.
'''

import argparse, nltk, random, pickle
from collections import defaultdict
from HAL import sentGenerator as gen
from reportlab.pdfgen import canvas # needed for PDF output
from Stanley import director

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('i')
parser.add_argument('o')
args = parser.parse_args()

if __name__ == '__main__':


    genre = args.i
    # iterate through all the files in the genre's directory
    scriptFormat = {}
    filenames = [('headings', genre + '.Headings'),
                 ('characters', genre + '.Characters'),
                 ('parentheticals', genre + '.Parentheticals'),
                 ('transitions', genre + '.Transitions'),
                 ('actions', genre + '.Actions.pickle'),
                 ('dialogue', genre + '.Dialogue.pickle')]

    for (var, filename) in filenames:
        if filename.endswith('.pickle'):
            loadfile = pickle.load(open(filename, 'rb'))
        else:
            loadfile = open(filename, 'rU', encoding='utf-8').readlines()
            for line in range(len(loadfile)):
                loadfile[line] = loadfile[line].strip()
        scriptFormat[var] = loadfile

    headings = scriptFormat['headings']
    characters = scriptFormat['characters']
    parentheticals = scriptFormat['parentheticals']
    transitions = scriptFormat['transitions']
    actions = scriptFormat['actions']
    dialogue = scriptFormat['dialogue']

    actGen = gen(actions)
    diaGen = gen(dialogue)
    output = open(args.o, 'w', encoding="utf-8")
    stan = director(headings, characters, parentheticals, transitions,
                    actGen, diaGen, output)
    stan()
