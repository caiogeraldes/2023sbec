FALA=./fala
TARGET=$(FALA)/2023_SBEC_CaioGeraldes.pdf
PRETARGET=$(FALA)/main.pdf
DIORISIS=./dados/diorisis/diorisis.zip
BIBLIO=$(FALA)/bibliografia/biblio.bib

all: $(TARGET)

$(TARGET): $(PRETARGET)
	cp $(FALA)/main.pdf $(TARGET)

$(PRETARGET): $(FALA)/main.tex $(BIBLIO)
	{ \
	cd $(FALA)/; \
	lualatex main.tex >> /dev/null; \
	biber main; \
	lualatex main.tex >> /dev/null; \
	lualatex main.tex >> /dev/null; \
	}

$(BIBLIO):
	git submodule update;

$(DIORISIS):
	{ \
	cd ./dados; \
	mkdir diorisis; \
	cd ./diorisis; \
	wget https://figshare.com/ndownloader/files/27831960; \
	mv 27831960 diorisis.zip; \
	}

diorisis: $(DIORISIS)
	{ \
	cd ./dados; \
	cd ./diorisis; \
	unzip -j "diorisis.zip" "Herodotus (0016) - Histories (001).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Apology (002).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Charmides (018).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Cratylus (005).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Critias (032).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Crito (003).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Euthydemus (021).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Euthyphro (001).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Gorgias (023).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Hippias Major (025).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Hippias Minor (026).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Ion (027).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Laches (019).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Laws (034).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Lysis (020).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Meno (024).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Parmenides (009).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Phaedo (004).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Phaedrus (012).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Philebus (010).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Protagoras (022).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Republic (030).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Sophist (007).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Statesman (008).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Symposium (011).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Theaetetus (006).json";\
  unzip -j "diorisis.zip" "Plato (0059) - Timaeus (031).json";\
  unzip -j "diorisis.zip" "Thucydides (0003) - History (001).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Agesilaus (009).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Anabasis (006).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Apology (005).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Cyropaedia (007).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Hellenica (001).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Hiero (008).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Memorabilia (002).json";\
  unzip -j "diorisis.zip" "Xenophon (0032) - Symposium (004).json";\
	}

clean:
	rm -f $(FALA)/main.aux\
		$(FALA)/main.bbl\
		$(FALA)/main.bcf\
		$(FALA)/main.blg\
		$(FALA)/main.log\
		$(FALA)/main.out\
		$(FALA)/main.pdf\
		$(FALA)/main.run.xml\
		$(DIORISIS)
	
