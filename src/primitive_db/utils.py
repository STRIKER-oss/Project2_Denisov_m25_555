#!/usr/bin/env python3

import json
import re


def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при загрузке метаданных: {e}")
        return {}


def save_metadata(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Ошибка при сохранении метаданных: {e}")
        return False


def validate_column_definition(column_def):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*:(int|str|bool)$'
    return bool(re.match(pattern, column_def))


def validate_data_type(data_type):
    return data_type in ['int', 'str', 'bool']


def parse_table_creation_args(args):
    if len(args) < 3:
        return None, "Недостаточно аргументов"
    
    table_name = args[1]
    columns = args[2:]
    return table_name, columns
