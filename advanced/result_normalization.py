# Read correct data and computed tags
res_tmp = open('result_tmp.txt', 'r')
result = open('result.txt', 'w')

for line in res_tmp:
	a = list(line.split())
	
	if len(a) > 0:
		# Split the second element into word and tag
		tag = a[1].split('+')
		
		# Check the length of the splitted tag (this is because of '<unk>' tags)
		if len(tag) > 1:
			tag = tag[1]
		else:
			tag = tag[0]
		
		# Concatenate word and new tag and write
		string = a[0] + '\t' + tag + '\n'
		result.write(string)	
	else:
		result.write('\n')

result.close()
