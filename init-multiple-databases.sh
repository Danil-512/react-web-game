#!/bin/bash

# Выполнение скрипта при любой ошибке
set -e
# Прерывать выполнение при попытке использования неопределенных переменных
set -u

# Функция для создания базы данных в рамках запущенной СУБД
function create_database() {
  # Локальная переменная. $1 - первый аргумент функции
  local database=$1
  #
  # Проверка существования нужной базы
  if PGPASSWORD="$MAIN_DATABASE_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$MAIN_DATABASE_USER" --dbname "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='$database'" | grep -q 1; then 
    echo "Database '$database' already exists, skipping"
    return 0
  fi
  #
  # Вывод в консоль информации о старте
  echo "Creating database '$database'"
  #
  # Подключение к главной базе данных в постгресе
  # <<-EOSQL - начало многострочного sql скрипта
  # ON_ERROR_STOP=1 - остановиться при ошибке sql
  PGPASSWORD="$MAIN_DATABASE_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$MAIN_DATABASE_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE "$database";
    GRANT ALL PRIVILEGES ON DATABASE "$database" TO "$MAIN_DATABASE_USER";
EOSQL
}

if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
  # Цикл по всем базам данных в переменной окружения с вызовом функции на создание базы данных
  for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    # Вызов функции создания базы данных
    create_database $db
    #
    # Вывод в терминал статуса
    echo "Database '$db' created"
  done
  #
  # Вывод в терминал статуса
  echo "Databases created"
fi