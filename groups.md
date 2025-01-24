## Группировка

### 1. Использование itertools.groupby

Модуль itertools предоставляет функцию groupby, которая группирует соседние элементы, если они идут подряд в отсортированном порядке.

Важно: Данные нужно отсортировать перед использованием groupby.

```python
from itertools import groupby

# Группировка чисел

data = [1, 1, 2, 2, 2, 3, 4, 4, 5]
grouped = groupby(data)

for key, group in grouped:
print(f'{key}: {list(group)}')

print(20 \* '-')

# Пример с объектами:

data = [
{'name': 'Alice', 'age': 25},
{'name': 'Bob', 'age': 30},
{'name': 'Charlie', 'age': 25},
{'name': 'Diana', 'age': 30},
]

# Сортировка по ключу для корректной работы groupby

sorted_data = sorted(data, key=lambda x: x['age'])

grouped = groupby(sorted_data, key=lambda x: x['age'])
for age, group in grouped:
print(f'Age {age}: {[item["name"] for item in group]}')

print(20 \* '-')
```

### 2. Использование collections.defaultdict

Если данные не отсортированы, можно сгруппировать их, используя словарь.

```python
from collections import defaultdict

data = [('Alice', 'A'), ('Bob', 'B'), ('Charlie', 'A'), ('Diana', 'B')]

grouped = defaultdict(list)
for name, group in data:
grouped[group].append(name)

print(grouped)

# Пример с подсчётом групп

data = [1, 2, 2, 3, 3, 3, 4]
grouped = defaultdict(int)

for num in data:
grouped[num] += 1

print(grouped)
print(20 \* '-')
```

### 3. Группировка вручную через словарь

Если не хочется использовать дополнительные библиотеки, можно написать свою логику.

```python
data = [
('apple', 'fruit'),
('carrot', 'vegetable'),
('banana', 'fruit'),
('spinach', 'vegetable'),
]

grouped = {}
for item, category in data:
if category not in grouped:
grouped[category] = []
grouped[category].append(item)

print(grouped)
```
