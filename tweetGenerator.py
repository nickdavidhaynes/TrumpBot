import markov
import random
from nltk.tokenize import sent_tokenize

def make_tweet(size=25, update=False):
	'''
	Take generated text, turn it into something that fits into a tweet
	'''
	file = open('trump_raw.txt')
	generator = markov.markov_generator(file)
	if update == True:
		generator.update_dicts()

	# if text is too long, remove sentences one by one until it fits in a tweet
	tweetable = False
	while not tweetable:
		gen_text = generator.generate_text(size=50)
		# remove the first sentence (it is usually a fragment)
		sentences = sent_tokenize(gen_text)
		gen_text = ' '.join(sentences[1:-1])
		if len(gen_text) < 120:
			tweet = gen_text
			tweetable = True
		else:
			sentences = sent_tokenize(gen_text)
			n_sentences = len(sentences) - 1
			while n_sentences > 0:
				gen_text = ' '.join(sentences[0:n_sentences])
				if len(gen_text) < 120:
					tweet = gen_text
					tweetable = True
					break
				n_sentences -= 1

	# Add a hashtag
	if random.random() > .5:
		tweet+=" #MakeAmericaGreatAgain"
	else:
		tweet+=" #Trump2016"
	print "----------------------------------"
	print "Tweet length: "+str(len(tweet))+" characters"
	print tweet
	return tweet
