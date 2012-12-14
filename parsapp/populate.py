from parsapp.models import Word
import subprocess


def populate():
	wordlist = ['parse', 'startup', 'hacker']
	for word in wordlist:
		p = subprocess.Popen(['wordnet',word, '-over'], stdout=subprocess.PIPE)
		out = p.communicate()
		Word.objects.create(name=word, description=out[0])

	# output = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]