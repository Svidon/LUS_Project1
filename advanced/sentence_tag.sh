#!/bin/bash

# Build fsa for sentence (assume prova.txt is the file)
fstcompile --acceptor --isymbols=lex.txt --osymbols=wordtags.lex.txt prova.txt > sent.fsa

# Compose all elements together
fstcompose sent.fsa automaton.fst |\
fstcompose - wordtags.lm |\
fstshortestpath |\
fstrmepsilon |\
fsttopsort > result.fst
echo "Computed TAGs"

# Print resulting automaton
fstprint --isymbols=lex.txt --osymbols=wordtags.lex.txt result.fst
fstdraw --isymbols=lex.txt --osymbols=wordtags.lex.txt -portrait result.fst | dot -Tpng -Gdpi=300 > tagged.png
