build:
	docker-compose build

clean:
	docker-compose down

up:
	docker-compose -p lighthouse_service up -d

refresh_app:
	-docker rm -f lighthouse_service_app_1
	docker-compose -p lighthouse_service up -d

push:
	rsync -rav \
		  --exclude '.git' \
		  --exclude 'app/reports' \
		  -e "ssh -i ~/.ssh/lighthouse_service.pem" \
		  . \
		  lighthouse:/home/ubuntu/lighthouse_service
