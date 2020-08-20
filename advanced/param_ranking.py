import os

# Open needed files
output = open('param_ranking.txt', 'w')

# Path to working directory
path1 = os.getcwd()

# Dictionary -> filename: F1 score
ranking = {}

# Navigate all evaluation files
for ev in os.listdir(path1+'/model_evaluations'):
	path = path1+'/model_evaluations/'
	with open(path+ev, 'r') as f:
		# We only need to read the second line (the one with the global F1)
		for i, line in enumerate(f):
			if i == 1:
				a = list(line.split())
				ranking[ev] = a[-1]
				
# Sort them wrt F1 score				
ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)

# Write in output file
for key in ranking:
	string = key[0] + '\t' + key[1] +'\n'
	output.write(string)
