# Primitive Database Management System

Простая система управления базами данных с интерфейсом командной строки, поддерживающая полный набор CRUD операций, валидацию типов данных, подтверждение опасных операций и мониторинг производительности.

## Ссылка на asciinema
https://asciinema.org/a/iDtjYcaQSXjGPLouZmovqJW5z

## Установка

```bash
# Установка зависимостей
make install

# Установка пакета в систему
make package-install

Запуск
bash

# Запуск через установленный пакет
project

# Или через Poetry
make run

Полный список команд
Управление таблицами

    create_table <table> <column:type> ... - создать таблицу с указанными столбцами

    list_tables - показать список всех таблиц

    drop_table <table> - удалить таблицу (с подтверждением)

Операции с данными (CRUD)

    insert <table> <value1> <value2> ... - добавить запись (автоматическая генерация ID)

    select <table> [WHERE condition] - выбрать записи (с фильтрацией)

    update <table> SET <column=value> [WHERE condition] - обновить записи

    delete <table> [WHERE condition] - удалить записи (с подтверждением)

Общие команды

    help - показать справку по командам

    exit - выйти из программы

Поддерживаемые типы данных

    int - целые числа (например: 25, 100, -5)

    str - строки (например: "John", ProductName)

    bool - логические значения (true/false или 1/0)
