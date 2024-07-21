# Установка

Клонируем проект: 
``` bash
https://github.com/A50low2050/WeatherApp.git
```
Переходим в директорию:

```bash
cd weather_app
```
Установка зависимостей:

``` bash 
pip install requirements.txt
```

Создаем миграции:

``` bash 
manage.py migrate
```

Запускаем проект:

``` bash 
manage.py runserver
```

На windows должен быть загружен **Desktop Docker**

Пишем команду для запуска redis:

``` bash
docker-compose up
```
Запуск Celery:

```bash
celery -A weather_app worker --loglevel=info -P eventlet
```

# Описание

Приложение показывает погоду в городе с помощью открытого API сайта **openweathermap**.
Проект написан на **Django**.

Для кэширование данных использовал redis.**Redis** запускается через **Docker**.

# Стек

:white_check_mark: **Django**

:white_check_mark: **Docker**

:white_check_mark: **Redis**
