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
build/dispersion1.pdf: auswertung/dispersion1.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/dispersion1.py
build/dispersion2.pdf: auswertung/dispersion2.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/dispersion2.py
build/eigenschwingung1.pdf: auswertung/eigenschwingung1.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/eigenschwingung1.py
build/eigenschwingung2.pdf: auswertung/eigenschwingung2.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/eigenschwingung2.py
build/v-ph.pdf: auswertung/phasengeschwindigkeit.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/phasengeschwindigkeit.py
build/wellenwiderstand.pdf: auswertung/wellenwiderstand.py matplotlibrc | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/wellenwiderstand.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/a1.pdf build/dispersion1.pdf build/dispersion2.pdf build/eigenschwingung1.pdf build/eigenschwingung2.pdf build/v-ph.pdf build/wellenwiderstand.pdf

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
