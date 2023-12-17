PY=C:\Pvthon27amd64\python.exe
EPS2PDF=ps2pdf
CROP=pdfcrop

SRC := $(wildcard *.py)
SRC := $(filter-out zplot.py，$(SRC))
EPS = $(patsubst %.py,%.eps,$(SRC))
PDF = $(patsubst %.py,%.pdf,$(SRC))

all: $(EPS) $(PDF)

%.eps: %.py
	$(PY) $< eps

%.pdf: %.eps
	$(EPS2PDF) $<
	$(CROP) $O $
	del $<

fig:
	//move *.pdf .. ..
	copy *.pdf ..\..\

clean:
	del *.eps *.pdf