DATABASE_NAME?=

.dropdb:
	@psql -U postgres -c "drop database if exists ${DATABASE_NAME};"

.createdb: .dropdb
	@psql -U postgres -c "create database ${DATABASE_NAME};"
#	pipenv run python rapidpro/manage.py migrate

settings:
	cp src/datagen/settings.py rapidpro/temba/settings.py

develop: settings
	pipenv sync
	pipenv run pip install -q -r rapidpro/pip-freeze.txt
	pipenv run pip install -e .[test]
	pipenv run python rapidpro/manage.py migrate
	cd rapidpro && pipenv run npm install
	pipenv shell

rapidpro: settings
	cd rapidpro && PATH=node_modules/.bin:${PATH} pipenv run ./manage.py runserver


clean:
	rm -fr rapidpro/node_modules rapidpro/sitestatic rapidpro/temba/settings.py

.PHONY: rapidpro
