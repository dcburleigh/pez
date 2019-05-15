
REPOROOT = /data/git

# Usage:
#
# Set up build directory
#
# cd kofun
# mkdir pez
# cd peze
# cp $(APPHOME)/docker/makefile  .
# edit makefile.conf
# make update-files
#
# The source file 'main.py' over-writes the default 'main.py' in starting container
#
# Run:
#    make build run check-URL
#
# see:
#    https://store.docker.com/community/images/tiangolo/uwsgi-nginx-flask
#https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask
#
# .....................................................................


IMG = pez
CNAME = $(IMG)
###CPATH = examples/$(IMG)

REPO = $(REPOROOT)/pez
MYDIR = $(REPOROOT)/pez/docker


FROMPORT = 80
PORT = 8020
CSHELL = ash

SRCPATH = src

PRODUCTION = 0

REPOTARGETS =

ETC = ./etc

-include makefile.conf

# .....................................................................
#
#  run options
#

VOLUMES =

#  .....................................................................
include ../common/makefile.inc

APPFILES = $(SRCPATH)/main.py   $(SRCPATH)/uwsgi.ini
APPFILES = $(SRCPATH)/main.py $(SRCPATH)/requirements.txt

$(APPFILES): $(SRCPATH)/% : $(MYDIR)/../server/%
	cp $< $@

#$(SRCPATH)/auth $(SRCPATH)/staffdb: $(SRCPATH)/%:  $(REPO)/server/%
#	rsync -av $</ $@/

app-mods:
	@rsync -a $(REPO)/server/auth/ $(SRCPATH)/auth/
	@rsync -a $(REPO)/server/staffdb/ $(SRCPATH)/staffdb/

#  .....................................................................

app-files: $(SRCPATH) $(APPFILES) app-mods

clean-src1:
	rm -rf $(SRCPATH)

re-app: clean-src app-files


#  .....................................................................
#
# run options
#

RUNARGS = --env-file=env.txt


ETCFILES = env.txt

$(ETCFILES): %: $(ETC)/%
	cp $< $@

#  ...................................................................
# hose-to-container
APPURL = http://localhost:$(PORT)/
check-url:
	@echo URL $(APPURL)
	@wget $(APPURL) -O info.html
	ls -l info.html

test-auth:
	@echo URL $(APPURL)
	@echo NOT WORKING needs auth
	@wget $(APPURL)/test -O test.html
	ls -l test.html

hello:
	@echo URL $(APPURL)
	@wget $(APPURL)/hello -O hello.html
	ls -l hello.html

#  .....................................................................
clean-dockerfile:
	rm -f Dockerfile

#  .....................................................................

DBFILES = import.sh export.sh

$(DBFILES): %: $(REPO)/database/%
	cp $< $@

db-files: $(DBFILES)

#  .....................................................................

CLIENTFILES = client.py

$(CLIENTFILES): %: $(REPO)/client/%
	cp $< $@

client-files: $(CLIENTFILES)

test-hello: client-files
	PEZ_AUTH_TOKEN=$(PEZ_AUTH_TOKEN) python client.py --hello --server local 

#  .....................................................................


# ports: 80, 3306
DEPENDS = httpd0

check-depends:
	@echo TODO verify these other images are running $(DEPENDS)
	docker ps -a --filter "name=$(DBCNAME)"
	docker ps -a --filter "name=httpd0"


makefile Dockerfile $(OTHERFILES): %:  $(MYDIR)/%
	rsync -av $< .

update-files: update-common Dockerfile  $(OTHERFILES)  app-files $(ETCFILES) client-files
