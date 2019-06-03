REPOROOT = /git

-include makefile.conf

REPO = $(REPOROOT)/pez

# 1) create tables in local MySQL database

F1 = makefile create_tables.sql

$(F1): %: $(REPO)/database/%
	cp $< $@

create-tables: $(F1)
	mysql test < create_tables.sql

# 2. populate the tables with your corporate directory,
# OR  try the sample data

F2 = staff.csv load.sh

$(F2): %: $(REPO)/database/sample_data/%
	cp $< $@

load-sample-data: $(F2)
	./load.sh


# 3. Export the tables from the local host database

./export.sh

# 4. import the tables into the docker container

./import.sh
