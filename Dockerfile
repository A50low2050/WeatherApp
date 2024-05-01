FROM python:3.10.6

# Set enviroments
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/weather_app

COPY requirements.txt /usr/src/weather_app

RUN pip install -r /usr/src/weather_app/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



