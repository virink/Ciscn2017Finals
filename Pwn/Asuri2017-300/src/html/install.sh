#!/bin/bash

#systemctl start mariadb && mysql -e 'source /var/www/html/babytrick.sql'


mkdir /var/www/html/upload/

chown -R www-data:www-data /var/www/html/

service apache2 start

/bin/bash
