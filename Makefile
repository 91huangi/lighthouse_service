build:
	docker-compose build

clean:
	docker-compose down

up:
	docker-compose -p lighthouse_service up -d

refresh_app:
	-docker rm -f lighthouse_service_app_1
	docker-compose -p lighthouse_service up -d
