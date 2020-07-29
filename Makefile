# Default command
.DEFAULT_GOAL := help

help:	## Show this help message
	@fgrep -h '##' $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	
train:	## Train the model and build automatons
	@./automaton.sh

tag:	## Tag your own sentence (assumed in prova.txt and in same format of extras/sample.txt) and generate resulting fst image
	@./sentence_tag.sh
	
test:	## Test the model on the test set. Will generate a file with all tagged sentences and return the model evaluation 
	@./testing.sh

clean:	## Clean all temporary and generated files in the directory
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
	@rm -f merge.txt
	@rm -f result.txt
	@rm -f -r test_fsa
	@echo Cleaned directory
