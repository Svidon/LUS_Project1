#!/bin/bash
# All instructions to get the results are listed in order here

# Create lexicon (OOV specified, it was all capital by default, dunno why)
# Comment if we want to use the cutoff
ngramsymbols --OOV_symbol="<unk>" < ../dataset/NL2SparQL4NLU.train.utterances.txt  > lex.txt
echo "Generated lexicon"

# Generate FSTs with python script
python3 train_fsts.py
# If you wanna use cutoff use the following line and comment above:
#python3 train_fsts_cutoff.py
echo "Generated FSTs"

# Compile FSTs into a complessive one (unk probabilities are already in a.txt)
fstcompile --isymbols=lex.txt --osymbols=tags.lex.txt a.txt > automaton.fst
echo "Compiled FSTs"

# Generate language model               
farcompilestrings --symbols=tags.lex.txt --unknown_symbol='<unk>' --keep_symbols=1 tag_sent.txt > tags.far
ngramcount --order=$1 tags.far > tags.cnt
ngrammake --method=$2 tags.cnt > tags.lm
echo "Built language model"
echo "Training done"
