# Десприпторы

**Дескриптор** — это объектовый атрибут с поведением, определяемым методами в его классе.

Если просто — это способ, с помощью которого объект может контролировать доступ к его атрибутам,
используя специально определенные методы \_\_get__, \_\_set__, и \_\_delete__.
Если говорить еще проще — дескрипторы позволяют задавать точки доступа к атрибутам объекта,
добавляя дополнительную логику, когда атрибут читается, записывается или удаляется.

## Основные методы

Протокол дескриптора в Python определяется наличием методов \_\_get__, \_\_set__ и \_\_delete__ в классе.
Эти методы позволяют объектам управлять тем, как значения атрибутов извлекаются, устанавливаются или удаляются.
Также существует необязательный метод \_\_set_name__, позволяющий дескриптору узнавать имя атрибута,
к которому он присвоен в классе.

- Метод \_\_get__ вызывается, когда значение атрибута извлекается, он принимает два аргумента: self и instance.
  instance - это экземпляр объекта, через который доступен дескриптор, или None, если обращение идет через класс.
  Возвращаемое значение этого метода будет значением указанного атрибута:

```python
class Descriptor:
    def __get__(self, instance, owner):
        return 'значение'


class MyClass:
    attr = Descriptor()


my_object = MyClass()
print(my_object.attr)  # выведет 'значение'
```

- Метод \_\_set__ позволяет управлять изменением значения атрибута.
  Он принимает три аргумента: self, instance и value, где value - это новое значение атрибута:

```python
class Descriptor:
    def __set__(self, instance, value):
        print(f"Установка значения {value}")
        self.__value = value


class MyClass:
    attr = Descriptor()


my_object = MyClass()
my_object.attr = 10  # выведет 'Установка значения 10'
```

- Метод \_\_delete__ вызывается при удалении атрибута с использованием оператора del.
  Он принимает два аргумента: self и instance:

```python
class Descriptor:
    def __delete__(self, instance):
        print("Удаление атрибута")
        del self.__value


class MyClass:
    attr = Descriptor()


my_object = MyClass()
del my_object.attr  # выведет 'Удаление атрибута'
```

- Необязательный метод \_\_set_name__ вызывается в момент создания класса для каждого дескриптора,
  что позволяет дескриптору знать имя атрибута, к которому он привязан. Этот метод принимает
  два аргумента: self и name, где name - это имя атрибута:

```python
class Descriptor:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, 'еще не установлено')

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)


class MyClass:
    attr = Descriptor()


my_object = MyClass()
print(my_object.attr)  # выведет 'еще не установлено'
my_object.attr = 99
print(my_object.attr)  # выведет 99
```

## Примеры использования

Создадим дескриптор для валидации данных, который будет проверять, что возраст пользователя не может быть отрицательным
числом и не может превышать 100 лет:

```python
class ValidateAge:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("Возраст должен быть между 0 и 100 годами")
        setattr(instance, self.private_name, value)


class Person:
    age = ValidateAge()

    def __init__(self, name, age):
        self.name = name
        self.age = age


try:
    p = Person("Kolya", 30)  # валидный возраст
    print(p.age)
    p.age = -5  # невалидный возраст, будет вызвано исключение ValueError
except ValueError as e:
    print(e)
```

Теперь создадим дескриптор для кэширования результатов тяжелых вычислений. Предположим, есть функция,
выполнение которой занимает значительное время, и нужно кэшировать ее результат для одних и тех же входных данных:

```python
import time


class CachedAttribute:
    def __init__(self, method):
        self.method = method
        self.cache = {}

    def __get__(self, instance, owner):
        if instance not in self.cache:
            self.cache[instance] = self.method(instance)
        return self.cache[instance]


class HeavyComputation:
    @CachedAttribute
    def compute(self):
        time.sleep(2)
        # имитация длительного вычисления
        return "Результат вычисления"


hc = HeavyComputation()
start_time = time.time()
print(hc.compute)  # первый вызов занимает время
print(f"Выполнено за {time.time() - start_time} секунд")

start_time = time.time()
print(hc.compute)  # второй вызов мгновенный, использует кэшированный результат
print(f"Выполнено за {time.time() - start_time} секунд")
```

Создадим дескриптор, который будет логировать любые изменения значений атрибутов:

```python
class LoggedAttribute:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        print(f"Установка {self.private_name} в {value}")
        setattr(instance, self.private_name, value)


class User:
    name = LoggedAttribute()
    age = LoggedAttribute()

    def __init__(self, name, age):
        self.name = name
        self.age = age


u = User("Katya", 30)
u.name = "Katyuha"  # Логируется изменение
u.age = 31  # Логируется изменение
```

## Реализация паттернов Singleton и Factory

### Singleton

Не будем объяснять, зачем нужен паттерн Singleton. Но если коротко, то он гарантирует, что
класс имеет только один экземпляр и предоставляет глобальную точку доступа к этому экземпляру.

Создадим дескриптор Singleton, который будет управлять созданием экземпляров другого класса, гарантируя, что создается
только один экземпляр:

```python
class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __get__(self, instance, owner):
        if self.instance is None:
            self.instance = self.cls()
        return self.instance


class Database:
    def __init__(self):
        print("Создание базы данных")


# применение дескриптора Singleton
class AppConfig:
    db = Singleton(Database)


# тестирование паттерна Singleton
config1 = AppConfig()
config2 = AppConfig()
db1 = config1.db  # создание БД
db2 = config2.db  # не создает новый экземпляр, использует существующий

print(db1 is db2)  # выведет True, подтверждая, что db1 и db2 - один и тот же объект
```

### Factory

**Factory** — это паттерн проектирования, который используется для создания объектов без указания
конкретных классов объектов.

Для реализации этого паттерна можно создать дескриптор, который будет динамически определять, какой объект создавать,
основываясь на каком-либо условии или конфигурации:

```python
class VehicleFactory:
    def __init__(self, cls):
        self.cls = cls

    def __get__(self, instance, owner):
        return self.cls()


class Car:
    def drive(self):
        print("Вождение автомобиля")


class Bike:
    def ride(self):
        print("Езда на велосипеде")


# фабрика, создающая автомобили
class AppConfigCar:
    vehicle = VehicleFactory(Car)


# фабрика, создающая велосипеды
class AppConfigBike:
    vehicle = VehicleFactory(Bike)


# создание и использование автомобиля
car_config = AppConfigCar()
car = car_config.vehicle  # создает объект Car
car.drive()

# создание и использование велосипеда
bike_config = AppConfigBike()
bike = bike_config.vehicle  # создает объект Bike
bike.ride()
```

## Встроенные функции property, classmethod и staticmethod

### Property

**property** - это встроенная функция Python, с ее помощью можно создать атрибут, значение которого
генерируется динамически через методы геттер и сеттер. Юзабельно, когда надо добавить логику валидации
при присвоении значения атрибуту или когда значение атрибута зависит от других атрибутов.

property работает как дескриптор, используя методы __get__, __set__ и __delete__ для управления доступом к атрибуту:

```python
class Celsius:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    def get_temperature(self):
        print("Получение значения")
        return self._temperature

    def set_temperature(self, value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже -273.15 градусов Цельсия")
        print("Установка значения")
        self._temperature = value

    temperature = property(get_temperature, set_temperature)


c = Celsius(37)
print(c.temperature)
c.temperature = -300  # вызовет исключение
```

### classmethod

**classmethod** - это декоратор, который изменяет метод так, что он получает класс (а не экземпляр класса) в качестве
первого аргумента.

Внутренне classmethod реализован как дескриптор. Когда метод декорирован как classmethod, его вызов приводит к вызову
метода \_\_get__ дескриптора, возвращающий привязанный метод - функцию, первым аргументом которой автоматически
становится класс:

```python
class A:
    @classmethod
    def method(cls):
        return f"вызван classmethod класса {cls}"


print(A.method())  # вызван classmethod класса <class '__main__.A'>
```

### staticmethod

**staticmethod** - это декоратор, который изменяет метод класса так, что он ведет себя как обычная функция,
не принимающая ни self, ни cls в качестве первого аргумента.

staticmethod также реализован как дескриптор. При его использовании метод \_\_get__ дескриптора просто
возвращает функцию без привязки к экземпляру или классу:

```python
class Math:
    @staticmethod
    def add(x, y):
        return x + y


print(Math.add(5, 7))  # 12
```

## Несколько особенностей

Дескрипторы данных \_\_get__ и \_\_set__ имеют приоритет над атрибутами экземпляра, тогда как дескрипторы
без данных \_\_get__ без \_\_set__ уступают им. Это важно учитывать при проектировании классов и их поведения.

\_\_set__ не будет вызываться, если попытаться изменить атрибут через прямое обращение к \_\_dict__ экземпляра. Чтобы
избежать этой ошибки, важно всегда использовать обычное присваивание для установки значений атрибутов, тем самым
обеспечивая вызов метода \_\_set__.

Если в классе определен дескриптор и атрибут экземпляра с одинаковым именем, это может привести к неожиданному
поведению. В таком случае дескриптор будет иметь приоритет при доступе через класс, но атрибут экземпляра может
своеобразно скрыть дескриптор при доступе напрямую. Чтобы избежать подобной ситуации, следует избегать именования
атрибутов экземпляра и дескрипторов одинаковыми именами.

При реализации метода \_\_get__ важно помнить, что он должен корректно обрабатывать ситуацию, когда instance аргумент
равен None. Это случается, когда доступ к атрибуту осуществляется через сам класс, а не его экземпляр. Обычно в таком
случае рекомендуется возвращать сам дескриптор (т.е., self).

Дескрипторы в Python — это удобный способ добавления логики к доступу к атрибутам.