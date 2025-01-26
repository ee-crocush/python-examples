# Пример простого приложения на FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, mapped
from sqlalchemy import String, Integer
from pydantic import BaseModel

# Настройки базы данных
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db_name"
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(
    bind=engine,  # Используем созданный движок
    autoflush=False,  # Отключаем автоматический сброс
    expire_on_commit=False,  # Отключаем устаревание данных после коммита
)

# Зависимость для получения сессии
async def get_db():
    async with async_session() as session:
        yield session

# Модель SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id: mapped[int] = mapped(Integer, primary_key=True, index=True)
    name: mapped[str] = mapped(String(100), index=True)
    email: mapped[str] = mapped(String(100), unique=True, index=True)

# Pydantic-схемы
class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Инициализация приложения
app = FastAPI()

# Создание таблиц при запуске
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Эндпоинт для создания пользователя
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Эндпоинт для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```
