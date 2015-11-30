ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/main.pdf

# hier Python-Skripte:
build/e1.pdf: auswertung/e.py matplotlibrc daten/e.txt build/c3.pickle | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/e.py

#Ich hab die restlichen Textdateien weggelassen..
build/a1.txt, build/c3.pickle: auswertung/abcd.py daten/a.txt daten/b.txt daten/c.txt daten/d.txt | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/abcd.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/e1.pdf build/a1.txt

build/main.pdf: FORCE | build
	  TEXINPUTS="$(call translate,build:)" \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --xelatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex

build:
	mkdir -p build

clean:
	rm -rf build

FORCE:

.PHONY: all clean
