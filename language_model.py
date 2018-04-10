# Read file's data
f = open('data/NLSPARQL.train.data', 'r')

# Sentences of corpus
sents = []
tmp = []

# Identify all sentences with tuples of word-tag
for line in f:
	a = list(line.split())

	if len(a) > 0:
		tmp.append(tuple(a))
	else:
		sents.append(tmp)
		tmp = []


# Dictionary of words frequencies
word_freq = {}

# Dictionary of word-tag counts
word_tag_count = {}

# Dictionary with probability that the word has that tag
word_tag_prob = {}

# Fill counting dictionaries
for p in sents:
	for t in p:
		key = t[0] + ' ' + t[1]
		word_tag_count[key] = word_tag_count.get(key, 0) + 1
		word_freq[t[0]] = word_freq.get(t[0], 0) + 1

# Fill probabilities dictionary
for p in sents:
	for t in p:
		key = t[0] + ' ' + t[1]
		if key not in word_tag_prob:
			word_tag_prob[key] = word_tag_count[key]/word_freq[t[0]]

print(word_tag_prob)