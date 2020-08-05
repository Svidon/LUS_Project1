#!/bin/bash
# All instructions to get the results are listed in order here

# Generate FSTs with python script
# If you want to use cutoff or lemmas, set the correct value in control variables in the file
python3 train_fsts.py

# Generate lexicon with previous computation
ngramsymbols --OOV_symbol="<unk>" < word.txt  > lex.txt
echo "Generated lexicon"
echo "Generated FSTs"

# Compile FSTs into a complessive one (unk probabilities are already in a.txt)
fstcompile --isymbols=lex.txt --osymbols=wordtags.lex.txt a.txt > automaton.fst
echo "Compiled FSTs"

# Generate language model (word+tags)             
farcompilestrings --symbols=wordtags.lex.txt --unknown_symbol='<unk>' --keep_symbols=1 wordtag_sent.txt > wordtags.far
ngramcount --order=$1 wordtags.far > wordtags.cnt
ngrammake --method=$2 wordtags.cnt > wordtags.lm
echo "Built language model"
echo "Training done"
