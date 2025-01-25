# Асинхронность

## 1. Как интегрировать асинхронные фреймворки (например, FastAPI) с Django?

### Проблема

Django в основном синхронный, а асинхронные фреймворки (например, FastAPI) используют asyncio. Если нужно использовать их вместе, можно обернуть один фреймворк в другой.

### Решение

Django-сервер + FastAPI:

- Используй ASGI-совместимый сервер (например, Daphne или Uvicorn).
- Настрой маршрутизацию так, чтобы FastAPI обрабатывал часть запросов.

### Пример

```python
from fastapi import FastAPI
from django.core.asgi import get_asgi_application
from fastapi.middleware.wsgi import WSGIMiddleware

# Инициализация FastAPI
app = FastAPI()

@app.get("/fastapi-route")
async def fastapi_route():
    return {"message": "FastAPI works"}

# Интеграция с Django
django_app = get_asgi_application()
app.mount("/django", WSGIMiddleware(django_app))
```

### Асинхронный Django

Django с версии 3.1 поддерживает асинхронные views, middlewares и consumers.

## 2. Задача: Написать асинхронный consumer для вебсокетов (Django Channels)

**Шаг 1: Установить Django Channels**

```bash
pip install channels
```

**Шаг 2: Настроить ASGI-сервер**

В settings.py добавить:

```python
INSTALLED_APPS += ["channels"]
ASGI_APPLICATION = "your_project.asgi.application"
```

**Шаг 3: Создать файл asgi.py**

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from your_app.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
```

**Шаг 4: Настроить маршруты для вебсокетов**

В your_app/routing.py:

```python
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
]
```

**Шаг 5: Написать consumer**

В your_app/consumers.py:

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        # Подключение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()  # Подтверждение соединения

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получение данных от клиента
        data = json.loads(text_data)
        message = data["message"]

        # Отправка сообщения группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения обратно клиенту
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
```

**Шаг 6: Настроить Redis для каналов**

Установить Redis и библиотеку:

```bash
pip install channels-redis
```

В settings.py:

```python
CHANNEL_LAYERS = {
    "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
        "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```
