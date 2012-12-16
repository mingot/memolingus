from parsapp.models import Word
import os, re 
# module_dir = os.path.dirname(__file__)
# path_gutenberg = os.path.join(module_dir, "static/1k_gutenberg.csv")
# path_coca = os.path.join(os.getcwd(), "parsapp/static/5k_coca.csv")

f_gutenberg = open("/home/mingot/Projectes/django/memolingus/parsapp/static/1k_gutenberg.csv", "r") 
f_coca = open("/home/mingot/Projectes/django/memolingus/parsapp/static/5k_coca.csv", "r")


# Load 1k freq from gutenberg
english_dict = []
for l in f_gutenberg:
	l=l.translate(None, "\"")
	l=l.rsplit(',')
	english_dict.append(l[1])

# Add Load 5k freq from coca (Corpus of Contemporany American English)
for l in f_coca:
	l=l.rsplit('\t')
	if len(l)>1: english_dict.append(l[1])

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def select_words(msg, request):
	
	msg = strip_non_ascii(msg) #remove not ascii characters
	msg = re.sub(r'[.,?!%\n()]','',msg)  # remove punctuation signs and numbers
	msg = re.sub(r'\'*','',msg)
	msg = re.split(' |\n',msg) # split text by whitespace and newlines
	msg2=list(msg)
	for word in msg2:
		if re.search('[0-9]', word): msg.remove(word) # Remove words containing numbers
		elif re.search('[A-Z]', word): msg.remove(word) # Remove words containing capital letters
		elif re.search('\'', word): word = re.sub('\'.+','',word) # Remove the contractions from apostrophes: you're -> you
	
	# Obtain all the words the user already know
	wordcontext = request.user.wordcontext_set.all()
	word_list=[]
	for wc in wordcontext:
		word_list.append(wc.word.name)

	msg_good=[]
	for word in msg:
		if word not in word_list:
			if word not in english_dict:
				msg_good.append(word)
	return(msg_good)

# The hacker made the startup! Parse it! Does Google really know how to fight against Samsung? It's just for 20$??