from parsapp.models import Word
import os, re 
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "static/top_words.csv")
f_dict = open(file_path) # Add

# Load english dictionary of top 1000 used words
count=0
english_dict = []
for l in f_dict:
	l=l.translate(None, "\"")
	l=l.rsplit(',')
	# print l
	english_dict.append(l[1])

def select_words(msg, request):
	msg_good=[]
	
	msg = msg.lower() # convert to lower case
	# msg = strip_non_ascii(msg) #remove not ascii characters
	msg = re.sub('[.,?!%\n()]','',msg)  # remove punctuation signs
	msg = msg.rsplit(' ') # split words
	
	# Obtain all the words the user already know
	wordcontext = request.user.wordcontext_set.all()
	word_list=[]
	for wc in wordcontext:
		word_list.append(wc.word.name)

	for word in msg:
		if word not in word_list:
			if word not in english_dict:
				msg_good.append(word)
	return(msg_good)