FROM postgres:16-alpine

# RUN rm -rf /var/lib/postgresql/data
COPY init.sql /docker-entrypoint-initdb.d/init.sql
COPY postgresql.conf /etc/postgresql.conf

ENTRYPOINT ["docker-entrypoint.sh", "-c", "config_file=/etc/postgresql.conf"]
