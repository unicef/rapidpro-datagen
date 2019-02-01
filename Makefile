develop:
#	pip install -r rapidpro/pip-freeze.txt
	cp src/datagen/settings.py rapidpro/temba/settings.py
	python rapidpro/manage.py migrate
	pip install -e .
