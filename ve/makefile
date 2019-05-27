REPOROOT = /git

ETC = ./etc

-include makefile.conf

REPO = $(REPOROOT)/pez

FILES = makefile dx70.py

$(FILES): %: $(REPO)/ve/%
	cp $< $@

endpoint-files:
	rsync -av $(REPO)/ve/endpoint/ endpoint/

ve.ini: %: $(ETC)/%
	cp $< $@

install: endpoint-files $(FILES)  ve.ini

	python dx70.py -c ve.ini
