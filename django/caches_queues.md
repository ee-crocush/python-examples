# Кэширование и очереди

## 1. Механизмы кэширования: Redis, Memcached

### Redis

Redis — это in-memory хранилище данных, которое поддерживает различные структуры данных (строки, хэши, списки, множества и т.д.). Redis обычно используется для кэширования данных, хранения сессий, очередей и Pub/Sub сообщений. Он является более мощным и функциональным, чем Memcached.

Преимущества Redis:

- Поддержка различных типов данных.
- Поддержка долговременных данных (сроки хранения данных).
- Высокая скорость операций.
- Возможности для работы с очередями, подпиской/публикацией и т.д.

### Memcached

Memcached — это высокоскоростной кэш для хранения небольших объектов (строки, числа и т.д.), используемый в основном для кэширования данных, таких как запросы к базе данных или результаты вычислений.

- Преимущества Memcached:
- Очень быстрый.
- Хорошо подходит для простого кэширования значений (например, кэширование результатов запросов).
- Очень прост в использовании.

## 2. Как настроить кэширование в Django? Чем отличаются FileBasedCache, LocMemCache и RedisCache?

Django поддерживает несколько механизмов кэширования, таких как FileBasedCache, LocMemCache и RedisCache. Рассмотрим их подробнее:

### FileBasedCache

FileBasedCache — кэширование с использованием файловой системы. Каждый элемент кэша сохраняется в отдельном файле.

Настройка в settings.py:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/path/to/cache/directory', # Укажите путь к директории для хранения кэша
    }
}
```

- Преимущества: Работает без дополнительных зависимостей, подойдет для небольших проектов.
- Недостатки: Не так быстро и масштабируемо, как другие механизмы.

### LocMemCache

LocMemCache — кэширование в памяти, ограниченное только текущим процессом (не распределенное). Это кэширование происходит в оперативной памяти вашего веб-сервера.

Настройка в settings.py:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

- Преимущества: Очень быстрый доступ, подходит для небольших проектов, где нет необходимости в распределенном кэшировании.
- Недостатки: Данные теряются при перезапуске сервера. Не масштабируется для больших приложений.

### RedisCache

RedisCache — кэширование с использованием Redis. Это самое популярное решение для кэширования в Django, поддерживающее распределенные кэши.

Настройка в settings.py:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1', # Адрес и номер базы данных Redis
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

- Преимущества: Высокая производительность, поддержка распределенного кэширования, долговечность данных.
- Недостатки: Требует установки Redis.

## 3. Как работать с очередями? Как настроить Celery с Django?

### Что такое очереди?

Очереди задач используются для асинхронного выполнения длительных операций. Вместо того чтобы блокировать запрос пользователя при обработке сложной задачи (например, отправка email, обработка изображений), можно поместить задачу в очередь, и выполнить её асинхронно.

### Celery

Celery — это популярный фреймворк для распределенных очередей в Python. Он позволяет запускать асинхронные задачи и обрабатывать их в фоновом режиме.

#### Установка Celery

Для начала нужно установить сам Celery и брокер сообщений (например, Redis):

```bash
pip install celery redis
```

#### Настройка Celery в Django

Создание файла celery.py в корне проекта:

```python
from **future** import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройку Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Используем настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()
```

Настройка в settings.py:

```python
# Настройки для Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0' # Указываем Redis как брокер
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

#### Создание задач (tasks)

В каждом приложении можно создавать задачи. Например, в приложении myapp создаем файл tasks.py:

```python
from celery import shared_task

@shared_task
def send_welcome_email(user_email): # Логика отправки email
    print(f"Sending welcome email to {user_email}")
```

#### Запуск Celery

Для запуска Celery необходимо выполнить команду:

```bash
celery -A your_project worker --loglevel=info
```

#### Пример вызова задачи из Django

```python
from myapp.tasks import send_welcome_email

# Вызов асинхронной задачи
send_welcome_email.delay('user@example.com')
```

## 4. Практическая задача: как реализовать задачу, которая будет выполняться раз в день?

Для выполнения задач по расписанию в Celery можно использовать расширение Celery Beat, которое позволяет запускать задачи по расписанию (например, каждый день).

### Установка Celery Beat

```bash
pip install celery[redis] django-celery-beat
```

### Настройка Celery Beat

Добавьте Celery Beat в INSTALLED_APPS в settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

### Создание задачи для выполнения раз в день

Например, создадим задачу, которая будет выполняться каждый день:

```python
from celery import shared_task

@shared_task
def daily_task():
    print("Задача выполнена!")
```

### Настройка расписания с Celery Beat

В settings.py добавляем настройки для CELERY_BEAT_SCHEDULE, чтобы задача выполнялась раз в день:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'daily-task': {
        'task': 'myapp.tasks.daily_task',
        'schedule': crontab(minute=0, hour=0), # Выполнять каждый день в полночь
    },
}
```

### Запуск Celery Beat

Celery Beat работает в отдельном процессе. Для его запуска используем команду:

```bash
celery -A your_project beat --loglevel=info
```

Теперь задача daily_task будет выполняться каждый день в полночь.

## Заключение

- Кэширование в Django может быть настроено с использованием различных бекендов, таких как FileBasedCache, LocMemCache, и RedisCache. Redis является предпочтительным вариантом для распределенного кэширования.
- Celery позволяет эффективно обрабатывать фоновые задачи и работает с брокерами сообщений, такими как Redis. Для периодических задач можно использовать Celery Beat, чтобы настроить выполнение задач по расписанию.
- Эти механизмы кэширования и очереди помогают улучшить производительность и разделить нагрузку на систему, выполняя ресурсоемкие операции в фоне.
