#!/bin/bash
# All instructions to get the results are listed in order here

# Create lexicon
ngramsymbols < dataset/NL2SparQL4NLU.train.conll.txt > lex.txt

# Add starting and ending symbols to lexicon
#echo "<s>	1771" >> lex.txt
#echo "<\s>	1772" >> lex.txt
echo "Generated lexicon"

# Generate FSTs with python script and also other needed files
python3 fst_generator.py
echo "Generated FSTs"

# Compile FSTs into a complessive one
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt a.txt > a.fst
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt unk.txt > unk.fst
fstunion a.fst unk.fst > automaton.fst
echo "Compiled FSTs"

# Generate language model
farcompilestrings --symbols=tags.lex.txt --unknown_symbol='<unk>' tag_sent.txt > tags.far
ngramcount --order=3 --require_symbols=false tags.far > tags.cnt
ngrammake --method=witten_bell tags.cnt > tags.lm
echo "Built language model"
echo "Training done"

# Generate FST for test data
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt a_test.txt > a_test.fst
echo "Built FST for test"

# Generate FSA for test data
#fstcompile --acceptor --isymbols=lex.txt --osymbols=tags.lex.txt a_test_fsa.txt > a_test.fsa
#echo "Built FSA for test"


# Compose all elements together
fstcompose a_test.fst automaton.fst |\
fstcompose - tags.lm |\
fstrmepsilon > result.fst
echo "Computed TAGs"

# Print resulting automaton
fstprint --isymbols=lex.txt --osymbols=tags.lex.txt result.fst
fstdraw --isymbols=lex.txt --osymbols=tags.lex.txt -portrait result.fst | dot -Tpng -Gdpi=300 >diome.png