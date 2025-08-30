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
# Объявление используемого serve порта
EXPOSE 5173
#
# Запуск сервера для обслуживания статики
# -s означает serve SPA - single page application
# -l означает порт прослушивания
CMD ["serve", "-s", "dist", "-l", "5173"]


# Сборка образа
## docker build -t react-front-image .
# Удаление образа
## docker image rm react-front-image
# Запуск контейнера 
## docker run -dp 5173:5173 --name react-front react-front-image
# Удалить контейнер
## docker rm react-front
# Остановить контейнер 
## docker stop react-front
# Перезапустить контейнер
## docker restart react-front