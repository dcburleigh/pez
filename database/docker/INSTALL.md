# Installation

create the MySQL docker container

* edit etc files

set the rootpassword, adminpassword, userpassword

* create image

docker build -t pezdb:v1.0 .

* run container

- database files are in shared volume shared/mysql
- map container port to external 3307

mkdir -p shared/admin
mkdir -p shared/mysql

docker run -dit --env-file  ./etc/deldev_db_env.txt -p 3307:3306 --volume HERE/shared/mysql:/var/lib/mysql  --volume HERE/shared/admin:/home/admin  --rm  --name pezdb pezdb:v1.0
