from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from globalapp import views


urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Аутентификация и регистрация
    path('register/', views.registerUser, name='registerUser'),
    path('loginuser/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),


    # Главная страница, avout, contancs
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contacts/', views.contactspage, name='contactspage'),

    # Генератор паролей
    path('generatepassword/', views.password_generator, name='generatepassword'),
    path('generatepassword/generated',
         views.generated_password, name='generated_password'),

    # Прогноз погоды и одежды
    path('weatherpage/', views.weatherpage, name='weatherpage'),
    path('weatherpage/generated/', views.generated_weather,
         name='generated_weather'),

    # Калькулятор
    path('calcpage/', views.calcpage, name='calcpage'),
    path('calcpage', views.calculate, name='calculate'),

    # Переводчик
    path('translatorpage/', views.translatorpage, name='translatorpage'),
    path('translatorpage',
         views.translated_text, name='translated_text'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
