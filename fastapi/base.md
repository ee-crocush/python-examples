# База по FastAPI

## 1. Что такое FastAPI, и в чем его преимущества?

FastAPI — это асинхронный фреймворк для создания API, построенный на базе Starlette для работы с запросами и Pydantic для валидации данных. Основные преимущества FastAPI включают:

- Высокая производительность, сравнимая с Node.js и Go, благодаря использованию асинхронных операций.
- Автоматически генерируемая документация через OpenAPI, что упрощает тестирование и интеграцию.
- Типизация данных с помощью Pydantic, что улучшает читаемость кода и уменьшает количество ошибок.
- Поддержка асинхронности из коробки, что позволяет обрабатывать множество запросов одновременно без блокировки.

Пример асинхронного маршрута:

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # асинхронная работа с базой данных или API
    return {"item_id": item_id}
```

## 2. Для чего используется Pydantic в FastAPI?

Pydantic в FastAPI используется для валидации и сериализации данных. Когда запрос приходит в FastAPI, Pydantic автоматически проверяет данные на соответствие схемам, используя аннотации типов. Это позволяет значительно сократить количество ошибок и делает код более поддерживаемым. Pydantic также генерирует схемы для API, которые автоматически используются для документации.

Пример использования Pydantic:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

## 3. Что такое Dependency Injection в FastAPI?

Dependency Injection (DI) — это принцип, при котором зависимости (например, объекты или сервисы) передаются в функции, а не создаются внутри них. В FastAPI DI позволяет легко управлять зависимостями, такими как базы данных, кэш, или другие сервисы. Это улучшает тестируемость, читаемость и поддержку кода. В FastAPI DI реализуется через параметр Depends, который позволяет инжектировать зависимости в функции-обработчики.

Пример с DI для работы с базой данных:

```python
from fastapi import Depends

# Настройки базы данных
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db_name"
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(
    bind=engine,  # Используем созданный движок
    autoflush=False,  # Отключаем автоматический сброс
    expire_on_commit=False,  # Отключаем устаревание данных после коммита
)
async def get_db():
    async with async_session() as session:
        yield session

@app.post("/items/")
async def create_item(item: Item, db: Session = Depends(get_db)):
    db.add(item)
    db.commit()
    return {"message": "Item created"}
```

## 4. Как настроить аутентификацию через JWT в FastAPI?

FastAPI поддерживает JWT (JSON Web Tokens) для аутентификации пользователей. JWT обычно используется для того, чтобы удостовериться, что запрос приходит от авторизованного пользователя, и передает информацию в виде токена. В FastAPI для работы с JWT можно использовать библиотеку pyjwt. Также можно создать зависимость, которая будет проверять токен в каждом запросе.

Пример с аутентификацией JWT:

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
```

## 5. Как работает SQLAlchemy в асинхронных приложениях?

SQLAlchemy поддерживает асинхронность начиная с версии 1.4. Для асинхронной работы необходимо использовать AsyncSession и create_async_engine, а также писать запросы с await. Это позволяет выполнять операции с базой данных без блокировки основной программы, что особенно полезно в высоконагруженных приложениях. Для асинхронной работы с базой данных нужно использовать драйверы, поддерживающие асинхронность, например asyncpg для PostgreSQL.

Пример асинхронного запроса:

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return user
```

## 6. Что такое middleware в FastAPI?

Middleware в FastAPI — это специальные обработчики, которые выполняются до или после обработки запроса. Они позволяют выполнять глобальные операции, такие как логирование, проверка авторизации или изменение данных запроса и ответа. В FastAPI middleware реализуются с помощью класса, который принимает и обрабатывает запросы и ответы.

Пример middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['X-Custom-Header'] = 'Hello World'
        return response

app.add_middleware(CustomMiddleware)
```

## 7. Как тестировать приложение на FastAPI?

Для тестирования приложения на FastAPI можно использовать встроенный клиент TestClient (для синхронных тестов) или httpx.AsyncClient (для асинхронных). Тесты обычно пишутся с использованием библиотеки pytest. С помощью TestClient можно отправлять запросы к серверу, а затем проверять ответы.

Пример теста с использованием TestClient:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    assert response.json() == {"name": "Alice", "email": "alice@example.com"}
```

## 8. Что такое OpenAPI и как его генерирует FastAPI?

OpenAPI — это спецификация для описания RESTful API. FastAPI автоматически генерирует OpenAPI-документацию на основе аннотаций типов и маршрутов. Это позволяет разработчикам и клиентам быстро понять, как работает API. Документация доступна по URL /docs, а также можно получить JSON-спецификацию по URL /openapi.json.

Пример документации OpenAPI:

```python
@app.get("/items/")
async def get_items():
    """
    Get a list of items.
    Returns:
        list: A list of items
    """
    return [{"item_name": "Item 1"}, {"item_name": "Item 2"}]
```

## 9. Как оптимизировать приложение FastAPI?

Оптимизация приложения на FastAPI может включать несколько аспектов: использование асинхронных библиотек для I/O операций, кеширование (например, Redis), использование фоновых задач через BackgroundTasks, а также асинхронную обработку запросов через WebSockets. Пример использования фоновых задач:

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Notification sent")
    return {"message": "Notification is being sent in the background"}
```

## 10. Как настроить асинхронные миграции с Alembic для SQLAlchemy?

Alembic поддерживает асинхронные миграции через asyncpg и SQLAlchemy 1.4. Нужно настроить асинхронный engine и использовать его с Alembic для миграций, чтобы поддерживать асинхронность в приложении.

## 11. Как использовать Pydantic с дополнительными валидаторами?

Pydantic поддерживает использование валидации через методы @root_validator и @validator. Это позволяет добавлять дополнительные проверки и изменять данные перед их сохранением.

Пример с валидатором:

```python
from pydantic import root_validator

class Item(BaseModel):
    name: str
    price: float

    @root_validator
    def check_price(cls, values):
        price = values.get('price')
        if price < 0:
            raise ValueError("Price must be positive")
        return values
```
