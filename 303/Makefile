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
build/plot.pdf: auswertung/plot.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/plot.py

build/plot2.pdf: auswertung/plot2.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/plot2.py

build/plot3.pdf: auswertung/plot3.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/plot3.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/plot2.pdf build/plot.pdf

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
