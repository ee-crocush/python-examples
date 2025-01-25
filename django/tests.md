# Тесты

## 1. Тесты: юнит, интеграционные, функциональные

### Юнит-тесты

Юнит-тесты проверяют отдельные компоненты системы в изоляции. Например, проверка одной функции или метода без взаимодействия с внешними сервисами (например, базой данных, API).

Пример юнит-теста:

```python
def test_addition():
    result = add(2, 3)
    assert result == 5
```

Здесь мы тестируем функцию add — это простой юнит-тест, который проверяет только логику сложения чисел.

### Интеграционные тесты

Интеграционные тесты проверяют, как несколько компонентов взаимодействуют друг с другом. В случае Django это может быть тестирование работы нескольких частей системы, например, базы данных и логики приложения.

Пример интеграционного теста:

```python
from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username='john', email='john@example.com')
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@example.com')
```

Здесь тестируется создание пользователя в базе данных, и проверяется, что данные правильно сохраняются и извлекаются.

### Функциональные тесты

Функциональные тесты проверяют весь процесс или сценарий, как он будет работать с точки зрения пользователя. Это включает в себя тестирование API, пользовательских интерфейсов, а также других важных аспектов работы системы.

Пример функционального теста:

```python
from rest_framework.test import APIClient
from django.urls import reverse

def test_user_api():
    client = APIClient()
    url = reverse('user-list')
    response = client.get(url)
    assert response.status_code == 200
```

Здесь мы тестируем работу API через клиент Django Rest Framework (DRF). Проверяется правильность ответа от API.

## 2. Как тестировать API? Примеры с использованием pytest или Django TestCase

### Пример с использованием pytest и pytest-django

Установка зависимостей:

```bash
pip install pytest pytest-django
```

Пример теста с использованием pytest:

```python
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_creation():
    client = APIClient()
    url = reverse('user-list') # URL для создания пользователя
    data = {'username': 'john', 'email': 'john@example.com', 'password': 'password123'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == 'john'
    assert 'password' not in response.data  # Проверяем, что пароль не вернулся в ответе
```

Здесь используется pytest для тестирования API. Мы создаем пользователя с помощью POST-запроса и проверяем статус и данные ответа.

### Пример с использованием Django TestCase

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'john', 'email': 'john@example.com', 'password': 'password123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'john')
        self.assertNotIn('password', response.data)
```

Здесь используется Django TestCase, который предоставляет встроенную поддержку для тестирования Django-приложений, включая тестирование API.

## 3. Как замокать внешний сервис (например, запросы через requests или httpx)?

Иногда при тестировании необходимо замокать запросы к внешним сервисам, чтобы избежать реальных вызовов. Для этого удобно использовать библиотеки, такие как unittest.mock или pytest-mock.

### Пример мокирования с pytest-mock

Предположим, у нас есть код, который делает HTTP-запрос:

```python
import requests

def get_weather(city):
    response = requests.get(f'http://weatherapi.com/{city}')
    return response.json()
```

Чтобы замокать этот запрос в тестах:

```python
import pytest
from unittest.mock import MagicMock
from myapp import get_weather

@pytest.mark.parametrize('city,expected', [
    ('London', {'temp': 15}),
    ('Moscow', {'temp': -5}),
])
def test_get_weather(mocker, city, expected):
    mock_response = MagicMock()
    mock_response.json.return_value = expected
    mocker.patch('requests.get', return_value=mock_response)

    result = get_weather(city)
    assert result == expected
```

Здесь мы использовали pytest-mock для замены реального запроса на мок, чтобы возвращать заранее заданные данные.

## 4. Как использовать фикстуры в pytest?

Фикстуры в pytest используются для подготовки и очистки данных или состояния перед тестом. Они позволяют повторно использовать код подготовки, например, создание объектов в базе данных.

Пример фикстуры:

```python
import pytest
from myapp.models import User

@pytest.fixture
def user():
    user = User.objects.create(
        username='john', email='john@example.com')
    return user

def test_user(user):
    assert user.username == 'john'
    assert user.email == 'john@example.com'
```

Здесь мы создаём фикстуру user, которая создает объект пользователя, и используем её в тестах. Фикстуры позволяют эффективно управлять состоянием данных для тестов.
