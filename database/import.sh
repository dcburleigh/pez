
dumpfile=staff.sql

# Path to container home directory on host
DBDIR=../mysql-deldev

# volume on host host
HVOL=$DBDIR/shared/admin

# corresponding shared volume in container
CVOL=/home/admin

# name of container
DBCNAME=deldevdb0

if [[ ! -d $DBDIR ]]
then
  echo ERROR no such directory $DBDIR
  exit
fi

if [[ ! -f $dumpfile ]]
then
  echo ERROR no such file $dumpfile
  exit
fi

cp $dumpfile $DBDIR/shared/admin
ls -l $DBDIR/shared/admin/$dumpfile

# import

docker exec $DBCNAME bash -c "mysql deldev < /home/admin/$dumpfile"
