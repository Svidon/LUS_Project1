from math import log

# Open needed files
train = open('dataset/NL2SparQL4NLU.train.conll.txt', 'r')
test = open('dataset/NL2SparQL4NLU.test.conll.txt', 'r')
w_out = open('I.lex.txt', 'w')
t_out = open('O.lex.txt', 'w')
tags_lex = open('tags.lex.txt', 'w')
automa = open('a.txt', 'w')
automa_test = open('a_test.txt', 'w')
unk = open('unk.txt', 'w')
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



#######################
# Reading of test file
#######################

# Sentences of corpus
sents_test = []
tmp_test = []

# Identify all sentences with tuples of word-tag
for line in test:
	a = list(line.split())

	if len(a) > 0:
		tmp_test.append(tuple(a))
	else:
		sents_test.append(tmp_test)
		tmp_test = []



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

# Dictionary with probability of word given the tag
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




##########################
# Other lexicon files
##########################
ids = 1

# Add epsilon
epsilon = '<eps>' + ' ' + '0' + '\n'
t_out.write(epsilon)
w_out.write(epsilon)


for w_key, t_key in zip(word_freq, tag_freq):
	ttmp = t_key + ' ' + str(ids) + '\n'
	t_out.write(ttmp)

	wtmp = w_key + ' ' + str(ids) + '\n'
	w_out.write(wtmp)

	ids += 1

unk_add = '<unk>' + ' ' + str(ids) + '\n'
w_out.write(unk_add)


# Tags' lexicon
ids = 1

# Add epsilon
tags_lex.write(epsilon)

for key in tag_freq:
	tagtmp = key + ' ' + str(ids) + '\n'
	tags_lex.write(tagtmp)
	ids += 1

tags_lex.write(unk_add)


########################################
# Generation of train FSTs for the tool
########################################

# Generate FSTs
for key in word_tag_prob:
	string = '0\t' + '0\t' + key[0] + '\t' + key[1] + '\t' + str(word_tag_prob[key]) + '\n'
	automa.write(string)
automa.write('0')

# FST for unknown words
for key in tag_freq:
	string = '0\t' + '0\t' + '<unk>' + '\t' + key + '\t' + str(1/n_tags) + '\n'
	unk.write(string)
unk.write('0')



######################################
# Generation of test FST for the tool
######################################

# Generate FSTs, handling unknown words
count = 0

for sent in sents_test:
	st = count
	
	for word in sent:
		if word in word_freq:
			string = str(count) + '\t' + str(count+1) + '\t' + word + '\t' + word + '\n'
			automa_test.write(string)
			count += 1
		else:
			string = str(count) + '\t' + str(count+1) + '\t' + '<unk>' + '\t' + '<unk>' + '\n'
			automa_test.write(string)
			count += 1

	automa_test.write(str(st))



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