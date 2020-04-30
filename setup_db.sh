#!/bin/bash

sed 's/127.0.0.1/0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl restart mysql
mysql << EOF
UPDATE mysql.user SET Password = PASSWORD('CHANGEME') WHERE User = 'root';
mysql -e "DROP DATABASE test";
mysql -e "FLUSH PRIVILEGES";
CREATE DATABASE inshort;
GRANT ALL ON inshort.* TO inshort@'%' IDENTIFIED BY 'j3qq4h7h2v';
SET GLOBAL event_scheduler = ON;
EOF

# ДОБАВИТЬ В setup.py после mygrate 
mysql -u root -p 'j3qq4h7h2v' -e 'CREATE EVENT test_event_03 ON SCHEDULE EVERY 1 MINUTE STARTS CURRENT_TIMESTAMP DO UPDATE inshort.custom_urls_customurl SET active = 0 WHERE expation_date < NOW();'

