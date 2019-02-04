settings:
	cp src/datagen/settings.py rapidpro/temba/settings.py

develop: settings
	pip install -r rapidpro/pip-freeze.txt
	python rapidpro/manage.py migrate
	pip install -e .

rapidpro: settings
	cd rapidpro && PATH=node_modules/.bin:${PATH} ./manage.py runserver


.PHONY: rapidpro
