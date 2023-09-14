import random
from . import clothes


def choose_clothes(feels_like : int) -> str:
    my_advice = ''
    if feels_like >= 10 and feels_like <= 15:
        weather_list = clothes.clothes_for_temperature_between_10_and_15
        my_advice = random.choice(weather_list)

    if feels_like >= 16 and feels_like <= 24:
        weather_list = clothes.clothes_for_temperature_between_16_and_24
        my_advice = random.choice(weather_list)

    if feels_like >= 25 and feels_like <= 40:
        weather_list = clothes.clothes_for_temperature_between_25_and_40
        my_advice = random.choice(weather_list)

    if feels_like >= 41:
        weather_list = clothes.clothes_for_temperature_more_than_40
        my_advice = random.choice(weather_list)

    if feels_like >= 0 and feels_like <= 9:
        weather_list = clothes.clothes_for_temperature_between_0_and_9
        my_advice = random.choice(weather_list)

    if feels_like >= -10 and feels_like <= 0:
        weather_list = clothes.clothes_for_temperature_between_0_and_min10
        my_advice = random.choice(weather_list)

    if feels_like <= -11 and feels_like >= -23:
        weather_list = clothes.clothes_for_temperature_between_min11_and_min23
        my_advice = random.choice(weather_list)

    if feels_like <= -24 and feels_like >= -35:
        weather_list = clothes.clothes_for_temperature_between_min24_and_min35
        my_advice = random.choice(weather_list)

    if feels_like <= -36:
        weather_list = clothes.clothes_for_temperature_more_than_min35
        my_advice = random.choice(weather_list)
    

    return my_advice