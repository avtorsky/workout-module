from dataclasses import dataclass, field
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: int = field(default=1000, init=False)
    MINUTES_IN_HOUR: int = field(default=60, init=False)

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUNNING_SPEED_COEFF_1: float = field(default=18.0, init=False)
    RUNNING_SPEED_COEFF_2: float = field(default=20.0, init=False)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        speed_normalized: float = (self.RUNNING_SPEED_COEFF_1
                                   * self.get_mean_speed()
                                   - self.RUNNING_SPEED_COEFF_2) / self.M_IN_KM
        duration_in_minutes: float = self.duration * self.MINUTES_IN_HOUR
        running_spent_calories: float = (speed_normalized
                                         * duration_in_minutes * self.weight)
        return running_spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPORTS_WALKING_CALORIES_COEFF_1: float = field(default=0.035, init=False)
    SPORTS_WALKING_CALORIES_COEFF_2: float = field(default=0.029, init=False)

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        mean_speed_to_height_ratio: float = (self.get_mean_speed()
                                             ** 2 // self.height)
        weight_summand_1: float = (self.SPORTS_WALKING_CALORIES_COEFF_1
                                   * self.weight)
        weight_summand_2: float = (mean_speed_to_height_ratio
                                   * self.SPORTS_WALKING_CALORIES_COEFF_2
                                   * self.weight)
        weight_summation: float = weight_summand_1 + weight_summand_2
        duration_in_minutes: float = self.duration * self.MINUTES_IN_HOUR
        sports_walking_spent_calories: float = (weight_summation
                                                * duration_in_minutes)
        return sports_walking_spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = field(default=1.38, init=False)
    SWIMMING_SPEED_COEFF_1: float = field(default=1.1, init=False)
    SWIMMING_SPEED_COEFF_2: float = field(default=2.0, init=False)

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        distance_in_meters: float = self.length_pool * self.count_pool
        distance_in_kilometers: float = distance_in_meters / self.M_IN_KM
        swimming_mean_speed: float = distance_in_kilometers / self.duration
        return swimming_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        speed_normalized: float = ((self.get_mean_speed()
                                   + self.SWIMMING_SPEED_COEFF_1)
                                   * self.SWIMMING_SPEED_COEFF_2)
        swimming_spent_calories: float = speed_normalized * self.weight
        return swimming_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_packages: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_packages:
        raise ValueError(f'Тип тренировки {workout_type} не поддерживается.')
    elif len(data) < 3:
        raise ValueError(f'В пакете {workout_type}:{data} '
                         'недостаточно данных о результатах тренировки.')
    return training_packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
