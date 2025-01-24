# Django, Django ORM, DRF

## Django

### Жизненный цикл запроса в Django

1. **Получение запроса**.
   Django получает HTTP-запрос от WSGI-сервера (например, Gunicorn или uWSGI). WSGI-сервер передает запрос в виде объекта HttpRequest.
2. **Обработка middleware**.
   Django проходит через цепочку middleware в порядке, заданном в MIDDLEWARE. Каждый middleware может модифицировать запрос или ранний ответ.
3. **URL Routing**.
   Запрос передается в URLconf, где определяется, какая view-функция должна обработать запрос. Выбор происходит на основе urlpatterns.
4. **View-функция**.
   Назначенная view-функция получает запрос, обрабатывает его (обычно с использованием моделей и шаблонов) и возвращает объект HttpResponse.
5. **Обработка ответа middleware**.
   Возвращаемый объект HttpResponse снова проходит через цепочку middleware (обратный порядок).
6. **Формирование HTTP-ответа**.
   Django передает обработанный HttpResponse обратно в WSGI-сервер, который отправляет его клиенту.

### Что такое middleware и как написать свое?

Middleware — это обработчики, которые оборачивают запрос и ответ. Они позволяют перехватывать и изменять запросы и ответы глобально.

#### Пример работы. Логирование запросов, добавление заголовков, проверка авторизации

Создание кастомного middleware:

```python
from django.utils.deprecation import MiddlewareMixin

class SimpleLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"Запрос: {request.method} {request.path}")

    def process_response(self, request, response):
        print(f"Ответ: {response.status_code}")
        return response
```

Добавляем этот middleware в MIDDLEWARE:

```python

MIDDLEWARE = [
    ...
    'myapp.middleware.SimpleLogMiddleware',
]
```

#### Чем отличаются @property и @cached_property?

#### @property

Позволяет превратить метод в атрибут, который вычисляется при каждом доступе.

Пример:

```python
class MyModel:
    @property
    def computed_value(self):
        return expensive_calculation()
```

#### @cached_property

Вычисляет значение только один раз и кэширует его для текущего экземпляра.

Пример:

```python
from django.utils.functional import cached_property

class MyModel:
    @cached_property
    def cached_value(self):
        return expensive_calculation()
```

Разница:

- @property вычисляется при каждом вызове.
- @cached_property кэширует результат.

### Что такое QuerySet? Как работают ленивые вычисления?

QuerySet — это объект, представляющий запрос к базе данных. Он не выполняется до тех пор, пока не потребуется результат.

#### Ленивые вычисления

-Запросы не выполняются при создании QuerySet. Выполнение происходит только при:

- Итерации по QuerySet.
- Преобразовании в список (e.g., list(qs)).
- Вызове методов, возвращающих данные (.count(), .exists(), и т.д.).

Пример:

```python
# QuerySet создан, но запрос не выполнен
qs = MyModel.objects.filter(active=True)
# Выполнение запроса
for obj in qs:
    print(obj.name)

```

## Django ORM

### Как сделать джойны в Django ORM?

Django делает JOIN автоматически при использовании связанных моделей:

```python
# JOIN по ForeignKey
qs = Book.objects.filter(author__name='John')
# JOIN по ManyToManyField
qs = Book.objects.filter(categories__name='Fiction')
```

### Что такое select_related и prefetch_related? Когда их использовать?

#### select_related

- Используется для ForeignKey/OneToOneField.
- Выполняет SQL JOIN для загрузки связанных объектов.
- Ускоряет доступ к связанным данным.

```python
qs = Book.objects.select_related('author').all()
```

#### prefetch_related

- Используется для ManyToManyField.
- Выполняет отдельный SQL-запрос для связанных объектов.

```python
qs = Book.objects.prefetch_related('categories').all()
```

## Django REST Framework

### Как настроить аутентификацию и авторизацию?

Настройка аутентификации через **DEFAULT_AUTHENTICATION_CLASSES**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Пример токен-аутентификации:

```bash
pip install djangorestframework-simplejwt
```

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Что такое ViewSet и как он упрощает разработку?

ViewSet — это класс, который объединяет логику CRUD в одном месте. Вместо написания отдельных view-функций, используется ViewSet с маршрутизацией.

```python
from rest_framework.viewsets import ModelViewSet

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

Подключение через router:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
urlpatterns += router.urls
```

### Разница между GenericAPIView и View?

- View: Базовый класс для создания кастомных API.
- GenericAPIView: Расширяет View и добавляет удобства, такие как queryset, serializer_class.

Пример использования GenericAPIView:

```python
from rest_framework.generics import GenericAPIView

class BookListView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)
```

### Как настроить пагинацию?

Пример настройки:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## Практические задачи

### Как сделать кастомный декоратор или middleware для API?

Пример декоратора:

```python
from functools import wraps
from rest_framework.response import Response

def check_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if request.user.role != role:
                return Response({"error": "Access Denied"}, status=403)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
```

### Как реализовать API, которое возвращает данные в зависимости от роли пользователя?

Пример:

```python
class RoleBasedViewSet(ModelViewSet):
    queryset = DataModel.objects.all()
    serializer_class = DataSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        return self.queryset.filter(owner=user)
```
