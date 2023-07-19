APP_VERSION ?= v0.1.0
IMAGE_REGISTRY ?= quay.io/opstree
IMAGE_NAME ?= attendance-api

# Build employee binary
build: fmt
	poetry config virtualenvs.create false
	poetry install --no-root --no-interaction --no-ansi

# Run go fmt against code
fmt:
	pylint router/ client/ models/ utils/ app.py

docker-build:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION} -f Dockerfile .

docker-push:
	docker push ${IMAGE_REGISTRY}/${IMAGE_NAME}:${APP_VERSION}

run-migrations:
	liquibase update --driver-properties-file=liquibase.properties
