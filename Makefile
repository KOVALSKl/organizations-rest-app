SRC_DIR = $(shell pwd)
COMPOSE_FILE = $(SRC_DIR)/docker-compose.yaml

build:
	$(DC) build $(c) \
	&& mkdir -p docker/coverage docker/logs \
	&& chmod 777 docker/coverage docker/logs

install_deps:
pip install -r requirements.txt
install_dev_deps:
	pip install -r dev_requirements.txt
lint:
	flake8 app
	mypy app
run:
	python -m uvicorn app.main:application  --port 8000 --host 0.0.0.0
dev:
	python -m uvicorn app.main:application --reload --port 8001 --host 0.0.0.0
docker_run:
	docker compose up -d --build
start:
	docker compose -f backend/docker-compose.dev.yaml up
stop:
	docker compose -f backend/docker-compose.dev.yaml down
cont:
	docker exec -it russpass_mag_backend_1 bash