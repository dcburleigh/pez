
# export from production database

# assumes user's CNF is set up

dumpfile=staff.sql
mysqldump --opt deldev staff staff_email > $dumpfile

ls -l $dumpfile
