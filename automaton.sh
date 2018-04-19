#!/bin/bash
# All instructions to get the results are listed in order here
# For the vocabularies one could also uncomment the code in the python code


# Create lexicon
ngramsymbols < data/NLSPARQL.train.data > lex.txt

# Add starting and ending symbols to lexicon
echo "<s>	1771" >> lex.txt
echo "<\s>	1772" >> lex.txt
echo "Generated lexicon"

# Generate fsts with python script
python3 fst_generator.py
echo "Generated FSTs"

# Compile fsts into a complessive one
fstcompile --isymbols=lex.txt --osymbols=lex.txt a.txt > a.fst
fstcompile --isymbols=lex.txt --osymbols=lex.txt unk.txt > unk.fst
fstunion a.fst unk.fst > automaton.fst
echo "Compiled FSTs"

# Generate language model
farcompilestrings --symbols=lex.txt --unknown_symbol='<unk>' tag_sent.txt > tags.far
ngramcount --order=3 --require_symbols=false tags.far > tags.cnt
ngrammake --method=witten_bell tags.cnt > tags.lm
echo "Built language model"

# Build fsa for sentence (assume 'prova.txt' is the file)
fstcompile --acceptor --isymbols=lex.txt --osymbols=lex.txt prova.txt > sent.fsa

# Compose all elements together
fstcompose sent.fsa automaton.fst |\
fstcompose - tags.lm |\
fstrmepsilon | fstshortestpath > result.fst
echo "Computed TAGs"

# Print resulting automaton
fstprint --isymbols=lex.txt --osymbols=lex.txt result.fst