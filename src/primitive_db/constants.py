META_FILE = "db_meta.json"
DATA_DIR = "data"
SUPPORTED_TYPES = ["int", "str", "bool"]
ERROR_TABLE_EXISTS = 'Ошибка: Таблица "{}" уже существует.'
ERROR_TABLE_NOT_EXISTS = 'Ошибка: Таблица "{}" не существует.'
ERROR_COLUMN_COUNT = "Ошибка: Ожидается {} значений, получено {}."
ERROR_INVALID_TYPE = 'Ошибка: Неверный тип для столбца "{}". Ожидается {}.'
ERROR_INVALID_VALUE = 'Некорректное значение: "{}". Попробуйте снова.'
ERROR_INVALID_DATA_TYPE = 'Некорректный тип данных: "{}". Поддерживаемые типы: {}.'
WHERE_PATTERN = "column = value"
SET_PATTERN = "column = value"
COLUMN_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_]*:(int|str|bool)$'
TRUE_VALUES = ['true', '1']
FALSE_VALUES = ['false', '0']
VALID_BOOLEAN_VALUES = TRUE_VALUES + FALSE_VALUES
