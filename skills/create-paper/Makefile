MAIN  = main
FLAGS = -pdf -interaction=nonstopmode -halt-on-error

.PHONY: all watch clean open

## Compile once (handles bibliography automatically via latexmk)
all:
	latexmk $(FLAGS) $(MAIN).tex

## Compile and recompile automatically on save (Ctrl-C to stop)
watch:
	latexmk $(FLAGS) -pvc $(MAIN).tex

## Compile and open the PDF
open: all
	open $(MAIN).pdf

## Remove all LaTeX auxiliary files
clean:
	latexmk -C $(MAIN).tex
