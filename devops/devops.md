# DevOps/Инфраструктура

## 1. Как деплоить проекты на продакшен? Какие инструменты использовать (Docker, Gunicorn, Nginx)?

Основные этапы деплоя Django-проекта на продакшен:

- Подготовка окружения. Выбор сервера. Операционная система: Чаще всего используют Ubuntu или Debian.
- Установка необходимых инструментов:
  - Python: Убедитесь, что установлен Python 3.x.
  - Virtualenv: Создайте изолированное окружение для проекта.
  - PostgreSQL/MySQL: Настройте базу данных.
- Gunicorn: WSGI-сервер для обработки запросов.
- Nginx: Реверс-прокси сервер, работающий перед Gunicorn для управления трафиком.
- Docker (опционально): Используется для контейнеризации приложения.

## 2. Что такое WSGI и ASGI? Чем они отличаются?

WSGI (Web Server Gateway Interface):

- Интерфейс между веб-сервером и Python-приложением.
- Работает только для синхронных приложений.
- Подходит для большинства стандартных Django-проектов.

ASGI (Asynchronous Server Gateway Interface):

- Расширение WSGI, поддерживающее асинхронные операции.
- Используется для приложений, где важна работа с вебсокетами, real-time данными.

Django 3+ поддерживает ASGI.

## 3. Как настроить CI/CD? Пример пайплайна для Django-проекта

CI/CD автоматизирует процесс тестирования, сборки и деплоя.

Инструменты:

- GitHub Actions, GitLab CI/CD, Jenkins, CircleCI.

Пример для GitHub Actions (.github/workflows/django.yml):

```yaml
name: Django CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m venv env
          source env/bin/activate
          pip install -r requirements.txt

      - name: Run tests
        run: |
          source env/bin/activate
          python manage.py test

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to server
        run: |
          ssh user@your-server "cd /path/to/project && git pull && docker-compose up --build -d"
```

Пример Gitlab:

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: registry.gitlab.com/your-namespace/your-project
  DJANGO_SETTINGS_MODULE: my_project.settings
  PYTHONUNBUFFERED: 1

# Шаг 1: Установка зависимостей и тестирование
test:
  stage: test
  image: python:3.10
  services:
    - postgres:latest
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_password
    POSTGRES_HOST: postgres
  before_script:
    - pip install -r requirements.txt
    - python manage.py migrate
  script:
    - python manage.py test

# Шаг 2: Сборка Docker-образа
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE:latest .
    - docker push $DOCKER_IMAGE:latest

# Шаг 3: Деплой на сервер
deploy:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - ssh-keyscan -H your-server.com >> ~/.ssh/known_hosts
  script:
    - ssh user@your-server.com "docker pull $DOCKER_IMAGE:latest && docker-compose -f /path/to/docker-compose.yml up -d"
  only:
    - main
```
