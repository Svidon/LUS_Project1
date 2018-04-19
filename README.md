# LUS_Project1

First project for Language Understanding System course about _Concept tagging_.
The dataset used is about films.

## How to use

You have to have installed python3, opengrm and openfst.
Simply run `./automaton.sh` and the script will generate a lexicon file (`lex.txt`) and an automaton (`automaton.fst`) for concept tagging with _IOB_ tag. If you have a sentence modeled with an FSA you can tag it.
ATM the model is build... next is to evaluate it on the test set, than to further improve it.
