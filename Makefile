up:
	docker-compose up --build -d

down:
	docker-compose down --rmi 'all'

web:
	docker exec -it short_link_service_web_1 bash

db:
	docker exec -it short_link_service_db_1 bash

nginx:
	docker exec -it short_link_service_nginx_1 bash

chown:
	sudo chown -R ${USER}:${USER} .

test:
	python manage.py test

prep:
	pip install --upgrade wheel

ps:
	psql -U postgres