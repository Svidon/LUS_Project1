from math import log

# Open needed files
train = open('../dataset/NL2SparQL4NLU.train.conll.txt', 'r')
tags_lex = open('wordtags.lex.txt', 'w')
automa = open('a.txt', 'w')
tag_sent = open('wordtag_sent.txt', 'w')
word_lex = open('word.txt', 'w')

# Control variables (to allow cutoff and lemmas usage)
LEMMAS = False
CUTOFF = False
CUTOFF_VAL = 3


########################
# Reading of train file
########################

# Sentences of corpus
sents = []
tmp = []

# Identify all sentences with tuples of word-tag
for line in train:
	a = list(line.split())

	if len(a) > 0:
		a[1] = '+'.join(a)
		tmp.append(tuple(a))
	else:
		sents.append(tmp)
		tmp = []


#####################################
# Filling of dictionaries
# both frequencies and probabilities
#####################################

# Dictionary of words frequencies and tag frequencies
word_freq = {}
wordtag_freq = {}

# Dictionary of word-tag counts
word_wordtag_count = {}

# Dictionary with probability of word given the tag
word_wordtag_prob = {}


# Fill counting dictionaries
for p in sents:
	for i, t in enumerate(p):

		# Count word frequencies, tag frequencies and word-tag frequencies
		key = (t[0], t[1])
		word_wordtag_count[key] = word_wordtag_count.get(key, 0) + 1
		word_freq[t[0]] = word_freq.get(t[0], 0) + 1
		wordtag_freq[t[1]] = wordtag_freq.get(t[1], 0) + 1

# Number of tags
n_tags = len(wordtag_freq)

# Fill probabilities dictionaries
for val in sents:
	for i, t in enumerate(val):

		# Word given tag
		key = (t[0], t[1])
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

# Add unk
unk_add = '<unk>' + ' ' + str(ids) + '\n'
tags_lex.write(unk_add)


########################################
# Generation of train FST for the tool
########################################

# Generate FSTs
for key in word_wordtag_prob:
	string = '0\t' + '0\t' + key[0] + '\t' + key[1] + '\t' + str(word_wordtag_prob[key]) + '\n'
	automa.write(string)

# Add unk information and final state
for key in wordtag_freq:
	string = '0\t' + '0\t' + '<unk>' + '\t' + key + '\t' + str(-log(1/float(n_tags))) + '\n'
	automa.write(string)
automa.write('0')


###############################################
# Generation of file for n-gram language model
###############################################

# Generate list of all sentences with just the tags
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
