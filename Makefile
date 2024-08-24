# Переменные для хранения команд
DOCKER_COMPOSE=docker compose

# Запустить проект
.PHONY: run
run:
	docker volume create sports_lines_postgres_data && $(DOCKER_COMPOSE) up -d && docker compose run django_http_app python manage.py migrate

# Остановить проект
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) down

# Линтинг с использованием pylint
.PHONY: lint

lint:
	@echo "Running pylint..."
	export DJANGO_SETTINGS_MODULE=SoftPro.settings && pylint --disable=C0413,C0415,W0613 ./soft_pro

# Запустить тестирование
.PHONY: test
test:
	$(DOCKER_COMPOSE) up -d && $(DOCKER_COMPOSE) run django_http_app python manage.py test && $(DOCKER_COMPOSE) down
