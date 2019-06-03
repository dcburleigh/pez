mysqlimport   --fields-terminated-by=,  \
 --columns='user_id,name,title,manager_user_id,email,active' \
 --local  test staff.csv
