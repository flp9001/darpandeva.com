install:
	pip-compile --upgrade requirements/local.in
	pip-compile --upgrade requirements/production.in
	cp requirements/production.txt requirements.txt
	pip install -r requirements/local.txt
	pip install -r requirements/production.txt

createdb:
	psql -c "CREATE DATABASE darpan_deva;"
	psql -c "CREATE USER darpan_deva WITH PASSWORD 'darpan_deva';"
	psql -c "ALTER ROLE darpan_deva SET client_encoding TO 'utf8';"
	psql -c "ALTER ROLE darpan_deva SET default_transaction_isolation TO 'read committed';"
	psql -c "ALTER ROLE darpan_deva SET timezone TO 'UTC';"
	psql -c "CREATE USER darpan_deva WITH PASSWORD 'darpan_deva';"
	psql -c "CREATE USER darpan_deva WITH PASSWORD 'darpan_deva';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE darpan_deva TO darpan_deva;"
