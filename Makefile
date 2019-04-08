# Obtain Tags
automaton:
	@./automaton.sh

# Clean all files in directory
clean:
	@rm *.fst
	@rm *.far
	@rm *.fsa
	@rm *.lm
	@rm *.cnt
	@rm lex.txt
	@rm unk.txt
	@rm tag_sent.txt
	@rm a.txt
	@rm a_test.txt
	@rm *.png
	@echo Cleaned directory