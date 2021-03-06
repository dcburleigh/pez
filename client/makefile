

# .......................................
# Use this code for testing
#
#
# usage:
#  mkdir client
#  cp GIT/pez/client/makefile .
#  edit makefile.conf
#  make install
#
# use the 'show' tool to access the code running directly on the host
# use the 'client' tool to access the code running in the container
#
# .......................................
REPOROOT = /git

#SOPT = --server host
SOPT = --server prod
SOPT = --server ace
SOPT = --server local

# test hook file label
T = managers

-include makefile.conf


# .......................................

REPO = $(REPOROOT)/pez

#  .....................................................................

CLIENTFILES = makefile  client.py show.py requirements.txt

$(CLIENTFILES): %: $(REPO)/client/%
	@cp $< $@

client-files: $(CLIENTFILES)

server-files: $(REPO)/server
	rsync -av  $(REPO)/server/ ./

install: client-files server-files  client_env.py

install-py: requirements.txt
	pip install -r requirements.txt

ifneq ($(PEZ_AUTH_TOKEN),)

has-auth-token check-auth-token:
	@echo OK

endif

#  .....................................................................

create-hook: check-auth-token client-files  py-project
	python hooks.py --hello $(SOPT)

#  .....................................................................

#
# use client to hit special esrver endpoints
#

hello: check-auth-token client-files
	python client.py --hello $(SOPT)

hello-local: check-auth-token client-files
	python client.py --hello --server local

whois: client-files
	@PEZ_AUTH_TOKEN=$(PEZ_AUTH_TOKEN) python client.py $(SOPT) --whois --userid 2474


#
# sample hook message
# for testing
#
HFILE = data/hook_message_name.json
HFILE = data/hook_message_reports.json
#HFILE = data/hook_message_managers.json
HFILE = data/hook_message_test.json
HFILE = data/hook_message_$(T).json
#HFILE = data/hook_message.json

#
# use show command to access server directly from the host
#

display-hook: check-auth-token  client-files server-files $(HFILE)
	echo f is $(HFILE)
	python show.py --hook $(HFILE) --display

show-hook: check-auth-token  client-files server-files $(HFILE)
	echo f is $(HFILE)
	python show.py --hook $(HFILE)

show-whois: check-auth-token client-files server-files data/hook_message_whois.json
	python show.py --hook data/hook_message_whois.json


#
# use client script to access server running via container
#    emulate the message posted from a web hook
#
post-help:  check-auth-token client-files data/hook_message_help.json
		python client.py $(SOPT) --hook data/hook_message_help.json

post-whois: client-files data/hook_message_whois.json
		python client.py $(SOPT) --hook data/hook_message_whois.json

post-hook:  client-files $(HFILE)
		python client.py $(SOPT) --hook $(HFILE)
