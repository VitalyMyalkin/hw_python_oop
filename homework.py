from typing import Dict, Type, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Формируем строку сообщения."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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
        # тут раньше была переменная "distance".
        # мы ее убрали, чтобы она не занимала память?
        # а высчитанное этой функцией значение
        # разве не сохраняется в какую-то ячейку?
        # и, соответственно, опять займет память...

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % self.__class__.__name__)

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

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        """Класс бег - наследник тренировки."""
        super().__init__(action, duration, weight)

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
    # если здесь использование функции math.sqrt неверно,
    # то почему значение калорий рассчитывается правильно??


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

    types: str = ''

    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    else:
        for i in list(workout_types):
            types += f'{i}, '
        raise ValueError(
            f'Текущая версия модуля фитнес-трекера работает c данными '
            f'тренировок c кодами {types}а от датчиков поступили '
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
