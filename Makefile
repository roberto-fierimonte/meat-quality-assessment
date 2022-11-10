#!make
-include .env
export

help: ## Display this help screen
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pre-commit: ## Run the pre-commit over the entire repo
	@poetry run pre-commit run --all-files

download-data: ## Downloads the dataset inside the `data` folder
	@poetry run python -m src.scripts.download_data

build-image: ## Build the Docker image locally
	@docker build --tag meat-quality-assessment -f ./containers/Dockerfile .

push-image: ## Push the Docker image to the container registry (must have a Dockerhub account and a repository for the project)
	@ $(MAKE) build-image && \
	docker tag meat-quality-assessment ${DOCKERHUB_USERNAME}/meat-quality-assessment && \
	docker push ${DOCKERHUB_USERNAME}/meat-quality-assessment

run-server: ## Run the REST API server in a Docker container
	@ $(MAKE) build-image && \
	docker run --rm -it -p 8080:8080 -v "${PROJ_DIR}/model":/opt/app/model meat-quality-assessment \
	--config=./src/serving_api/config.py

run-server-local: ## Run the REST API server locally
	@poetry run python -m gunicorn src.serving_api.app:app --config=./src/serving_api/config.py

test-api: ## Send a request to the API. Must specify a file name with image=<$file-name>
	@curl -X POST -F "image=@$(image)" http://localhost:8080/predict
