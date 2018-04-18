# Open needed files
f = open('data/NLSPARQL.train.data', 'r')
w_out = open('I.lex.txt', 'w')
t_out = open('O.lex.txt', 'w')
automa = open('a.txt', 'w')

# Sentences of corpus
sents = []
tmp = [tuple(['<s>', 'O'])]

# Identify all sentences with tuples of word-tag
for line in f:
	a = list(line.split())

	if len(a) > 0:
		tmp.append(tuple(a))
	else:
		sents.append(tmp)
		tmp = [tuple(['<s>', 'O'])]


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

		# Usual counting dicts
		key = t[0] + ' ' + t[1]
		word_tag_count[key] = word_tag_count.get(key, 0) + 1
		word_freq[t[0]] = word_freq.get(t[0], 0) + 1
		tag_freq[t[1]] = tag_freq.get(t[1], 0) + 1

		# Count bigram tags
		if i > 0:
			bitags = p[i-1][1] + ' ' + t[1]
			tag_tag_freq[bitags] = tag_tag_freq.get(bitags, 0) +1
		

# Fill probabilities dictionaries
for val in sents:
	for i, t in enumerate(val):

		# Word given tag
		key = t[0] + ' ' + t[1]
		if key not in word_tag_prob:
			word_tag_prob[key] = word_tag_count[key]/tag_freq[t[1]]

		# Tag given previous tag
		if i > 0:
			bitags = val[i-1][1] + ' ' + t[1]
			tag_tag_prob[bitags] = tag_tag_freq[bitags]/tag_freq[val[i-1][1]]



# Create vocabulary files
ids = 1

# Add epsilon
ttmp = '<eps>' + ' ' + '0' + '\n'
t_out.write(ttmp)

wtmp = '<eps>' + ' ' + '0' + '\n'
w_out.write(wtmp)


for w_key, t_key in zip(word_freq, tag_freq):
	ttmp = t_key + ' ' + str(ids) + '\n'
	t_out.write(ttmp)

	wtmp = w_key + ' ' + str(ids) + '\n'
	w_out.write(wtmp)

	ids += 1

unk = '<unk>' + ' ' + str(ids) + '\n'
w_out.write(unk)