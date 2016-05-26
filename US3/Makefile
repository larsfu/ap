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
build/a1.pdf: auswertung/a.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/a.py
build/b1.pdf: auswertung/b.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/b.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/b1.pdf build/a1.pdf

build/main.pdf: FORCE | build
	  TEXINPUTS="$(call translate,build:)" \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
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
