FALA=./fala
TARGET=$(FALA)/2023_SBEC_CaioGeraldes.pdf
PRETARGET=$(FALA)/main.pdf
BIBLIO=$(FALA)/bibliografia/biblio.bib
DATAOK=./dados/diorisis/dataok
FIGURAS_PATH=$(FALA)/figs/
DATA_PATH=./dados/diorisis/

all: $(TARGET)

$(TARGET): $(PRETARGET)
	{\
		cp $(PRETARGET) $(TARGET);\
		rm -f $(PRETARGET) \
				$(FALA)/main.aux\
				$(FALA)/main.bbl\
				$(FALA)/main.bcf\
				$(FALA)/main.blg\
				$(FALA)/main.log\
				$(FALA)/main.out\
				$(FALA)/main.run.xml;\
	}

$(PRETARGET): $(FALA)/main.tex $(BIBLIO) $(FIGURAS_PATH)/confusao.png $(FIGURAS_PATH)/diff2.png $(FIGURAS_PATH)/diffz.png
	{ \
	cd $(FALA)/; \
	lualatex main.tex >> /dev/null; \
	biber main; \
	lualatex main.tex >> /dev/null; \
	lualatex main.tex >> /dev/null; \
	}

$(BIBLIO):
	git submodule update --init --remote --recursive;

$(DATAOK):
	{ \
	mkdir -p dados/diorisis;\
	cd ./dados/diorisis/; \
	wget https://figshare.com/ndownloader/files/27831960; \
	mv 27831960 diorisis.zip; \
  unzip -jo "diorisis.zip" "Plato (0059) - Apology (002).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Charmides (018).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Cratylus (005).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Critias (032).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Crito (003).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Euthydemus (021).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Euthyphro (001).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Gorgias (023).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Hippias Major (025).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Hippias Minor (026).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Ion (027).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Laches (019).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Laws (034).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Lysis (020).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Meno (024).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Parmenides (009).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Phaedo (004).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Phaedrus (012).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Philebus (010).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Protagoras (022).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Republic (030).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Sophist (007).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Statesman (008).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Symposium (011).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Theaetetus (006).json";\
  unzip -jo "diorisis.zip" "Plato (0059) - Timaeus (031).json";\
  unzip -jo "diorisis.zip" "Thucydides (0003) - History (001).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Agesilaus (009).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Anabasis (006).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Apology (005).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Cyropaedia (007).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Hellenica (001).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Hiero (008).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Memorabilia (002).json";\
  unzip -jo "diorisis.zip" "Xenophon (0032) - Symposium (004).json";\
	unzip -jo "diorisis.zip" "Herodotus (0016) - Histories (001).json";\
	rm -f "diorisis.zip";\
	rm -f 27831960 27831960.*;\
	touch dataok;\
	}

$(FIGURAS_PATH)/confusao.png $(FIGURAS_PATH)/diff2.png $(FIGURAS_PATH)/diffz.png: $(DATAOK)
	{ \
		cd ./dados/lexicogenero/;\
		poetry run python src/lexicogenero/main.py;\
	}

python:
	{\
		cd ./dados/lexicogenero/;\
		poetry install;\
		poetry run pip install torch;\
	}

env:
	{\
		rm -f "$$(pwd)/dados/lexicogenero/.env";\
		echo "DIORISIS_PATH=\"$$(pwd)/dados/diorisis/\"" >> "$$(pwd)/dados/lexicogenero/.env";\
		echo "FIGURAS_PATH=\"$$(pwd)/fala/figs/\"" >> "$$(pwd)/dados/lexicogenero/.env";\
		cat "$$(pwd)/dados/lexicogenero/.env";\
	}

clean:
	rm -f $(TARGET)\
	  $(FIGURAS_PATH)/confusao.png\
	  $(FIGURAS_PATH)/diff2.png\
	  $(FIGURAS_PATH)/diffz.png\
	  $(DATAOK)\
	  $(DATA_PATH)/*.json
	
