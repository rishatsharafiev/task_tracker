#!/bin/bash

echo "Create database and user"

psql -c "CREATE DATABASE tt_db;"
psql -c "CREATE USER tt_user WITH SUPERUSER PASSWORD 'tt_pwd';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE tt_db TO tt_user;"
psql -c "ALTER USER tt_user WITH SUPERUSER;"
