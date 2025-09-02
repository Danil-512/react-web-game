# Базовый образ
FROM python:3.12-slim-bookworm
#
# Выбор программы для выполнения программ - bash
SHELL ["/bin/bash", "-c"]
#
# Создание переменных окружения
# Запретит python внутри контейнера создавать файлы с кэшем
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает буферезировать вывод ctd aut и std r - все сообщения будут сразу выводиться в std aut
ENV PYTHONUNBUFFERED 1
#
# Обновить pip
RUN pip install --upgrade pip
#
# Обновить все пакеты в линуксе
RUN apt-get update && apt-get install -y
#
# Создать нового пользователя в линуксе
RUN useradd -rms /bin/bash django-proj
#
# Создать и перейти в директорию проекта
WORKDIR /app
#
# Копирование зависимостей и их установка
COPY --chown=django-proj:django-proj requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#
# Копировать файлы проекта в образ контейнера
COPY --chown=django-proj:django-proj . .
#
# Переключение на нужного пользователя
USER django-proj
#
# Запуск проекта
CMD ["sh", "-c", "python ./laws_rest_api/manage.py migrate && gunicorn -b 0.0.0.0:7000 --pythonpath laws_rest_api laws_rest_api.wsgi:application"]
#
# Создание образа
# docker build -t django_laws_image .
#
# Создание контейнера
# docker run -dp 7000:7000 --name django_laws django_laws_image
#
# Запустить контейнер
# docker start django_laws
#
# Удалить образ
# docker image rm django_laws_image
#
# Удалить контейнер
# docker rm django_laws