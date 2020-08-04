import numpy as np

# Read main files
train = open('../dataset/NL2SparQL4NLU.train.conll.txt', 'r')
test = open('../dataset/NL2SparQL4NLU.test.conll.txt', 'r')
train_csv = open('train_tags.csv', 'w')
test_csv = open('test_tags.csv', 'w')

########################
# Reading of train file
########################

# Sentences of corpus
train_sents = []
tmp = []

# Identify all sentences with tuples of word-tag
for line in train:
	a = list(line.split())

	if len(a) > 0:
		tmp.append(tuple(a))
	else:
		train_sents.append(tmp)
		tmp = []
			
########################
# Reading of test file
########################

# Sentences of corpus
test_sents = []
tmp = []

# Identify all sentences with tuples of word-tag
for line in test:
	a = list(line.split())

	if len(a) > 0:
		tmp.append(tuple(a))
	else:
		test_sents.append(tmp)
		tmp = []
		
		
######################################
# Basic information about the dataset
######################################

print("SENTENCES ANALYSIS\n")

# Number of sentences and their average length in training set
print("Number of training set sentences: ", len(train_sents))
print("Average length of training sentences: {}\n".format(np.mean([len(s) for s in train_sents])))

# Number of sentences and their average length in test set
print("Number of test set sentences: ", len(test_sents))
print("Average length of test sentences: {}\n\n".format(np.mean([len(s) for s in test_sents])))


################################
# Concepts and OOV distribution
################################

print("CONCEPTS DISTRIBUTIONS\n")

# Count train concepts
train_concepts_counts = {}
total = 0

for p in train_sents:
	for i, t in enumerate(p):
		train_concepts_counts[t[1]] = train_concepts_counts.get(t[1], 0) + 1
		total += 1
		
sorted_train_concepts = sorted(train_concepts_counts.items(), key=lambda x: x[1], reverse=True)
print("Train concepts: {}".format(sorted_train_concepts))

# Out of concept percentage
print("Train out of concept percentage (\"O\" tag): {}%".format(train_concepts_counts['O']/total*100))
print("Concepts tags for training percentage: {}%\n".format((1-train_concepts_counts['O']/total)*100))

# Save the information about train tags counts in a file
# Header
head = "tag, counts\n"
train_csv.write(head)

for el in sorted_train_concepts:
	string = el[0] + ", " + str(el[1]) + "\n"
	train_csv.write(string)
	

# Count test concepts
test_concepts_counts = {}
total = 0

for p in test_sents:
	for i, t in enumerate(p):
		test_concepts_counts[t[1]] = test_concepts_counts.get(t[1], 0) + 1
		total += 1
		
sorted_test_concepts = sorted(test_concepts_counts.items(), key=lambda x: x[1], reverse=True)
print("Test concepts: {}".format(sorted_test_concepts))

# Out of concept percentage
print("Test out of concept percentage (\"O\" tag): {}%".format(test_concepts_counts['O']/total*100))
print("Concepts tags for test percentage: {}%\n".format((1-test_concepts_counts['O']/total)*100))

# Save the information about test tags counts in a file
# Header
head = "tag, counts\n"
test_csv.write(head)

for el in sorted_test_concepts:
	string = el[0] + ", " + str(el[1]) + "\n"
	test_csv.write(string)
