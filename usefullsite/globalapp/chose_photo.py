def getnameofphoto(weather: str, description: str) -> str:
    if weather == 'Drizzle':
        return "{% static 'img/icons_for_weather/drizzle.png' %}"

    if weather == 'Rain' and description not in [
        'freezing rain',
        'light intensity shower rain',
        'shower rain',
        'heavy intensity shower rain',
        'ragged shower rain',
    ]:
        return 'img/icons_for_weather/rain.png'

    if weather == 'Rain' and description in [
        'light intensity shower rain',
        'shower rain',
        'heavy intensity shower rain',
        'ragged shower rain',
    ]:
        return 'img/icons_for_weather/09d.png'

    if weather == 'Rain' and description is 'freezing rain':
        return 'img/icons_for_weather/freezing_rain.png'

    if weather == 'Thunderstorm':
        return 'img/icons_for_weather/thunderstorm.png'

    if weather == 'Snow':
        return 'img/icons_for_weather/freezing_rain.png'

    if weather in [
        'Mist',
        'Smoke',
        'Haze',
        'Dust',
        'Fog',
        'Sand',
        'Ash',
        'Squall',
        'Tornado'
    ]:
        return 'img/icons_for_weather/50d.png'

    if weather == 'Clear':
        return 'img/icons_for_weather/clear_sky.png'

    if weather == 'Clouds' and description == 'few clouds':
        return 'img/icons_for_weather/few_clouds.png'

    if weather == 'Clouds' and description == 'scattered clouds':
        return 'img/icons_for_weather/scattered_clouds.png'

    if weather == 'Clouds' and description in [
        'broken clouds',
        'overcast clouds'
    ]:
        return "img/icons_for_weather/broken_clouds_and_overcast.png"
