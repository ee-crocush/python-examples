# Пишем чат на Django

## Шаг 1: Установка зависимостей

```bash
pip install django channels
```

## Шаг 2: Создание проекта и приложения

Создаем проект Django:

```bash
django-admin startproject chat_project
cd chat_project
```

Создаем приложение chat:

```bash
python manage.py startapp chat
```

## Шаг 3: Настройка Channels и базы данных

В settings.py добавляем следующие настройки:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'chat', # Наше приложение
]
```

Указываем ASGI-приложение:

```python
ASGI_APPLICATION = 'chat_project.asgi.application'
```

Настройки для каналов:

```python
CHANNEL_LAYERS = {
    'default': {
    'BACKEND': 'channels.layers.InMemoryChannelLayer', # Для локальной разработки
    },
}
```

В chat_project/asgi.py создаём настройки ASGI:

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
```

## Шаг 4: Создание модели для сообщений

В chat/models.py создаём модель для сообщений чата:

```python
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"
```

Применяем миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Шаг 5: Создание Consumer для чата

В chat/consumers.py создаём ChatConsumer для обработки WebSocket-сообщений, а также добавляем пагинацию:

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from django.core.paginator import Paginator

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        # Отправка истории сообщений при подключении
        self.page_number = 1  # Начинаем с первой страницы
        messages = await self.get_chat_history()

        # Отправляем сообщения при подключении
        for message in messages:
            await self.send_message(message)

        # Присоединяем пользователя к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def get_chat_history(self):
        # Получаем сообщения с учетом пагинации
        all_messages = await database_sync_to_async(ChatMessage.objects.all().order_by('-timestamp'))()
        paginator = Paginator(all_messages, 10)
        page = paginator.page(self.page_number)
        return page.object_list

    async def receive(self, text_data):
        # Получаем сообщение от клиента
        text_data_json = json.loads(text_data)

        if 'message' in text_data_json:
            message = text_data_json["message"]

            # Сохраняем сообщение в базу данных
            user = await self.get_user_from_channel()  # Получаем пользователя
            chat_message = ChatMessage(user=user, message=message)
            chat_message.save()

            # Отправляем сообщение группе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": user.username,
                    "message": message,
                    "timestamp": chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
        elif 'load_more' in text_data_json:
            # Если пользователь прокручивает чат, запрашиваем больше сообщений
            self.page_number += 1  # Загружаем следующую страницу
            messages = await self.get_chat_history()

            # Отправляем старые сообщения
            for message in messages:
                await self.send_message(message)

    async def chat_message(self, event):
        # Получаем сообщение от группы
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp,
        }))

    async def send_message(self, message):
        # Отправляем одно сообщение
        await self.send(text_data=json.dumps({
            "message": message.message,
            "username": message.user.username,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }))

    async def get_user_from_channel(self):
        # Получение пользователя по каналу (используем аутентификацию)
        return self.scope["user"]  # Получаем пользователя из WebSocket
```

## Шаг 6: Создание маршрутов WebSocket

В chat/routing.py добавляем маршрут для WebSocket:

```python
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
]
```

## Шаг 7: Настройка аутентификации пользователей

В settings.py настроим аутентификацию пользователей:

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Используем стандартную аутентификацию
]
```

В chat/views.py создаём представление для страницы чата и аутентификации:

```python
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
return redirect('login')

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat/chat.html')
```

В chat/urls.py добавляем маршруты для входа и чата:

```python
from django.urls import path
from .views import chat_view, login_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chat_view, name='chat'),
]
```

## Шаг 8: Создание HTML-шаблонов

Создаём шаблон для входа: chat/templates/chat/login.html

```html
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<title>Login</title>
	</head>
	<body>
		<h1>Login</h1>
		<form method="post">
			{% csrf_token %} {{ form.as_p }}
			<button type="submit">Login</button>
		</form>
	</body>
</html>
```

Создаём шаблон для чата: chat/templates/chat/chat.html

```html
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<title>Chat</title>
		<script>
			document.addEventListener('DOMContentLoaded', () => {
				const chatSocket = new WebSocket(
					'ws://' + window.location.host + '/ws/chat/'
				)

				chatSocket.onmessage = (e) => {
					const data = JSON.parse(e.data)
					const message = data.message
					const username = data.username
					const timestamp = data.timestamp

					const chatLog = document.getElementById('chat-log')
					const newMessage = document.createElement('div')
					newMessage.textContent = `${username} (${timestamp}): ${message}`
					chatLog.appendChild(newMessage)

					// Автопрокрутка в самый низ при отправке сообщений
					chatLog.scrollTop = chatLog.scrollHeight
				}

				chatSocket.onclose = () => {
					console.error('Chat socket closed unexpectedly')
				}

				document.getElementById('chat-message-submit').onclick = () => {
					const messageInput = document.getElementById('chat-message-input')
					const message = messageInput.value
					chatSocket.send(JSON.stringify({ message }))
					messageInput.value = ''
				}

				// Прокрутка в самый верх
				const chatLog = document.getElementById('chat-log')
				chatLog.addEventListener('scroll', () => {
					if (chatLog.scrollTop === 0) {
						// Если пользователь прокрутил в верхний край, запрашиваем старые сообщения
						chatSocket.send(JSON.stringify({ load_more: true }))
					}
				})
			})
		</script>
	</head>
	<body>
		<h1>Chat</h1>
		<div
			id="chat-log"
			style="border: 1px solid #000; height: 300px; overflow-y: scroll; padding: 10px;">
			<!-- Сообщения будут добавляться сюда -->
		</div>
		<input
			id="chat-message-input"
			type="text"
			placeholder="Введите сообщение" />
		<button id="chat-message-submit">Отправить</button>
	</body>
</html>
```

## Шаг 9: Запуск проекта

```bash
python manage.py runserver
```

Переходим по URL http://127.0.0.1:8000/login/ и логинемся

Открываем страницу чата и радуемся http://127.0.0.1:8000/chat/
