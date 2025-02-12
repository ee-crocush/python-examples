from abc import ABC, abstractmethod
from dataclasses import dataclass


class Animal(ABC):
    def __init__(self, age, name):
        if age < 0:
            raise ValueError('Животное еще не родилось')
        self.age = age
        self.name = name

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def show_info(self):
        msg = 'лет'

        if self.age == 1:
            msg = 'год'
        if self.age % 10 in {2, 3, 4}:
            msg = 'года'

        print(f'{self.name} живет уже {self.age} {msg}')


class Cat(Animal):
    def __init__(self, *args, **kwargs):
        self.__paws_count: int = 4
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_paws_text(val: int) -> str:
        if val == 1:
            return 'лапка'
        if val % 10 in {2, 3}:
            return 'лапки'
        return 'лапок'

    @property
    def paws_count(self) -> int:
        return self.__paws_count

    @paws_count.setter
    def paws_count(self, val: int):
        if not val:
            raise ValueError('Ты хочешь оставить котика без лапок?')
        if val > 4:
            print(
                f'Ты что, хочешь, чтобы у котика было {val} {self.get_paws_text(val)}? Дурной?'
            )
        if val < 4:
            print(
                f'Ты что хочешь оставить котика инвалидом? У него теперь {val} {self.get_paws_text(val)}!'
            )
        self.__paws_count = val

    def make_sound(self):
        print('МЯУ')

    def move(self):
        print('Котик скачет')


@dataclass(order=True)
class PositivePoint:
    x: int
    y: int
    z: int = 0

    def __post_init__(self):
        if self.x <= 0:
            raise ValueError('Число то должны быть больше нуля!')


def main():
    cat = Cat(age=2, name='Tom')
    cat.move()
    cat.show_info()
    cat.make_sound()

    print(f'У котика {cat.paws_count} лапки')

    cat.paws_count = 5
    cat.paws_count = 12

    print('С котиками закончили, переходим к dataclass')

    point = PositivePoint(10, 20)
    point2 = PositivePoint(10, 20, 30)

    print(point > point2)


if __name__ == '__main__':
    main()
