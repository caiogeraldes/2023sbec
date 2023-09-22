TARGET=./fala/2023_SBEC_CaioGeraldes.pdf
FALA=./fala

all: tex

tex: $(TARGET)
	cp $(FALA)/main.pdf $(TARGET)

$(TARGET): $(FALA)/main.tex
	{ \
	cd $(FALA)/; \
	lualatex main.tex >> /dev/null; \
	biber main; \
	lualatex main.tex >> /dev/null; \
	lualatex main.tex >> /dev/null; \
	}

clean:
	rm -f $(FALA)/main.aux $(FALA)/main.bbl $(FALA)/main.bcf $(FALA)/main.blg $(FALA)/main.log $(FALA)/main.out $(FALA)/main.pdf $(FALA)/main.run.xml
	
