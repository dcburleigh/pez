#https://hub.docker.com/_/mariadb/
FROM mariadb:10.2

MAINTAINER  DelDev

# first time setup only
COPY etc/create_deldev.sql /docker-entrypoint-initdb.d

# for convenience when we connect to the container's shell
COPY etc/root.my.cnf /root/.my.cnf

# create non-priv user with access to the deldev database
RUN useradd -g users -m deldev
COPY etc/deldev.my.cnf /home/deldev/.my.cnf
RUN chown deldev:users /home/deldev/.my.cnf

EXPOSE 3306
