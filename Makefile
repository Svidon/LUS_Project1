# Obtain Tags
automaton:
	@./automaton.sh

# Clean all files in directory
clean:
	@rm *.fst
	@rm *.far
	@rm *.lm
	@rm *.cnt
	@rm lex.txt
	@rm unk.txt
	@rm tag_sent.txt
	@rm a.txt
	@rm a_test.txt
	@echo Cleaned directory