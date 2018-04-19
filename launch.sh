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