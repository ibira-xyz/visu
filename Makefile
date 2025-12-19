.PHONY: help build up down logs clean rebuild test-index test-post

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
		-d '{"pathParameters":{"slug":"sample-post"}}'

test-nginx: ## Test through Nginx (full stack)
	@echo "Testing index through Nginx..."
	curl -s http://localhost:8080/ | head -20
	@echo ""
	@echo "Testing post through Nginx..."
	curl -s http://localhost:8080/post/sample-post | head -20
