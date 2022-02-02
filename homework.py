from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    RUNNING_SPEED_COEFF_1: float = 18.0
    RUNNING_SPEED_COEFF_2: float = 20.0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        speed_normalized: float = (self.RUNNING_SPEED_COEFF_1
                                   * self.get_mean_speed()
                                   - self.RUNNING_SPEED_COEFF_2) / self.M_IN_KM
        duration_in_minutes: float = self.duration * self.MINUTES_IN_HOUR
        running_spent_calories: float = (speed_normalized
                                         * duration_in_minutes * self.weight)
        return running_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPORTS_WALKING_CALORIES_COEFF_1: float = 0.035
    SPORTS_WALKING_CALORIES_COEFF_2: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

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


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SWIMMING_SPEED_COEFF_1: float = 1.1
    SWIMMING_SPEED_COEFF_2: float = 2.0

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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

    if workout_type in training_packages:
        return training_packages[workout_type](*data)
    else:
        raise ValueError(f'Тип тренировки {workout_type} не поддерживается.')


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
