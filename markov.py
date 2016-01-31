'''
module for building, updating, and calling the encyclopedia
'''
import pickle
import random

def create_doubles_dict(words):
	'''
	create (or update an existing) dictionary of word doubles
	'''
	# from list of words, create a list of doubles
	doubles_list = []
	for i in range(len(words)-1):
		doubles_list.append([words[i], words[i+1]])

	# from list of doubles, create a dictionary of word1:word2 pairs
	doubles_dict = {}
	for double in doubles_list:
		key = double[0]
		val = double[1]
		if key in doubles_dict:
			doubles_dict[key].append(val)
		else:
			doubles_dict[key] = [val]

	pickle.dump(doubles_dict, open('doubles_dict.pickle','w'))
	return doubles_dict

def create_triples_dict(words):
	'''
	create (or update an existing) dictionary of word doubles
	'''
	# from list of words, create a list of triples
	triples_list = []
	for i in range(len(words)-2):
		triples_list.append([words[i], words[i+1], words[i+2]])

	# from list of triples, create a dictionary of (word1,word2):word3 pairs
	triples_dict = {}
	for triple in triples_list:
		key = (triple[0], triple[1])
		val = triple[2]
		if key in triples_dict:
			triples_dict[key].append(val)
		else:
			triples_dict[key] = [val]

	pickle.dump(triples_dict, open('triples_dict.pickle','w'))
	return triples_dict

class markov_generator(object):

	def __init__(self, text_file, update=False):
		self.text = text_file.read()
		self.words = self.create_words_list()
		try:
			self.doubles_dict = pickle.load(open('doubles_dict.pickle','r'))
		except IOError:
			self.doubles_dict = create_doubles_dict(self.words)
			pickle.dump(self.doubles_dict, open('doubles_dict.pickle','w'))
			print 'No doubles dictionary was found, so one was created.'
		try:
			self.triples_dict = pickle.load(open('triples_dict.pickle','r'))
		except IOError:
			self.triples_dict = create_triples_dict(self.words)
			pickle.dump(self.triples_dict, open('triples_dict.pickle','w'))
			print 'No triples dictionary was found, so one was created.'

	def update_dicts(self):
		self.doubles_dict = create_doubles_dict(self.words)
		pickle.dump(self.doubles_dict, open('doubles_dict.pickle','w'))
		self.triples_dict = create_triples_dict(self.words)
		pickle.dump(self.triples_dict, open('triples_dict.pickle','w'))

	def create_words_list(self):
		tmp_words = self.text.decode('utf-8').split()
		new_words = []
		for word in tmp_words:
			if word == '.' or word == ' ' or word == ' .' or word == "" or word == '. ':
				continue
			new_words.append(word)
		return new_words

	def generate_doubles(self, size=25):
		seed = random.randint(0, len(self.words)-2)
		word1 = self.words[seed]
		gen_words = []
		for i in range(size):
			gen_words.append(word1)
			word1 = random.choice(self.doubles_dict[(word1)])
		gen_words.append(word1)
		return ' '.join(gen_words)

	def generate_triples(self, size=25):
		seed = random.randint(0, len(self.words)-3)
		word1, word2 = self.words[seed], self.words[seed+1]
		gen_words = []
		for i in range(size):
			gen_words.append(word1)
			word1, word2 = word2, random.choice(self.triples_dict[(word1, word2)])
		gen_words.append(word2)
		return ' '.join(gen_words)

	def generate_text(self, size=25, p=.2):
		seed = random.randint(0, len(self.words)-3)
		word1, word2 = self.words[seed], self.words[seed+1]
		gen_words = []
		for i in range(size):
			gen_words.append(word1)
			try:
				triple_len = len(self.triples_dict[(word1, word2)])
			except KeyError:
				triple_len = 0
			if random.random() < p or triple_len < 1:
				word1 = word2
				word2 = random.choice(self.doubles_dict[word1])
			else:
				word1, word2 = word2, random.choice(self.triples_dict[(word1, word2)])
		gen_words.append(word2)
		return ' '.join(gen_words)
