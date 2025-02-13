## dataclasses

@dataclass — это декоратор в Python, который был добавлен в версии 3.7 в модуле dataclasses. Он предназначен для упрощения создания классов, которые используются для хранения данных.

Когда вы используете @dataclass, Python автоматически генерирует для класса стандартные методы, такие как:

- **init** — для инициализации объекта.
- **repr** — для представления объекта в виде строки (удобно для отладки).
- **eq** — для сравнения объектов.
- Другие методы, такие как **lt**, **le**, **gt**, **ge** (если включён параметр order).

@dataclass(order=True) — добавляет методы сравнения (<, <=, >, >=).

@dataclass(frozen=True) — делает объект неизменяемым (вводит поведение, похожее на namedtuple).

@dataclass(init=False) — не генерирует метод **init**.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
    z: int = 0 # Значение по умолчанию

point1 = Point(10, 20)
point2 = Point(10, 20, 30)

print(point1) # Point(x=10, y=20, z=0)
print(point1 == point2) # False, т.к. значения отличаются

print(20 \* '=')

@dataclass(order=True)
class Player:
    score: int
    name: str

# Создаём несколько объектов

player1 = Player(300, 'Alice')
player2 = Player(150, 'Bob')
player3 = Player(100, 'Bannie')

# Сравнение объектов

print(player1 < player2) # False (300 > 150)
print(player2 > player3) # True (150 > 100)
print(player1 == player3) # False (разные значения score)

# Сортировка списка объектов

players = [player1, player2, player3]
sorted_players = sorted(players, key=lambda p: p.name) # Сортировка по name
for player in sorted_players:
    print(player)
```
