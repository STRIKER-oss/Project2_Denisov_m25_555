#!/usr/bin/env python3
import json
import os
import re

from .constants import (
    COLUMN_PATTERN,
    DATA_DIR,
    META_FILE,
    SUPPORTED_TYPES,
)


def load_metadata():
    try:
        with open(META_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, IOError):
        return {}


def save_metadata(data):
    try:
        with open(META_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def load_table_data(table_name):
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError):
        return []


def save_table_data(table_name, data):
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def validate_column_definition(column_definition):
    return bool(re.match(COLUMN_PATTERN, column_definition))


def validate_data_type(data_type):
    return data_type in SUPPORTED_TYPES


def parse_table_creation_args(arguments):
    if len(arguments) < 3:
        return None, "Недостаточно аргументов"

    table_name = arguments[1]
    columns = arguments[2:]
    return table_name, columns
