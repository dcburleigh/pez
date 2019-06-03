use mysql;

create database deldev;
  
-- user @ localhost (in the container)
grant select on deldev.* to deldevuser@localhost identified by 'userpassword';
grant all on deldev.* to deldevadmin@localhost identified by 'adminpassword';

-- remote user, e.g. another container
grant select on deldev.* to deldevuser@'%' identified by 'userpassword';
grant all on deldev.* to deldevadmin@'%' identified by 'adminpassword';
