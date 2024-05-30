# How to install opensky api dependencies

* in `/flight_data` run `pip install -e opensky-api/python`
* `pip install pandas`
* `python scrape_adsb_data.py`

# How to install and set up postgreSQL

* First set up psql in your machines terminal:
* install postgreSQL: sudo dnf install postgresql-server postgresql-contrib
* initialize the psql database cluster: sudo postgresql-setup --initdb
* start psql: sudo systemctl start postgresql
* enable psql: sudo systemctl enable postgresql
* create a database and user: sudo -u postgres psql

* now you're in postgres, do the following:
* CREATE DATABASE adsb_data;
* CREATE USER <username> WITH PASSWORD '<password>';
* ALTER ROLE <username> SET client_encoding TO 'utf8';
* ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';
* ALTER ROLE <username> SET timezone TO 'UTC';
* GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;
* \c adsb_data eheidrich
* \conninfo (gets the info for the url to use with sqlalchemy)
* \q (quits postgres in terminal)