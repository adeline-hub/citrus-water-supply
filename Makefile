.PHONY: all data eda report clean publish

PYTHON = python
QUARTO = quarto

all: data report

data:
	$(PYTHON) src/generate_data.py

eda:
	marimo run notebooks/eda_marimo.py

report:
	cd report && $(QUARTO) render index.qmd --to html
	cd report && $(QUARTO) render index.qmd --to pdf
	cp -r report/_site/* docs/

clean:
	rm -rf report/_site docs/* data/processed/*

publish:
	cd report && $(QUARTO) publish gh-pages