def translate_weather(weather: str) -> str:
    if weather == 'Thunderstorm':
        return 'Гром'
    if weather == 'Drizzle':
        return 'Морось'
    if weather == 'Rain':
        return 'Дождь'
    if weather == 'Snow':
        return 'Снег'
    if weather == 'Mist':
        return 'Туман'
    if weather == 'Smoke':
        return 'Дымка'
    if weather == 'Haze':
        return 'Туман'
    if weather == 'Dust':
        return 'Пыль'
    if weather == 'Fog':
        return 'Туман'
    if weather == 'Sand':
        return 'Песчано'
    if weather == 'Ash':
        return 'Пепельно'
    if weather == 'Squall':
        return 'Шквал'
    if weather == 'Tornado':
        return 'Торнадо'
    if weather == 'Clear':
        return 'Чистое небо'
    if weather == 'Clouds':
        return 'Облачно'


def translate_description(description: str) -> str:
    if description == 'thunderstorm with light rain':
        return 'Гроза с небольшим дождём'

    if description == 'thunderstorm with rain':
        return 'Гроза с дождем'

    if description == 'thunderstorm with heavy rain':
        return 'Гроза с сильным дождем'

    if description == 'light thunderstorm':
        return 'Небольшая гроза'

    if description == 'thunderstorm':
        return 'На улице сейчас гроза, аккуратнее'

    if description == 'heavy thunderstorm':
        return 'Сильная гроза, осторожнее'

    if description == 'ragged thunderstorm':
        return "Острый 'рваный' гром"

    if description == 'thunderstorm with light drizzle':
        return 'Гроза с небольшим моросью'

    if description == 'thunderstorm with drizzle':
        return 'Гроза с моросью'

    if description == '	thunderstorm with heavy drizzle':
        return 'Гроза с сильной моросью'

    if description == 'light intensity drizzle':
        return 'Слабый дождь'

    if description == 'drizzle':
        return 'На улице моросит'

    if description == 'heavy intensity drizzle':
        return 'Сильный дождь/изморось'

    if description == 'light intensity drizzle rain':
        return 'Небольшой дождь/изморось'

    if description == 'drizzle rain':
        return 'Моросящий дождь'

    if description == 'heavy intensity drizzle rain':
        return 'Сильный моросящий дождь'

    if description == 'shower rain and drizzle':
        return 'Дождь с моросью'

    if description == 'shower drizzle':
        return 'Льёт как из ведра'

    if description == 'light snow':
        return 'Небольшой снегопад'

    if description == 'heavy snow':
        return 'Сильный снегопад'

    if description == 'sleet':
        return 'Мокрый снег/слякоть'

    if description == 'light shower sleet':
        return 'Небольшой дождь с мокрым снегом'

    if description == 'shower sleet':
        return 'Слякоть'

    if description == 'light rain and snow':
        return 'Небольшой дождь со снегом'

    if description == 'light rain':
        return 'На улице небольшой дождь/морось'

    if description == 'rain and snow':
        return 'Снег и дождь'

    if description == 'light shower snow':
        return 'Небольшой ливневый снегопад'

    if description == 'shower snow':
        return 'Снегопад'

    if description == 'heavy shower snow':
        return 'Сильный снегопад'

    if description == 'mist':
        return 'Туманная погода'

    if description == 'smoke':
        return 'На улице дымка, осторожнее!'

    if description == 'haze':
        return 'На улице обнаружена туманность'

    if description == 'sand/dust whirls':
        return 'Песчано-пылевые вихри'

    if description == 'fog':
        return 'На улице обнаружена туманность, осторожнее'

    if description == 'sand':
        return 'Порывы ветра, на улице песчано'

    if description == 'dust':
        return 'На улице пыльно'

    if description == 'volcanic ash':
        return 'Обнаружены вулканические осадки, очень аккуратно выходите на улицу'

    if description == 'squalls':
        return 'Обнаружен вихрь, осторожнее'

    if description == 'tornado':
        return 'На улице обнаружено торнадо, лучше не выходите из дома!'

    if description == 'clear sky':
        return 'На улице безоблачно, прекрасная погода!'

    if description == 'few clouds':
        return 'Небольшие облака: 11-25%'

    if description == 'scattered clouds':
        return 'Разбросанные по небу облака: 25-50%'

    if description == 'broken clouds':
        return 'Небо практически полностью заполнено облаками: 51-84%'

    if description == 'overcast clouds':
        return 'Пасмурная облачность: 85-100%'
