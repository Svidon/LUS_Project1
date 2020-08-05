# Default command
.DEFAULT_GOAL := help

help:	 ## Show this help message
	@fgrep -h '##' $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	
train:	 ## Train the model and build automatons. Parameters have to be specified.
	@## Use order parameter to specify the ngram order (use an integer number).
	@## Use method to specify the smoothing method to build the language model
	@## 	(possible values are: absolute, katz, kneser_ney, presmoothed, unsmoothed, witten_bell)
	@./automaton.sh $(order) $(method)

tag:	 ## Tag your own sentence (assumed in prova.txt and in same format of extras/sample.txt) and generate resulting fst image
	@./sentence_tag.sh
	
test:	 ## Test the model on the test set. Will generate a file with all tagged sentences and return the model evaluation 
	@./testing.sh

clean:	 ## Clean all temporary and generated files in the directory
	@rm -f *.fst
	@rm -f *.far
	@rm -f *.fsa
	@rm -f *.lm
	@rm -f *.cnt
	@rm -f *lex.txt
	@rm -f wordtag_sent.txt
	@rm -f a.txt
	@rm -f merge.txt
	@rm -f result.txt
	@rm -f evaluation.txt
	@rm -f word.txt
	@rm -f -r test_fsa
	@echo Cleaned directory
