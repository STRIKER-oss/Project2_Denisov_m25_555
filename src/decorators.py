import functools
import time
from typing import Any, Callable

import prompt


def handle_db_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: Обращение к несуществующему ключу - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации данных: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Ошибка: Файл не найден - {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None
    return wrapper


def confirm_action(action_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            message = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            confirmation = prompt.string(message)
            if confirmation.lower() != 'y':
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")
        return result
    return wrapper


def validate_table_exists(metadata: dict) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(table_name: str, *args, **kwargs) -> Any:
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                return None
            return func(table_name, *args, **kwargs)
        return wrapper
    return decorator
