settings:
	cp src/datagen/settings.py rapidpro/temba/settings.py

develop: settings
#	pipenv run pip install -r rapidpro/pip-freeze.txt
#	pipenv run python rapidpro/manage.py migrate
	cd rapidpro && pipenv run npm install
	pipenv run pip install -e .[test]

rapidpro: settings
	cd rapidpro && PATH=node_modules/.bin:${PATH} pipenv run ./manage.py runserver


clean:
	rm -fr rapidpro/node_modules rapidpro/sitestatic rapidpro/temba/settings.py

.PHONY: rapidpro
