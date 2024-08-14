#!/bin/bash
set -e


# Create databases
for DB in $MYSQL_DATABASES; do
    echo "Creating database: $DB"
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS \`$DB\`;"
done