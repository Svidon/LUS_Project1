from math import log

# Open needed files
train = open('../dataset/NL2SparQL4NLU.train.conll.txt', 'r')
train_features = open('../dataset/NL2SparQL4NLU.train.features.conll.txt', 'r')
tags_lex = open('wordtags.lex.txt', 'w')
automa = open('a.txt', 'w')
tag_sent = open('wordtag_sent.txt', 'w')
word_lex = open('word.txt', 'w')

# Control variables (to allow cutoff and lemmas usage)
LEMMAS = False
POS = True
CUTOFF = False
CUTOFF_VAL = 3



###############################
# Reading of train file
# Together with features file
###############################

# Sentences of corpus
sents = []
tmp = []

# List of original tags (this will include)
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
	

#####################################
# Filling of dictionaries
# both frequencies and probabilities
#####################################
# Dictionary of wordtag frequencies
wordtag_freq = {}

# Dictionary of word-wordtag counts
word_wordtag_count = {}

# Dictionary with probability of word given the wordtag
word_wordtag_prob = {}


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

# Number of tags
n_tags = len(wordtag_freq)

# Fill probabilities dictionaries
for val in sents:
	for i, t in enumerate(val):

		# Word given wordtag
		key = (t[0], t[1])
		# Same control as before, to avoid controlling without cutoff
		if CUTOFF:
			if t[0] in lex:
				if key not in word_wordtag_prob:
					word_wordtag_prob[key] = -log(float(word_wordtag_count[key])/float(wordtag_freq.get(t[1])))
		else:
			if key not in word_wordtag_prob:
				word_wordtag_prob[key] = -log(float(word_wordtag_count[key])/float(wordtag_freq.get(t[1])))


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

# Add unks #TODO check if this is how it is handled
unk_add = '<unk>' + ' ' + str(ids) + '\n'
tags_lex.write(unk_add)


########################################
# Generation of train FST for the tool
########################################

# Generate FSTs
for key in word_wordtag_prob:
	string = '0\t' + '0\t' + key[0] + '\t' + key[1] + '\t' + str(word_wordtag_prob[key]) + '\n'
	automa.write(string)

# Add unk information and final state #TODO check how this is handled -> '+'.join(['<unk>', key])
unk_prob = str(-log(1/float(len(wordtag_freq))))
for key in wordtag_freq:
	string = '0\t' + '0\t' + '<unk>' + '\t' + key + '\t' + unk_prob + '\n'
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
