all:
	docker compose up --build
down:
	docker compose down
all-d:
	docker compose up --build -d
back:
	docker compose up --build manul-db manul-backend
back-d:
	docker compose up --build -d manul-db manul-backend	
clean:
	docker image rm app-manul-backend app-manul-bot postgres:alpine && docker volume rm app_manul-db-volume
