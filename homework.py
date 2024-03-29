from typing import Dict, Type, List, ClassVar
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO_STRING: ClassVar[float] = ('Тип тренировки: {training_type}; '
                                    'Длительность: {duration:.3f} ч.; '
                                    'Дистанция: {distance:.3f} км; '
                                    'Ср. скорость: {speed:.3f} км/ч; '
                                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Формируем строку сообщения."""
        return self.INFO_STRING.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    H_IN_M: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Расчет калорий бега."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM * self.duration * self.H_IN_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_WALK_1: float = 0.035
    COEFF_WALK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        """Класс спортходьба - наследник тренировки."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет калорий ходьбы."""
        return ((self.COEFF_WALK_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.COEFF_WALK_2 * self.weight)
                * self.duration * self.H_IN_M)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_SWIM_1: float = 1.1
    COEFF_SWIM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        """Класс плавание - наследник тренировки."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчет скорости плавание."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчет калорий плавание."""
        return (self.get_mean_speed()
                + self.COEFF_SWIM_1) * self.COEFF_SWIM_2 * self.weight


def read_package(workout_type: str,
                 data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    types: str = ', '.join(workout_types)
    raise ValueError(
        f'Текущая версия модуля фитнес-трекера работает c данными '
        f'тренировок c кодами {types}, а от датчиков поступили '
        f'данные о неизвестной тренировке с кодом {workout_type}.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
