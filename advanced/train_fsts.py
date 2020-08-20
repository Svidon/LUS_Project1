from math import log

# Open needed files
train = open('../dataset/NL2SparQL4NLU.train.conll.txt', 'r')
train_features = open('../dataset/NL2SparQL4NLU.train.features.conll.txt', 'r')
test_utt = open('../dataset/NL2SparQL4NLU.test.features.conll.txt', 'r')
test_gen = open('test_generalized.txt', 'w')
tags_lex = open('wordtags.lex.txt', 'w')
automa = open('a.txt', 'w')
tag_sent = open('wordtag_sent.txt', 'w')
word_lex = open('word.txt', 'w')

# Control variables (to allow cutoff and lemmas usage)
LEMMAS = True
POS = False
CUTOFF = False
CUTOFF_VAL = 4 # Min number of occurences to include

# This is the string used for numbers generalization
num = '<number>'


###############################
# Reading of train file
# Together with features file
###############################

# Sentences of corpus
sents = []
tmp = []

# List of original tags. This will be used for '<unk>' words. It will include POS tags
original_tags = []

# Identify all sentences with tuples of word-wordtag
for t_line, f_line in zip(train, train_features):
	a = list(t_line.split()) # Words Tags
	f = list(f_line.split()) # Words POS-Tags Lemma

	if len(a) > 0:
		# Check if we have to use POS tags as additional features
		if POS:
			a[1] = '+'.join([a[1], f[1]])
		original_tags.append(a[1])
		
		# Check if words have to be mapped onto their lemmas
		if LEMMAS:
			a[0] = f[2]
		
		# Generalize all numbers with a unique token	
		if a[0].isdigit():	
			a[0] = num
			
		a[1] = '+'.join(a)
		tmp.append(tuple(a))
	else:
		sents.append(tmp)
		tmp = []

# Original tags as set
original_tags = set(original_tags)


#######################
# Lexicon with cutoff
#######################
# Dictionary of word counts
word_freq = {}

for p in sents:
	for i, t in enumerate(p):
		word_freq[t[0]] = word_freq.get(t[0], 0) + 1

# By default lex can be considered the set of keys of word freq. For praticity we set it to word_freq
lex = list(word_freq.keys())
# Apply cutoff if required
if CUTOFF:
	lex = []
	lex.extend(sorted([word for word, freq in word_freq.items() if freq >= CUTOFF_VAL]))

# Generate the file on which to compute the lexicon with ngramsymbols
for val in lex:
	string = val + '\n'
	word_lex.write(string)
	

###############################################
# Filling of dictionaries
# Kept because of code ease wrt previous model
###############################################
# Dictionary of wordtag frequencies
wordtag_freq = {}

# Dictionary of word-wordtag counts
word_wordtag_count = {}

# Fill counting dictionaries
for p in sents:
	for i, t in enumerate(p):

		# Word count already computed
		# This control is just to avoid doing the nested control every time if there is no cutoff
		if CUTOFF:
			# Lex contains the lexicon with cutoff
			if t[0] in lex:
				key = (t[0], t[1])
				word_wordtag_count[key] = word_wordtag_count.get(key, 0) + 1
				wordtag_freq[t[1]] = wordtag_freq.get(t[1], 0) + 1
		else:
			key = (t[0], t[1])
			word_wordtag_count[key] = word_wordtag_count.get(key, 0) + 1
			wordtag_freq[t[1]] = wordtag_freq.get(t[1], 0) + 1


#########################################
# Generate TAGs lexicon
#########################################
ids = 1

# Add epsilon
epsilon = '<eps>' + ' ' + '0' + '\n'
tags_lex.write(epsilon)

for key in wordtag_freq:
	tagtmp = key + ' ' + str(ids) + '\n'
	tags_lex.write(tagtmp)
	ids += 1
	
# Add tags for unk words
for el in original_tags:
	tagtmp = '<unk>+' + el + ' ' + str(ids) + '\n'
	tags_lex.write(tagtmp)
	ids += 1

# Add final unk
unk_add = '<unk>' + ' ' + str(ids) + '\n'
tags_lex.write(unk_add)


###################################################################################
# Generation of train FST for the tool
# Unweighted since all the probabilities would be 1 for words and equal among unks
###################################################################################

# Generate FSTs
for key in word_wordtag_count:
	string = '0\t' + '0\t' + key[0] + '\t' + key[1] + '\n'
	automa.write(string)

# Add unk information and final state
unk_prob = str(-log(1/float(len(wordtag_freq))))
for key in wordtag_freq:
	string = '0\t' + '0\t' + '<unk>' + '\t' + key + '\n'
	automa.write(string)
automa.write('0')


###############################################
# Generation of file for n-gram language model
###############################################

# Generate list of all sentences with just the tags
# All the correct tags are used, even for cutoff words, it provides more training information
tag_sentencies = []

for p in sents:
	tmp = []

	for el in p:
		tmp.append(el[1])

	tag_sentencies.append(tmp)

# Write out tag sentencies
for el in tag_sentencies:
	string = ''
	for tag in el:
		string += tag + ' '

	string += '\n'
	tag_sent.write(string)
tag_sent.close()


###################################
# Generalization of the test input
###################################
# Read test set
test_sents = []
tmp = []

for line in test_utt:
	a = list(line.split()) # Word pos lemma
	
	if len(a) > 0:
		# If we are using lemmas use those, otherwise normal word
		if LEMMAS:
			word = a[2]
		else:
			word = a[0]
		
		if a[0].isdigit():
			tmp.append(num)
		else:
			tmp.append(word)
	else:
		test_sents.append(tmp)
		tmp = []
			
# Output in a new file with the same structure of utterances file
for sent in test_sents:
	string = ' '.join(sent) + '\n'
	test_gen.write(string)	
