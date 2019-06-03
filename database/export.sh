
# export from production database

# assumes user's CNF is set up
DB=test
dumpfile=staff.sql
mysqldump --opt $DB staff staff_email > $dumpfile

ls -l $dumpfile

# TODO:
#  upload to file-depot
