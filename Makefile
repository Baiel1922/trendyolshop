run:
	./manage.py runserver
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser
kill:
	fuser -k 8000/tcp






