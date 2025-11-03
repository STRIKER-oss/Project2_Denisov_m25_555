#!/usr/bin/env python3
from prettytable import PrettyTable

from ..decorators import confirm_action, handle_db_errors, log_time
from .constants import (
    ERROR_COLUMN_COUNT,
    ERROR_INVALID_DATA_TYPE,
    ERROR_INVALID_TYPE,
    ERROR_INVALID_VALUE,
    ERROR_TABLE_EXISTS,
    ERROR_TABLE_NOT_EXISTS,
    SUPPORTED_TYPES,
    VALID_BOOLEAN_VALUES,
)
from .utils import (
    load_table_data,
    save_table_data,
    validate_column_definition,
    validate_data_type,
)


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(ERROR_TABLE_EXISTS.format(table_name))
        return None

    table_columns = {"ID": "int"}

    for column_definition in columns:
        if not validate_column_definition(column_definition):
            print(ERROR_INVALID_VALUE.format(column_definition))
            return None

        column_name, column_type = column_definition.split(":")

        if not validate_data_type(column_type):
            supported_types_str = ", ".join(SUPPORTED_TYPES)
            print(ERROR_INVALID_DATA_TYPE.format(column_type, supported_types_str))
            return None

        table_columns[column_name] = column_type

    metadata[table_name] = table_columns

    save_table_data(table_name, [])

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


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(ERROR_TABLE_NOT_EXISTS.format(table_name))
        return None

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(ERROR_TABLE_NOT_EXISTS.format(table_name))
        return None

    table_schema = metadata[table_name]
    expected_columns = list(table_schema.keys())[1:]
    expected_count = len(expected_columns)

    if len(values) != expected_count:
        print(ERROR_COLUMN_COUNT.format(expected_count, len(values)))
        return None

    table_data = load_table_data(table_name)

    validated_values = []
    for index, value in enumerate(values):
        column_name = expected_columns[index]
        expected_type = table_schema[column_name]

        if not validate_value_type(value, expected_type):
            print(ERROR_INVALID_TYPE.format(column_name, expected_type))
            return None

        validated_values.append(convert_value(value, expected_type))

    if table_data:
        new_id = max(item['ID'] for item in table_data) + 1
    else:
        new_id = 1

    new_record = {'ID': new_id}
    for index, column_name in enumerate(expected_columns):
        new_record[column_name] = validated_values[index]

    table_data.append(new_record)
    save_table_data(table_name, table_data)

    print(f'Запись успешно добавлена в таблицу "{table_name}" с ID {new_id}.')
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    if not table_data:
        return []

    if where_clause is None:
        return table_data

    filtered_data = []
    for record in table_data:
        is_match = True
        for column, value in where_clause.items():
            if column == "_operator":
                continue
                
            if column not in record:
                is_match = False
                break
                
            operator = where_clause.get("_operator", "=")
            record_value = record[column]
            condition_value = convert_value(value, type(record_value).__name__)
            
            if operator == "=":
                if record_value != condition_value:
                    is_match = False
                    break
            elif operator == ">":
                if record_value <= condition_value:
                    is_match = False
                    break
            elif operator == "<":
                if record_value >= condition_value:
                    is_match = False
                    break
            elif operator == ">=":
                if record_value < condition_value:
                    is_match = False
                    break
            elif operator == "<=":
                if record_value > condition_value:
                    is_match = False
                    break
                    
        if is_match:
            filtered_data.append(record)

    return filtered_data

@handle_db_errors
def update(table_data, set_clause, where_clause):
    if not table_data:
        return table_data
    
    updated_count = 0
    for record in table_data:
        is_match = True
        for column, value in where_clause.items():
            if column == "_operator":
                continue
                
            if column not in record:
                is_match = False
                break
                
            operator = where_clause.get("_operator", "=")
            record_value = record[column]
            condition_value = convert_value(value, type(record_value).__name__)
            
            if operator == "=":
                if record_value != condition_value:
                    is_match = False
                    break
            elif operator == ">":
                if record_value <= condition_value:
                    is_match = False
                    break
            elif operator == "<":
                if record_value >= condition_value:
                    is_match = False
                    break
            elif operator == ">=":
                if record_value < condition_value:
                    is_match = False
                    break
            elif operator == "<=":
                if record_value > condition_value:
                    is_match = False
                    break
        
        if is_match:
            for column, new_value in set_clause.items():
                if column in record and column != 'ID':
                    record_type = type(record[column]).__name__
                    record[column] = convert_value(new_value, record_type)
                    updated_count += 1
    
    print(f'Обновлено {updated_count} записей.')
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    if not table_data:
        return table_data
    
    if where_clause is None:
        deleted_count = len(table_data)
        table_data.clear()
        print(f'Удалено {deleted_count} записей.')
        return table_data
    
    records_to_keep = []
    deleted_count = 0
    
    for record in table_data:
        is_match = True
        for column, value in where_clause.items():
            if column == "_operator":
                continue
                
            if column not in record:
                is_match = False
                break
                
            operator = where_clause.get("_operator", "=")
            record_value = record[column]
            condition_value = convert_value(value, type(record_value).__name__)
            
            if operator == "=":
                if record_value != condition_value:
                    is_match = False
                    break
            elif operator == ">":
                if record_value <= condition_value:
                    is_match = False
                    break
            elif operator == "<":
                if record_value >= condition_value:
                    is_match = False
                    break
            elif operator == ">=":
                if record_value < condition_value:
                    is_match = False
                    break
            elif operator == "<=":
                if record_value > condition_value:
                    is_match = False
                    break
        
        if is_match:
            deleted_count += 1
        else:
            records_to_keep.append(record)
    
    print(f'Удалено {deleted_count} записей.')
    return records_to_keep

def display_table_data(table_data, table_name):
    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return

    table = PrettyTable()
    table.field_names = table_data[0].keys()

    for record in table_data:
        table.add_row(record.values())

    print(f'\nТаблица "{table_name}":')
    print(table)


def validate_value_type(value, expected_type):
    try:
        if expected_type == 'int':
            int(value)
        elif expected_type == 'bool':
            if value.lower() not in VALID_BOOLEAN_VALUES:
                return False
        elif expected_type == 'str':
            str(value)
        return True
    except (ValueError, TypeError):
        return False


def convert_value(value, expected_type):
    if expected_type == 'int':
        return int(value)
    elif expected_type == 'bool':
        return value.lower() in ['true', '1']
    elif expected_type == 'str':
        return str(value)
    return value
