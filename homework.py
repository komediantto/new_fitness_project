from typing import Dict

class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    def __init__(self, action: int, duration: int, weight: int, ):
        self.action = action
        self.duration = duration
        self.weight = weight
        # self.LEN_STEP: float = 0.65
        # self.M_IN_KM: int = 1000
    
    def get_distance(self):
        result = (self.action * self.LEN_STEP) / self.M_IN_KM
        return result
    
    def get_mean_speed(self):
        dist = self.get_distance()
        speed = dist / self.duration
        return speed
    
    def get_spent_calories(self):
        pass
    
    def show_training_info(self) -> 'InfoMessage':
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    def get_spent_calories(self):
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        cal = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) *
               self.weight / self.M_IN_KM * self.duration * 60)
        return cal


class SportsWalking(Training):
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self):
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        coeff_calorie_3: int = 2
        cal = ((coeff_calorie_1 * self.weight + 
                (self.get_mean_speed()**coeff_calorie_3 // self.height)
                * coeff_calorie_2 * self.weight) * self.duration * 60)
        return cal


class Swimming(Training):
    LEN_STEP: float = 1.38
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        
    
    def get_mean_speed(self):
        dist = self.get_distance()
        speed = (self.length_pool * self.count_pool /
                 self.M_IN_KM / self.duration)
        return speed
    
    def get_spent_calories(self):
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        cal = ((self.get_mean_speed() + coeff_calorie_1) * 
               coeff_calorie_2 * self.weight)  
        return cal


class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        
    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; ' 
               f'Длительность: {self.duration:.3f} ч.; ' 
               f'Дистанция: {self.distance:.3f} км; ' 
               f'Ср. скорость: {self.speed:.3f} км/ч; ' 
               f'Потрачено ккал: {self.calories:.3f}.') 
        
def read_package(workout_type, data):
    dict: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in dict:
        training = dict[workout_type]
        return training(*data)
    raise AttributeError

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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