REPOROOT = /git

-include makefile.conf

REPO = $(REPOROOT)/pez

# 1) create tables in local MySQL database

F1 = makefile create_tables.sql export.sh import.sh 

$(F1): %: $(REPO)/database/%
	cp $< $@

db-files: $(F1)

create-tables: db-files
	mysql test < create_tables.sql

# 2. populate the tables with your corporate directory,
# OR  try the sample data

F2 = staff.csv load.sh

$(F2): %: $(REPO)/database/sample_data/%
	cp $< $@

load-sample-data: $(F2)
	./load.sh


# 3. Export the tables from the local host database

# ./export.sh

# 4. Create the MySQL container

container-files:
	rsync -avu $(REPO)/database/docker/ docker/
	copy $(REPO)/database/create_tables.sql docker


# see: INSTALL.md


# 5. import the tables into the docker container

# ./import.sh
