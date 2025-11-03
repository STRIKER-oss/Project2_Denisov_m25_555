import shlex

import prompt

from .core import (
    create_table,
    delete,
    display_table_data,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_set_clause, parse_where_condition
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def run():
    print("***База данных***\n")
    print_help()

    while True:
        metadata = load_metadata()

        try:
            user_input = prompt.string("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы...")
            break

        if not user_input:
            continue

        try:
            arguments = shlex.split(user_input)
        except ValueError as error:
            print(f"Ошибка разбора команды: {error}")
            continue

        if not arguments:
            continue

        command = arguments[0].lower()

        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            handle_create_table(metadata, arguments)
        elif command == "list_tables":
            list_tables(metadata)
        elif command == "drop_table":
            handle_drop_table(metadata, arguments)
        elif command == "insert":
            handle_insert(metadata, arguments)
        elif command == "select":
            handle_select(metadata, arguments)
        elif command == "update":
            handle_update(metadata, arguments)
        elif command == "delete":
            handle_delete(metadata, arguments)
        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")
            print("Введите 'help' для справки.")


def handle_create_table(metadata, arguments):
    if len(arguments) < 3:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: create_table <имя_таблицы> <столбец1:тип> ..."
        print(msg)
        return

    table_name = arguments[1]
    columns = arguments[2:]
    result = create_table(metadata, table_name, columns)
    if result is not None:
        save_metadata(result)


def handle_drop_table(metadata, arguments):
    if len(arguments) < 2:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: drop_table <имя_таблицы>"
        print(msg)
        return

    table_name = arguments[1]
    result = drop_table(metadata, table_name)
    if result is not None:
        save_metadata(result)


def handle_insert(metadata, arguments):
    if len(arguments) < 3:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: insert <имя_таблицы> <значение1> <значение2> ..."
        print(msg)
        return
    
    table_name = arguments[1]
    
    # Простой split для всех аргументов после имени таблицы
    values = arguments[2:]
    
    if values is not None:
        result = insert(metadata, table_name, values)
        if result is not None:
            save_table_data(table_name, result)

def handle_select(metadata, arguments):
    if len(arguments) < 2:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: select <имя_таблицы> [WHERE условие]"
        print(msg)
        return

    table_name = arguments[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    where_clause = None
    if len(arguments) > 2:
        where_string = ' '.join(arguments[2:])
        where_clause = parse_where_condition(where_string)
        if where_clause is None:
            return

    table_data = load_table_data(table_name)
    if table_data is not None:
        result_data = select(table_data, where_clause)
        display_table_data(result_data, table_name)


def handle_update(metadata, arguments):
    if len(arguments) < 4:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: update <имя_таблицы> SET <условие> [WHERE условие]"
        print(msg)
        return

    table_name = arguments[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    if arguments[2].upper() != 'SET':
        print("Ошибка: Ожидается ключевое слово SET")
        return

    where_index = -1
    for index, argument in enumerate(arguments):
        if argument.upper() == 'WHERE':
            where_index = index
            break

    if where_index != -1:
        set_string = ' '.join(arguments[3:where_index])
        where_string = ' '.join(arguments[where_index+1:])
    else:
        set_string = ' '.join(arguments[3:])
        where_string = None

    set_clause = parse_set_clause(set_string)
    where_clause = parse_where_condition(where_string) if where_string else None

    if set_clause is not None:
        table_data = load_table_data(table_name)
        if table_data is not None:
            result_data = update(table_data, set_clause, where_clause)
            if result_data is not None:
                save_table_data(table_name, result_data)


def handle_delete(metadata, arguments):
    if len(arguments) < 2:
        msg = "Ошибка: Недостаточно аргументов."
        msg += " Использование: delete <имя_таблицы> [WHERE условие]"
        print(msg)
        return

    table_name = arguments[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    where_clause = None
    if len(arguments) > 2:
        where_string = ' '.join(arguments[2:])
        where_clause = parse_where_condition(where_string)
        if where_clause is None:
            return

    table_data = load_table_data(table_name)
    if table_data is not None:
        result_data = delete(table_data, where_clause)
        if result_data is not None:
            save_table_data(table_name, result_data)


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("  create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("  list_tables - показать список всех таблиц")
    print("  drop_table <имя_таблицы> - удалить таблицу")
    print("  insert <имя_таблицы> <значение1> <значение2> ... - добавить запись")
    print("  select <имя_таблицы> [WHERE условие] - выбрать записи")
    msg = "  update <имя_таблицы> SET <столбец=значение>"
    msg += " [WHERE условие] - обновить записи"
    print(msg)
    print("  delete <имя_таблицы> [WHERE условие] - удалить записи")

    print("\nОбщие команды:")
    print("  exit - выход из программы")
    print("  help - справочная информация")

    print("\nПримеры:")
    print("  create_table users name:str age:int active:bool")
    print('  insert users "John Doe" 25 true')
    print('  select users WHERE "age > 20"')
    print('  update users SET "active = false" WHERE "name = John Doe"')
    print('  delete users WHERE "active = false"')
    print()


def welcome():
    run()
