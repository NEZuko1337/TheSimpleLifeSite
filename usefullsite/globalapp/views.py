from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import random
import requests
from requests.exceptions import ReadTimeout
from fake_useragent import UserAgent
from . import translate_to_russian
from . import clothes_for_weather
from . chose_photo import getnameofphoto
from . calcul import calculateresult
from . forms import UserRegisterForm, LoginForm
from . translatedResponces import translateResponse

API_KEY_FOR_WEATHER = '1acb680e0f535aba8fbe6446aa7abde9'


# Функция обработки домашней страницы
def home_page(request):
    return render(request, 'globalapp/home.html')


# Функция обработки страницы about
def about_page(request):
    return render(request, 'globalapp/about.html')


# Функция обработки страницы генерации пароля
@login_required
def password_generator(request):
    return render(request, "globalapp/password_generator.html")


# Функция обработки страницы с погодой
@login_required
def weatherpage(request):
    return render(request, "globalapp/weatherpage.html")


# Функция обработки страницы с калькулятором
@login_required
def calcpage(request):
    return render(request, "globalapp/calcpage.html")


# Функция обработки страницы с контактной инфой
def contactspage(request):
    return render(request, "globalapp/contacts.html")


# Функция обработки страницы с переводчиком
@login_required
def translatorpage(request):
    return render(request, "globalapp/translatorpage.html")


# Функция для регистрации пользователя
def registerUser(request):
    # Если метод пост, то иду ниже
    if request.method == "POST":
        # Создаю форму с пост-датой
        form = UserRegisterForm(data=request.POST)
        # Проверяю форму на валидность,
        if form.is_valid():
            # Есди все хорошо, сохраняю юзера и делаю редирект на login страничку
            form.save()
            return redirect('loginUser')
        else:
            # Иначе рендерю эту же страницу и выдаю ошибки, которые уже автоматом встроены в form(очень удобно)
            return render(request, "globalapp/register.html", {'form': form, 'error_message': form.errors})
    # Просто гет запрос
    else:
        form = UserRegisterForm()
        return render(request, "globalapp/register.html", {'form': form})


# Функция для логина пользователя
def loginUser(request):
    # Елси пост, то иду ниже
    if request.method == "POST":
        # Создаю формочку с пост-датой
        form = LoginForm(data=request.POST)
        # Чекаю на валидность
        if form.is_valid():
            # Если валидна, то получаю username и password
            username = request.POST['username']
            password = request.POST['password']
            # Аутентефицирую пользоватателя
            user = authenticate(username=username, password=password)
            # Проверяю на существование и неудаленность его из базы с пользователями
            if user.is_active and user is not None:
                # Логиню и возвращаюсь на главную страницу
                login(request, user)
                return redirect('home')
        # Если форма не валидна, кидаю на ту же страницу, добавляя на нее ошибки
        else:
            return render(request, 'globalapp/login.html', {'form': form, 'error_message': form.non_field_errors})
    # Обычный гет запрос
    else:
        form = LoginForm()
        return render(request, "globalapp/login.html", {'form': form, 'error_message': form.non_field_errors})


# Функция выхода пользователя из аккаунта, тут объяснять нечего, все изи.
@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')


# Сама генерация пароля
@login_required
def generated_password(request):
    generated_pass = ''
    length_of_password = int(request.GET.get('length'))
    default_letters = []

    # Две проверки на то, чтобы не обойти систему хихихаха(длина)
    if length_of_password < 8 or length_of_password > 16:
        return render(request, "globalapp/password_generator.html",
                      {"error": "Ах ты засранец, не обманывай систему, выбирай из того, что есть"}
                      )

    # Проверка на заглавные буквы
    uppercase_check = request.GET.get('uppercase')
    if uppercase_check:
        default_letters.extend(list('QWERTYUIOPASDFGHJKLZXCVBNM'))

    # Проверка на цифры
    numbers_check = request.GET.get('numbers')
    if numbers_check:
        default_letters.extend(list('1234567890'))

    # Проверка на специальные символы
    special_symbols_check = request.GET.get('special')
    if special_symbols_check:
        default_letters.extend(list('~!@#$%^&*()_-+=/}:;?{'))

    # Проверка на существование букв в пароле
    letters_check = request.GET.get('letters')
    if letters_check:
        default_letters.extend(list('qwertyuiopasdfghjklzxcvbnm'))

    # Отлов крысенышка
    if default_letters == []:
        return render(request, "globalapp/password_generator.html",
                      {"error": "Ну выбери что-нибудь, как я тебе пароль сделаю из ничего!"}
                      )
    # Основной цикл программы
    for _ in range(length_of_password):
        generated_pass += random.choice(default_letters)
    return render(request, "globalapp/generatedpass.html", {'password': generated_pass})


# Функция для прогноза одежды и погоды, объективно можно было сделать лучше, но додумася до этого довольно поздно
# Запросы к апихе можно было делать в другой функции, плюс асинхронно, но я решил опустить этот момент, оставил как есть
# Все работает, кул
@login_required
def generated_weather(request):
    city = None
    check_clothes = None
    check_weather = None
    ua = UserAgent().random
    header = {
        "user-agent": ua
    }
    if request.method == 'POST':
        if request.POST.get('city') is not None:
            city = request.POST.get('city', None)
            check_clothes = request.POST.get('clothes_check', None)
            check_weather = request.POST.get('weather_now', None)

            # Отлов птушника
            if check_clothes is None and check_weather is None:
                return render(request, 'globalapp/weatherpage.html', {
                    'error': 'Тебе нужно выбрать какой-то из параметров, ты же явно не хочешь увидеть пустую страницу ^_^'
                }
                )
            if len(city) <= 1:
                return render(request, 'globalapp/weatherpage.html', {
                    'error': 'Введи информацию корректно',
                }
                )
            if check_weather and check_clothes:
                # Линк ведущий на главный сайт с погодой
                main_link = 'http://api.openweathermap.org'

                # Линк чтобы узнать координаты
                link_for_coordinates = f'{main_link}/geo/1.0/direct?q={city}&appid={API_KEY_FOR_WEATHER}'

                # Делаю запрос, чтобы узнать координаты
                try:
                    req_to_know_the_coordinates_of_city = requests.get(
                        link_for_coordinates, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте чуть позже'
                    }
                    )
                try:
                    # Узнаем координаты нашего города
                    lat = req_to_know_the_coordinates_of_city[0]['lat']
                    lon = req_to_know_the_coordinates_of_city[0]['lon']
                except KeyError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Хм, смешно, а как я тебе выдам информацию без введенного города? Введи его скорее!'})
                except IndexError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Такого города не существует, введи существующий'})

                # Тут уже линка на основной прогноз
                link_to_forecast = f'{main_link}/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY_FOR_WEATHER}'
                try:
                    req_to_know_the_weather = requests.get(
                        link_to_forecast, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте немного позже'
                    }
                    )
                # Температура и некоторые другие параметры, 273 отнимаю, так как Кельвины.
                temp = int(
                    req_to_know_the_weather['list'][0]['main']['temp']) - 273
                feels_like = int(
                    req_to_know_the_weather['list'][0]['main']['feels_like']) - 273
                humidity = str(
                    req_to_know_the_weather['list'][0]['main']['humidity']) + '%'

                temp_during_next_3_hours = int(
                    req_to_know_the_weather['list'][1]['main']['temp']) - 273
                feels_like_during_next_3_hours = feels_like = int(
                    req_to_know_the_weather['list'][1]['main']['feels_like']) - 273
                humidity_during_next_3_hours = humidity = str(
                    req_to_know_the_weather['list'][1]['main']['humidity']) + '%'

                # Совет с оджеждой смотреть clothes_for_weather.py
                my_advice: str = clothes_for_weather.choose_clothes(
                    feels_like=feels_like)

                advice_for_next_3_hours = clothes_for_weather.choose_clothes(
                    feels_like=feels_like_during_next_3_hours)

                # Узнаем что сейчас на улице, а после переводим на русский
                main_weather = req_to_know_the_weather['list'][0]['weather'][0]['main']
                weather_description = req_to_know_the_weather['list'][0]['weather'][0]['description']

                main_weather_for_next_3_hours = req_to_know_the_weather[
                    'list'][1]['weather'][0]['main']
                weather_description_for_next_3_hours = req_to_know_the_weather[
                    'list'][1]['weather'][0]['description']

                # Функции по переводу есть в translate_to_russian.py
                translated_weather = translate_to_russian.translate_weather(
                    main_weather)
                translated_description = translate_to_russian.translate_description(
                    weather_description)

                translated_weather_for_next_3_hours = translate_to_russian.translate_weather(
                    main_weather_for_next_3_hours)
                translated_description_for_next_3_hours = translate_to_russian.translate_description(
                    weather_description_for_next_3_hours)

                # Выбор фотки по погоде смотреть chose_photo.py
                url_of_photo = getnameofphoto(
                    main_weather, weather_description)

                url_of_photo_for_next_3_hours = getnameofphoto(
                    main_weather_for_next_3_hours, weather_description_for_next_3_hours)

                # Загружаю параметры в словарик контекст и передаю его(base)
                context = {
                    'city': city,

                    'temp': temp,
                    'next_temp': temp_during_next_3_hours,

                    'feels_like': feels_like,
                    'next_feels_like': feels_like_during_next_3_hours,

                    'humidity': humidity,
                    'next_humidity': humidity_during_next_3_hours,

                    'advice': my_advice,
                    'next_advice': advice_for_next_3_hours,

                    'main_weather': translated_weather,
                    'next_main_weather': translated_weather_for_next_3_hours,

                    'weather_description': translated_description,
                    'next_weather_description': translated_description_for_next_3_hours,

                    'photourl': url_of_photo,
                    'next_photo': url_of_photo_for_next_3_hours
                }
                return render(request, 'globalapp/generatedweather.html', context)
            if check_weather:
                # Линк ведущий на главный сайт с погодой
                main_link = 'http://api.openweathermap.org'

                # Линк чтобы узнать координаты
                link_for_coordinates = f'{main_link}/geo/1.0/direct?q={city}&appid={API_KEY_FOR_WEATHER}'

                # Делаю запрос, чтобы узнать координаты
                try:
                    req_to_know_the_coordinates_of_city = requests.get(
                        link_for_coordinates, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте чуть позже'
                    }
                    )
                try:
                    # Узнаем координаты нашего города
                    lat = req_to_know_the_coordinates_of_city[0]['lat']
                    lon = req_to_know_the_coordinates_of_city[0]['lon']
                except KeyError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Хм, смешно, а как я тебе выдам информацию без введенного города? Введи его скорее!'})
                except IndexError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Такого города не существует, введи существующий'})

                # Тут уже линка на основной прогноз
                link_to_forecast = f'{main_link}/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY_FOR_WEATHER}'
                try:
                    req_to_know_the_weather = requests.get(
                        link_to_forecast, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте немного позже'
                    }
                    )
                # Температура и некоторые другие параметры, 273 отнимаю, так как Кельвины.
                temp = int(
                    req_to_know_the_weather['list'][0]['main']['temp']) - 273
                feels_like = int(
                    req_to_know_the_weather['list'][0]['main']['feels_like']) - 273
                humidity = str(
                    req_to_know_the_weather['list'][0]['main']['humidity']) + '%'

                temp_during_next_3_hours = int(
                    req_to_know_the_weather['list'][1]['main']['temp']) - 273
                feels_like_during_next_3_hours = feels_like = int(
                    req_to_know_the_weather['list'][1]['main']['feels_like']) - 273
                humidity_during_next_3_hours = humidity = str(
                    req_to_know_the_weather['list'][1]['main']['humidity']) + '%'

                # Узнаем что сейчас на улице, а после переводим на русский
                main_weather = req_to_know_the_weather['list'][0]['weather'][0]['main']
                weather_description = req_to_know_the_weather['list'][0]['weather'][0]['description']

                main_weather_for_next_3_hours = req_to_know_the_weather[
                    'list'][1]['weather'][0]['main']
                weather_description_for_next_3_hours = req_to_know_the_weather[
                    'list'][1]['weather'][0]['description']

                # Функции по переводу есть в translate_to_russian.py
                translated_weather = translate_to_russian.translate_weather(
                    main_weather)
                translated_description = translate_to_russian.translate_description(
                    weather_description)

                translated_weather_for_next_3_hours = translate_to_russian.translate_weather(
                    main_weather_for_next_3_hours)
                translated_description_for_next_3_hours = translate_to_russian.translate_description(
                    weather_description_for_next_3_hours)

                # Выбор фотки по погоде смотреть chose_photo.py
                url_of_photo = getnameofphoto(
                    main_weather, weather_description)

                url_of_photo_for_next_3_hours = getnameofphoto(
                    main_weather_for_next_3_hours, weather_description_for_next_3_hours)
                context = {
                    'city': city,

                    'temp': temp,
                    'next_temp': temp_during_next_3_hours,

                    'feels_like': feels_like,
                    'next_feels_like': feels_like_during_next_3_hours,

                    'humidity': humidity,
                    'next_humidity': humidity_during_next_3_hours,

                    'main_weather': translated_weather,
                    'next_main_weather': translated_weather_for_next_3_hours,

                    'weather_description': translated_description,
                    'next_weather_description': translated_description_for_next_3_hours,

                    'photourl': url_of_photo,
                    'next_photo': url_of_photo_for_next_3_hours
                }
                return render(request, 'globalapp/generatedweather.html', context)
            if check_clothes:
                # Линк ведущий на главный сайт с погодой
                main_link = 'http://api.openweathermap.org'

                # Линк чтобы узнать координаты
                link_for_coordinates = f'{main_link}/geo/1.0/direct?q={city}&appid={API_KEY_FOR_WEATHER}'

                # Делаю запрос, чтобы узнать координаты
                try:
                    req_to_know_the_coordinates_of_city = requests.get(
                        link_for_coordinates, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте чуть позже'
                    }
                    )
                try:
                    # Узнаем координаты нашего города
                    lat = req_to_know_the_coordinates_of_city[0]['lat']
                    lon = req_to_know_the_coordinates_of_city[0]['lon']
                except KeyError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Хм, смешно, а как я тебе выдам информацию без введенного города? Введи его скорее!'})
                except IndexError:
                    return render(request, 'globalapp/weatherpage.html', {'error': 'Такого города не существует, введи существующий'})

                # Тут уже линка на основной прогноз
                link_to_forecast = f'{main_link}/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY_FOR_WEATHER}'
                try:
                    req_to_know_the_weather = requests.get(
                        link_to_forecast, headers=header).json()
                except ReadTimeout:
                    return render(request, 'globalapp/weatherpage.html', {
                        'error': 'Возникла ошибка, попробуйте немного позже'
                    }
                    )

                feels_like = int(
                    req_to_know_the_weather['list'][0]['main']['feels_like']) - 273

                # Совет с оджеждой смотреть clothes_for_weather.py
                my_advice: str = clothes_for_weather.choose_clothes(
                    feels_like=feels_like)

                context = {
                    'city': city,
                    'advice': my_advice,
                }

                return render(request, 'globalapp/generatedweather.html', context)

            # Впаду писать какие то адекватные ошибки, этого достаточно
            else:
                return render(request, 'globalapp/weatherpage.html', {'error': 'Возникла ошибка, проверь все ли ты верно ввел'})

        # Еще один отлов птушника
        else:
            return render(request, 'globalapp/weatherpage.html', {'error': 'Хм, смешно, а как я тебе выдам информацию без введенного города? Введи его скорее!'})

    # Просто гет запрос
    else:
        return render(request, 'globalapp/weatherpage.html')
    # Ура, я закончил эту функцию, наконец-то


# Функция выполняющая базовыые математические вычисления с калькулятором
@login_required
def calculate(request):
    # Основные вычисления и вся программа в целом
    if request.method == 'POST':
        # Получаю инфу
        first_number = request.POST.get('number1')
        second_number = request.POST.get('number2')
        operation = request.POST.get('operation')
        # Основная прога
        if first_number is not None and second_number is not None and operation in ['+', '-', '*', '/']:
            try:
                # Перевожу в флоат
                num1 = float(first_number)
                num2 = float(second_number)
            # Ловлю ошибку
            except ValueError:
                return render(request, 'globalapp/calcpage.html', {
                    'error': 'Ты не ввел необходимую информацию, ввел ее некоректно, или пытаешься выполнить то же самое действие, уже имея ответ на свой вопрос, введи данные заново пожалуйста'})
            try:
                result = calculateresult(num1, operation, num2)
            # делить на 0 забанено
            except ZeroDivisionError:
                return render(request, "globalapp/calcpage.html", {'error': 'На 0 делить нельзя дружочек, не забывай про это'})
            return render(request, 'globalapp/calcpage.html', {
                'result': result,
                'num1': num1,
                'num2': num2,
                'operation': operation,
            }
            )

        # Отлов ослов
        if operation not in [
            '+', '-', '*', '/'
        ]:
            return render(request, 'globalapp/calcpage.html', {'error': 'Мамкин хакер не меняй код, давай лучше данные введи нормальные'})
        else:
            return render(request, 'globalapp/calcpage.html', {'error': 'Что-то пошло не так'})

    # Гет запрос
    else:
        return render(request, "globalapp/calcpage.html")


# Переводчик
@login_required
def translated_text(request):
    # Фейк юзерагент для реквестов
    ua = UserAgent().random
    header = {
        "user-agent": ua
    }
    if request.method == 'POST':
        # Получаю инфу
        text_to_translate = request.POST.get('text_to_translate')
        language_from = request.POST.get('language_from')
        language_to = request.POST.get('language_to')
        # Объеденяю два языка в пару для api
        language_pair = language_from+'|'+language_to
        # Основная апишка
        API = f'https://api.mymemory.translated.net/get?q={text_to_translate}&langpair={language_pair}'
        try:
            req = requests.get(API, headers=header).json()
        # Ловлю ошибку долгого получения инфы с сервера
        except ReadTimeout:
            return render(request, 'globalapp/translatorpage.html', {'error': 'Возникла ошибка, попробуйте чуть позже'})
        # Ловлю ошибку коннекта с апишкой
        except requests.exceptions.ConnectionError:
            return render(request, 'globalapp/translatorpage.html', {'error': 'Подключение в данный момент невозможно'})
        # Статус код
        responseStatus = int(req['responseStatus'])
        # Описание кода
        responseDetails = req['responseDetails']
        # Перевожу на русский через translatedResponces.py
        translated_responseDetails = translateResponse(responseDetails)
        # Елси код >=200 все кул, выводим все и кайфуем
        if responseStatus >= 200 and responseStatus < 300:
            translated_text = req['responseData']['translatedText']
            context = {
                'translatedText': translated_text,
                'text_to_translate': text_to_translate
            }
            return render(request, "globalapp/translatorpage.html", context)
        # Это увы
        if responseStatus >= 400 and responseStatus < 500:
            return render(request, 'globalapp/translatorpage.html', {'error': translated_responseDetails})
        else:
            # Написал от балды вдруг какую еще ошибку тут поймаю, кто знает
            return render(request, 'globalapp/translatorpage.html', {
                'error': 'Возникла серверная ошибка, если вы ее видите, напишите мне в ВК или на гит, желательно прикрепить скрин того, что вы вводили',
            })
    # Гет запросик
    else:
        return render(request, 'globalapp/translatorpage.html')

# На 14.09.23 я заканчиваю работу с данным проектом, дальше буду деплоить его, изменю эту комент, когда захочу что-то добавить/поменять
# сам сайт будет находится по примерной ссылке https://thesimplelife.pythonanywhere.com/
# Следить за самим проектом можно на моем гите, все будет в пинах
