import zipfile, argparse, os, nltk, operator, re, sys, random
from collections import defaultdict
from nltk.text import ContextIndex
from generator import sentGenerator
from reportlab.pdfgen import canvas

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('i')
parser.add_argument('o')
args = parser.parse_args()


# Creates subclass of ContextIndex modifying nonfunctioning methods.
# ContextModule takes one argument: word_tokens (i.e. the tokenized text)
class ContextModule(ContextIndex):

    # There is an error in the source code for the ContextIndex.similar_words function.
    def similar_words(self, text, word, n=20):
        scores = defaultdict(int)
        for c in self._word_to_contexts[self._key(word)]:
            for w in self._context_to_words[c]:
                if w != word:
                    scores[w] += self._context_to_words[c][word] * self._context_to_words[c][w]
        return sorted(scores, key=scores.get, reverse=True)[::-1][:int(n)]   

# # Gets screenplays and opens and processes the data into a dataset_dict. 
# # Assumption: DAVE.py is in the same directory as the screenplays.
# def getData(file_extension):
#   dataset_dict = {}
#   # Find screenplays
#   for filename in os.listdir('.'):
#         if filename.endswith(file_extension):
#             dataset_dict[filename[0:len(filename)-len(file_extension)]] \
#               = open(filename, 'rU', encoding='utf-8').read()
#   return dataset_dict

# Normalize data by flattening text and removing stopwords. Preserve the
# original text for final result.
def normalize(text):
    words = nltk.word_tokenize(text)
    nrml = [word.lower() for word in words]
    stop = nltk.corpus.stopwords.words('english')
    wc = r'([^\w]+)'
    nonwc_set = [] 
    for word in nrml: nonwc_set.extend(re.findall(wc, word))
    nonwc_set= set(nonwc_set)
    for word in nrml:
        if word in stop or word in nonwc_set: 
            while word in nrml: nrml.remove(word)
    return nrml

# Find similar context words.
# Note: Use untokenized text.
def findSimilar(text, word):
    context = ContextModule(text)
    similarWords = context.similar_words(text, word)
    print (commonContexts)
    print (similarWords)
    return similar


# Find common contexts between words or the contexts a word is used.
# Note: Use untokenized text and a list of words or a single string.
def findContext(text, words):
    contexts = text.common_contexts(words)
    return contexts

if __name__ == '__main__':

    base_text = open(args.i, 'rU', encoding='utf-8').read()
    base_sents = nltk.sent_tokenize(base_text)
    gen = sentGenerator(base_text)
    output = open(args.o, 'w', encoding="utf-8")

    c = canvas.Canvas(args.o)
    c.setFont('Courier', 16)
    c.drawCentredString(297.635,420.945,"Movie Title") 
    c.drawCentredString(297.635,375.945,"Written by: D.A.V.E")
    c.showPage()
    c.setFont('Courier', 12)
    x=810

    for i in range(0,30):
        j = random.randint(0, len(base_sents))
        words = nltk.word_tokenize(base_sents[j])
        next = words[0]
        sentence = gen(next)
        #output.write(sentence)
        while(True):
            if(x==10):
                c.showPage()
                c.setFont('Courier', 12)
                x=810
            if len(sentence) > 75:
                first = sentence[:75]
                second = sentence[-(len(sentence)-75):]
                c.drawString(30,x,first)
                x=x-25
                sentence = second

            else:
                c.drawString(30,x,sentence)
                x=x-25
                break

    c.save()
