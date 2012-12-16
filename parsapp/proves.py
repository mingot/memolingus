
f_coca = open("/home/mingot/Projectes/django/memolingus/parsapp/static/5k_coca.csv", "r")


# Load 5k freq from coca (Corpus of Contemporany American English)
count=0
english_dict = []
for l in f_coca:
	l=l.rsplit('\t')
	if len(l)>1: english_dict.append(l[1])
	count +=1 
	print l
	if count ==11: break
print english_dict