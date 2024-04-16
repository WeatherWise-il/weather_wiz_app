FROM mysql/mysql-server:8.0.32-1.2.11-server
ENV MYSQL_USER=appuser
ENV MYSQL_PASSWORD=appuser1
ENV MYSQL_ROOT_PASSWORD=root
ENV DB_PORT=3306
# Copy my.cnf config file
COPY ./config/my.cnf /etc/mysql/my.cnf 
# Copy citis CSV data to defualt MySQL data location.
COPY ./data/data.csv /var/lib/mysql-files/data.csv
COPY init.sql /docker-entrypoint-initdb.d/init.sql
EXPOSE $DB_PORT





