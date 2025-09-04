# ЭТАП СБОРКИ ПРОЕКТА
FROM node:22-alpine as builder
#
# Установка рабочей директории внутри проекта
WORKDIR /app
#
# Копирование файлов зависимостей
COPY package*.json ./
#
# Установка всех скопированных зависимостей
RUN npm install
#
# Копирование всего кода проекта в рабочую директорию контейнера
COPY . .
#
# Сборка приложения
RUN npm run build


# ЭТАП ЗАПУСКА
FROM node:22-alpine as runner
#
# Установка рабочей директории внутри проекта
WORKDIR /app
#
# Установка локального сервера serve глобально для обслуживания статики
RUN npm install -g serve
#
# Копирование приложения собранного на этапе build
COPY --from=builder /app/dist ./dist
#
CMD ["echo", "React build complete - static files reading for nginx"]


# Сборка образа
## docker build -t react_front_image .
# Удаление образа
## docker image rm react_front_image
# Запуск контейнера 
## docker run -dp 5173:5173 --name react_front react_front_image
# Удалить контейнер
## docker rm react_front
# Остановить контейнер 
## docker stop react_front
# Перезапустить контейнер
## docker restart react_front