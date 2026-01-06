.PHONY: help build up down logs clean rebuild test-index test-post

SLUG ?= post
ENV ?= prod

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	cd local_env && \
	docker-compose build

up: ## Start all services
	cd local_env && \
	docker-compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "🌐 Access the application at: http://localhost:8080"
	@echo "📝 View logs with: make logs"

down: ## Stop all services
	cd local_env && \
	docker-compose down

logs: ## Show logs from all services
	cd local_env && \
	docker-compose logs -f

clean: ## Remove containers, networks, and volumes
	cd local_env && \
	docker-compose down -v
	docker system prune -f

rebuild: clean build up ## Clean rebuild and restart

test-index: ## Test index Lambda directly
	@echo "Testing index Lambda..."
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

test-post: ## Test post Lambda directly (example slug: sample-post)
	@echo "Testing post Lambda..."
	curl -XPOST "http://localhost:9001/2015-03-31/functions/function/invocations" \
		-d '{"pathParameters":{"slug":"$(SLUG)"}}'

test-nginx: ## Test through Nginx (full stack)
	@echo "Testing index through Nginx..."
	curl -s http://localhost:8080/ | head -20
	@echo ""
	@echo "Testing post through Nginx..."
	curl -s http://localhost:8080/post/${SLUG} | head -20

login:
	aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 987608117561.dkr.ecr.sa-east-1.amazonaws.com

deploy: ## Deploy to AWS (requires AWS CLI configured)
	cd src && \
	docker buildx build -f Dockerfile --build-arg LAMBDA_FILE=lambda_index.py --build-arg STAGE=$(ENV) --platform linux/amd64 --provenance=false -t root:$(ENV) . && \
	docker buildx build -f Dockerfile --build-arg LAMBDA_FILE=lambda_post.py --build-arg STAGE=$(ENV) --platform linux/amd64 --provenance=false -t post:$(ENV) . && \
	docker tag root:$(ENV) 987608117561.dkr.ecr.sa-east-1.amazonaws.com/root:$(ENV) && \
	docker tag post:$(ENV) 987608117561.dkr.ecr.sa-east-1.amazonaws.com/post:$(ENV) && \
	docker push 987608117561.dkr.ecr.sa-east-1.amazonaws.com/root:$(ENV) && \
	docker push 987608117561.dkr.ecr.sa-east-1.amazonaws.com/post:$(ENV)
	aws lambda update-function-code --function-name root --image-uri 987608117561.dkr.ecr.sa-east-1.amazonaws.com/root:$(ENV)
	aws lambda update-function-code --function-name post-$(ENV) --image-uri 987608117561.dkr.ecr.sa-east-1.amazonaws.com/post:$(ENV)
	@echo "✅ Deployment complete!"
