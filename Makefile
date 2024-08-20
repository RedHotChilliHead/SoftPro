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

# Линтинг с использованием pylint
lint:
	@pylint ./SoftPro
