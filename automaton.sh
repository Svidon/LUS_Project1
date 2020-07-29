#!/bin/bash
# All instructions to get the results are listed in order here

# Create lexicon (OOV specified, it was all capital by default, dunno why)
ngramsymbols --OOV_symbol="<unk>" < dataset/NL2SparQL4NLU.train.utterances.txt  > lex.txt
echo "Generated lexicon"

# Generate FSTs with python script
python3 train_fsts.py
echo "Generated FSTs"

# Compile FSTs into a complessive one
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt a.txt > a.fst
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt unk.txt > unk.fst
fstunion a.fst unk.fst > automaton.fst
echo "Compiled FSTs"

# Generate language model               
farcompilestrings --symbols=tags.lex.txt --unknown_symbol='<unk>' --keep_symbols=1 tag_sent.txt > tags.far
ngramcount --order=3 tags.far > tags.cnt
ngrammake --method=witten_bell tags.cnt > tags.lm
echo "Built language model"
echo "Training done"
