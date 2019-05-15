
# export from production database

# assumes user's CNF is set up

dumpfile=staff.sql
mysqldump --opt deldev staff > $dumpfile

ls -l $dumpfile
