'''
generator.py

Generates sentences through predicting the next possible word in sentence based on the context 
of its preceding words. The next word selected is based on conditional frequency distributions 
of bigrams found in the text. 

Modified from Chris Moyer's <cmoyer@newstex.com>
'''

import nltk, random

TERMINAL_PUNCT = ['.', '!', '?', '\n\n']
SPLIT_PUNCT = [',', ';']
CLAUSE_TERMINALS = TERMINAL_PUNCT + SPLIT_PUNCT
STOPWORDS = nltk.corpus.stopwords.words('english')

class sentGenerator(object):

	def __init__(self, corpa, *args, **kwargs):
		if isinstance(corpa, str):
			words = nltk.word_tokenize(corpa)
			sents = nltk.sent_tokenize(corpa)
		bigrams = nltk.bigrams([w.lower() for w in words])
		self.cdf = nltk.ConditionalFreqDist(bigrams)
		self.flat_cdf = nltk.ConditionalFreqDist([(w.lower(), w) for w in words])
		self.avg_sent_len = int(len(words)/len(sents))

	# Generates phrases through bigram frequencies with constraints on word type, word length, or
	# punctuation.
	def __call__(self, word):	
		word = word.lower()							# Flatten word
		if ' ' in word:								# If there are multiple input words, set phrase  
			phrase = nltk.word_tokenize(word)		# 	to be the tokenized sentence
			word = phrase[-1]						# Then set word to be the last word in the phrase
		else:										# Else set phrase to only contain word
			phrase = [word]

		while word not in TERMINAL_PUNCT:			# Making sure the word isn't in any of the clause
			if phrase[-1] in SPLIT_PUNCT:			# terminating punctuation lists, set prev to be
				prev = phrase[-1]					# the last word of the phrase. Then, generate the
			else:									# next word from the most likely word after prev
				prev = phrase[-1]					# from the n-gram generated list
			for next in self.cdf[word]:
				if next == word:					# Don't accept duplicate words and symbols
					continue						# Don't allow the sent len be <.5 the avg length

				if not (next.isalpha() or next.isdigit()) and not next in CLAUSE_TERMINALS:
					continue
				
				if next in TERMINAL_PUNCT and len(phrase) < self.avg_sent_len/2:
					continue

				# We select a word with <4 chars after a preceding word of <4 chars only a small
				# amount of chance to avoid repetition common, short words. 
				if not next in phrase[int(-len(phrase)/2):]:
					prev_phrase = [prev, next]
					if not ' '.join(prev_phrase) in ' '.join(phrase):
						if not (len(next) < 4 and (len(prev) < 4) and not random.randint(0,6)):
							word = next

			if word == phrase[-1]:
				phrase.append('\n')
				break

			phrase.append(word)

		for index, word in enumerate(phrase[:]):
			freq = self.flat_cdf[word]
			if freq:
				phrase[index] = freq.max()
		phrase = ' '.join(phrase)

		phrase = phrase[0].upper() + phrase[1:]
		
		for symbol in CLAUSE_TERMINALS:
			phrase = phrase.replace(' %s' % symbol, symbol)
		return phrase 

	# Gets list of clause terminals
	def getTerminalPunct(self):
		return CLAUSE_TERMINALS

