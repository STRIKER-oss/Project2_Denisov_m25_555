#!/usr/bin/env python3

import shlex
import prompt
from .core import create_table, list_tables, drop_table
from .utils import load_metadata, save_metadata


def run():
    metadata_file = "db_meta.json"
    
    print("***База данных***\n")
    print_help()
    
    while True:
        metadata = load_metadata(metadata_file)
        
        user_input = prompt.string("Введите команду: ").strip()
        
        if not user_input:
            continue
        
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Ошибка разбора команды: {e}")
            continue
        
        command = args[0].lower()
        
        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Недостаточно аргументов. Использование: create_table <имя_таблицы> <столбец1:тип> ...")
                continue
            table_name = args[1]
            columns = args[2:]
            result = create_table(metadata, table_name, columns)
            if result is not None:
                save_metadata(metadata_file, result)
        elif command == "list_tables":
            list_tables(metadata)
        elif command == "drop_table":
            if len(args) < 2:
                print("Ошибка: Недостаточно аргументов. Использование: drop_table <имя_таблицы>")
                continue
            table_name = args[1]
            result = drop_table(metadata, table_name)
            if result is not None:
                save_metadata(metadata_file, result)
        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def welcome():
    run()
