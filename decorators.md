## Декораторы

### 1. Декоратор над функциями

В декоратор передаем функцию. Далее в нем обязательно объявляем wrapper (имя стандартное, можно любое). В этом wrapper вызываем функцию. Если функция, для которой будет использоваться декоратор,возвращает значение, то декоратор возращаем результат функции

```python
# decorator возращает wrapper
def decorator(func):
    def wrapper(*args, **kwargs):
        print('Start decorator')
        result = func(*args, **kwargs)
        print('End decorator')
        return result

    return wrapper

# Если фунция ничего не возращает, то можно без return func
def decorator_without_return_result(func):
    def wrapper(*args, **kwargs):
        print('Start decorator')
        func(*args, **kwargs)
        print('End decorator')

    return wrapper


@decorator
def sum_nums(*args) -> int:
    return sum(args)


@decorator
def sum_list(nums: list) -> int:
    return sum(nums)


@decorator
def sum_nums_without_return(*args) -> int:
    print(sum(args))


print('Декоратор над функциями, которые возращают значение')
print(sum_nums(1, 2, 3, 4, 5))
print(sum_list(range(6)))
print(20 * '=')
print('Декоратор над функциями, которые не возращают значение')
sum_nums_without_return(1, 2, 3, 4, 5)
print(20 * '=')

# 2. Декоратор, в который передается значение

def decorator_with_value(value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('Start decorator with value: ', value)
            result = func(*args, **kwargs)
            print('End decorator with value')

            return result

        return wrapper

    return decorator


@decorator_with_value(10)
def some_func(a: int):
    print(f'Йоу, мы вызываем some_func с переменной a: {a}')


some_func(5)
print(20 * '=')
```

### 3. Декоратор для класса

В декоратор передаем cls - это класс, над которым будет работать декоратор. В декораторе создается новый класс Wrapper в него передаем cls, у которого есть **init**. В нем логика декоратора и вызываем super().**init**. класс Wrapper должен вернуть Wrapper

```python
def class_decorator(cls):
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            print('Йоу это декоратор для класса, устанавливаем атрибут a')
            super().__init__(*args, **kwargs)
            setattr(self, 'a', 10)
            print('Декоратор закончил работу')

    return Wrapper


@class_decorator
class SomeClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @decorator
    def some_cls_func(self, *args, **kwargs):
        print('а это some_cls_func')


print('Работаем с классами')
sm = SomeClass(1, 2)
print(sm.a)
sm.some_cls_func()
print(20 * '=')
```
