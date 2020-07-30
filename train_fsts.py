from math import log

# Open needed files
train = open('dataset/NL2SparQL4NLU.train.conll.txt', 'r')
tags_lex = open('tags.lex.txt', 'w')
automa = open('a.txt', 'w')
tag_sent = open('tag_sent.txt', 'w')


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
tag_freq = {}
tag_tag_freq = {}

# Dictionary of word-tag counts
word_tag_count = {}

# Dictionary with probability of word given the tag
word_tag_prob = {}

# Dictionary with probability of tag given previous tag
tag_tag_prob = {}


# Fill counting dictionaries
for p in sents:
	for i, t in enumerate(p):

		# Count word frequencies, tag frequencies and word-tag frequencies
		key = (t[0], t[1])
		word_tag_count[key] = word_tag_count.get(key, 0) + 1
		word_freq[t[0]] = word_freq.get(t[0], 0) + 1
		tag_freq[t[1]] = tag_freq.get(t[1], 0) + 1

		# Count bigram tags
		if i > 0:
			bitags = (p[i-1][1], t[1])
			tag_tag_freq[bitags] = tag_tag_freq.get(bitags, 0) +1



# Number of tags
n_tags = len(tag_freq)



# Fill probabilities dictionaries
for val in sents:
	for i, t in enumerate(val):

		# Word given tag
		key = (t[0], t[1])
		if key not in word_tag_prob:
			word_tag_prob[key] = -log(float(word_tag_count[key])/float(tag_freq.get(t[1])))

		# Tag given previous tag
		if i > 0:
			bitags = (val[i-1][1], t[1])
			tag_tag_prob[bitags] = -log(float(tag_tag_freq[bitags])/float(tag_freq.get(val[i-1][1])))




#########################################
# Generate TAGs lexicon
#########################################
ids = 1

# Add epsilon
epsilon = '<eps>' + ' ' + '0' + '\n'
tags_lex.write(epsilon)

for key in tag_freq:
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
for key in word_tag_prob:
	string = '0\t' + '0\t' + key[0] + '\t' + key[1] + '\t' + str(word_tag_prob[key]) + '\n'
	automa.write(string)

# Add unk information and final state
for key in tag_freq:
	string = '0\t' + '0\t' + '<unk>' + '\t' + key + '\t' + str(1/n_tags) + '\n'
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
