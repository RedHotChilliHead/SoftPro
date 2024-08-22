# Переменные для хранения команд
DOCKER_COMPOSE=docker compose

# Запустить проект
.PHONY: run
run:
	$(DOCKER_COMPOSE) up -d

# Остановить проект
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) down

# Линтинг с использованием pylint
.PHONY: lint

lint:
	@echo "Running pylint..."
	export DJANGO_SETTINGS_MODULE=SoftPro.settings && pylint ./SoftPro

# Запустить тестирование
.PHONY: test
test:
	$(DOCKER_COMPOSE) run django_http_app python manage.py test
