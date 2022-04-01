import math
from typing import Dict, Type, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        # формируем строку сообщения
        return (f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def get_name(self) -> str:
        """Получить название тренировки."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = self.get_name()
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(training_type, self.duration, distance, speed, calories)
        return info
        pass


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight) -> None:
        # класс бег - наследник тренировки
        super().__init__(action, duration, weight)

    def get_name(self) -> str:
        # получаем имя для тренировки
        training_type = 'Running'
        return training_type

    def get_spent_calories(self) -> float:
        # расчет калорий бега
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        calories: float = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) *
                           self.weight / self.M_IN_KM * self.duration * self.H_IN_M)
        return calories

    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height) -> None:
        # класс спортходьба - наследник тренировки
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_name(self) -> str:
        # получаем имя для тренировки
        training_type = 'SportsWalking'
        return training_type

    def get_spent_calories(self) -> float:
        # расчет калорий ходьбы
        coeff_walk_1: float = 0.035
        coeff_walk_2: float = 0.029
        calories: float = ((coeff_walk_1 * self.weight + (math.sqrt(self.get_mean_speed()) //
                                                          self.height) * coeff_walk_2 * self.weight) *
                           self.duration * self.H_IN_M)
        return calories

    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool: float, count_pool: float) -> None:
        # класс плавание - наследник тренировки
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_name(self) -> str:
        # получаем имя для тренировки
        training_type = 'Swimming'
        return training_type

    def get_mean_speed(self) -> float:
        # расчет скорости плавание
        speed: float = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        # расчет калорий плавание
        coeff_swim_1: float = 1.1
        coeff_swim_2: float = 2
        calories: float = (self.get_mean_speed() + coeff_swim_1) * coeff_swim_2 * self.weight
        return calories

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages: List = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
