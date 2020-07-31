#!/bin/bash

# Build fsa for sentence (assume prova.txt is the file)
fstcompile --acceptor --isymbols=lex.txt --osymbols=tags.lex.txt prova.txt > sent.fsa

# Compose all elements together
fstcompose sent.fsa automaton.fst |\
fstcompose - tags.lm |\
fstshortestpath |\
fstrmepsilon |\
fsttopsort > result.fst
echo "Computed TAGs"

# Print resulting automaton
fstprint --isymbols=lex.txt --osymbols=tags.lex.txt result.fst
fstdraw --isymbols=lex.txt --osymbols=tags.lex.txt -portrait result.fst | dot -Tpng -Gdpi=300 > tagged.png
