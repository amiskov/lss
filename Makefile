run:
	./manage.py runserver 0.0.0.0:8080

freeze:
	pip freeze > requirements.txt

seed:
	./manage.py loaddata --format=yaml ./activities/seed.yaml
