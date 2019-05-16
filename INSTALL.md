# Installation

## install  database

database is running in separate MariaDB container, assumed running.

see: GIT/kofun/perl-db

* export from production

./export.sh

* import to database to container

./import.sh

* configure database credentials

edit etc/deldev_db.cnf
add database credentials
see: etc/db.example.cnf

edit etc/env.txt
set DB_CONFIG_FILE


## Install as docker container

see: docker/makefile

## create bot

### Webex teams bot
https://developer.webex.com

<avatar> > My apps > create new app > create a bot

* configure

edit etc/env.txt
set PEZBOT_ACCESS_TOKEN to the access token created above


### create hook
