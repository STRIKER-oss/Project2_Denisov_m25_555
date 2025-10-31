#!/usr/bin/env python3

from .utils import validate_column_definition, validate_data_type


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None
    
    table_columns = {"ID": "int"}
    
    for column_def in columns:
        if not validate_column_definition(column_def):
            print(f'Некорректное значение: "{column_def}". Попробуйте снова.')
            return None
        
        column_name, column_type = column_def.split(":")
        
        if not validate_data_type(column_type):
            print(f'Некорректный тип данных: "{column_type}". Поддерживаемые типы: int, str, bool.')
            return None
        
        table_columns[column_name] = column_type
    
    metadata[table_name] = table_columns
    
    columns_str = ", ".join([f"{col}:{typ}" for col, typ in table_columns.items()])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    
    return metadata


def list_tables(metadata):
    if not metadata:
        print("В базе данных нет таблиц.")
        return
    
    print("Список таблиц:")
    for table_name in metadata:
        print(f"- {table_name}")


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    
    return metadata
