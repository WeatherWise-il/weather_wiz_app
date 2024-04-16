CREATE DATABASE weather_db;

use weather_db;

SET SESSION sql_mode = '';

CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(75) NOT NULL,
    state_code VARCHAR(20) NOT NULL,
    country_code VARCHAR(20) NOT NULL,
    country_full VARCHAR(45) NOT NULL,
    city_lat  DECIMAL(11,8) NOT NULL,
    city_lon DECIMAL(11,8) NOT NULL
);


LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE cities
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(city_id, city_name, state_code, country_code, country_full, city_lat, city_lon);



GRANT SELECT  ON weather_db.* TO 'appuser'@'%';
FLUSH PRIVILEGES;



