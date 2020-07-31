#!/bin/bash

# Generate FAR with all test sentences
farcompilestrings --symbols=lex.txt --unknown_symbol="<unk>" ../dataset/NL2SparQL4NLU.test.utterances.txt > test.far

# Extract all the sentences in a separate folder
mkdir -p test_fsa
cd test_fsa
farextract --filename_suffix='.fsa' ../test.far
cd ..

# Now cycle on every sentence and compute its tags
for file in  test_fsa/*.fsa; do
	# Compose all elements together
	fstcompose $file automaton.fst |\
	fstcompose - tags.lm | fstshortestpath | fstrmepsilon | fsttopsort |\
	fstprint --isymbols=lex.txt --osymbols=tags.lex.txt | cut -f 3,4 > $file.res.txt
done
echo "Computed TAGs"

# Merge all the results
cat test_fsa/*.res.txt > result.txt

# Here evaluate model
paste ../dataset/NL2SparQL4NLU.test.conll.txt result.txt | cut -f 1,2,4 > merge.txt
perl extras/conlleval.pl -d "\t" < merge.txt > evaluation.txt

# At the end
echo "Testing done"
