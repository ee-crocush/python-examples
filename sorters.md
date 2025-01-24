## Сортировка

### Вариант 1 с sorted

```python
data = [5, 2, 9, 1, 5, 6]
sorted_data = sorted(data) # [1, 2, 5, 5, 6, 9]

# Сортировка строк по длине

words = ['apple', 'banana', 'pear', 'kiwi']
sorted_words = sorted(words, key=len) # ['pear', 'kiwi', 'apple', 'banana']

# Обратная сортировка

reverse_data = sorted(data, reverse=True) # [9, 6, 5, 5, 2, 1]

print(sorted_data)
print(sorted_words)
print(reverse_data)
print(20 \* '-')

# sorted лямбы

data = [
{'name': 'Alice', 'score': 90},
{'name': 'Bob', 'score': 85},
{'name': 'Charlie', 'score': 95},
]

sorted_data = sorted(data, key=lambda x: x['name'], reverse=True)
print(sorted_data)
print(20 \* '-')
```

### Вариант 2 с sort - для списков

```python
data = [5, 2, 7, 1, 5, 6]
data.sort() # Список изменён: [1, 2, 5, 5, 6, 7]

# Обратная сортировка

data.sort(reverse=True) # [7, 6, 5, 5, 2, 1]

# Сортировка с использованием key

words = ['apple', 'banana', 'pear', 'kiwi']
words.sort(key=len) # ['pear', 'kiwi', 'apple', 'banana']

print(data)
print(words)
print(20 \* '-')
```

### Вариант 3. bisect для поддержания сортированного списка

Модуль bisect полезен для работы с отсортированными списками, чтобы быстро находить место вставки элементов.

```python
import bisect

data = [1, 2, 4, 5]
bisect.insort(data, 3) # Вставляет элемент 3 в нужное место
print(data) # [1, 2, 3, 4, 5]
```
