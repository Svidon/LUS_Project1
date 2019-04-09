# Default command
.DEFAULT_GOAL := automaton

# Obtain Tags
automaton:
	@./automaton.sh

# Tag your own sentence
tag:
	@./sentence_tag.sh

# Clean all files in directory
clean:
	@rm -f *.fst
	@rm -f *.far
	@rm -f *.fsa
	@rm -f *.lm
	@rm -f *.cnt
	@rm -f *lex.txt
	@rm -f unk.txt
	@rm -f tag_sent.txt
	@rm -f a.txt
	@rm -f a_test.txt
	@rm -f *.png
	@echo Cleaned directory