FROM postgres:12.3

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

COPY postgresql.conf    /etc/postgresql/postgresql.conf
COPY init-postgres.sh   /docker-entrypoint-initdb.d/init.db.sh

EXPOSE 5432

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
