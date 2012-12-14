from parsapp.models import Word
import subprocess


def lookup(word):
	'''Look up for <word> in dictionary WordNet'''
	p = subprocess.Popen(['wordnet',word, '-over'], stdout=subprocess.PIPE)
	description = p.communicate()
	return description[0]


def populate():
	'''Populate Word model with words and definitios from predefined list'''
	wordlist = ['parse', 'startup', 'hacker']
	for word in wordlist:
		description = lookup(word)
		Word.objects.create(name=word, description=description)
