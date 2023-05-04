run:
	./manage.py runserver

freeze:
	pip freeze > requirements.txt

seed:
	./manage.py loaddata --format=yaml ./activities/seed.yaml
