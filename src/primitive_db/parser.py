import shlex


def parse_where_condition(where_string):
    if not where_string:
        return None

    try:
        where_string = where_string.replace("WHERE", "").strip()
        
        operators = ['>=', '<=', '>', '<', '=']
        operator = None
        
        for op in operators:
            if op in where_string:
                operator = op
                break
        
        if not operator:
            msg = "Ошибка: Некорректный формат условия WHERE."
            msg += " Используйте: column оператор value"
            print(msg)
            return None

        parts = where_string.split(operator, 1)
        if len(parts) != 2:
            msg = "Ошибка: Некорректный формат условия WHERE."
            msg += " Используйте: column оператор value"
            print(msg)
            return None

        column = parts[0].strip()
        value = parts[1].strip()
        
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        
        return {column: value, "_operator": operator}
    except Exception as error:
        print(f"Ошибка разбора условия WHERE: {error}")
        return None


def parse_set_clause(set_string):
    if not set_string:
        return None

    try:
        set_string = set_string.replace("SET", "").strip()
        set_clause = {}

        clauses = set_string.split(',')
        for clause in clauses:
            clause = clause.strip()
            if '=' not in clause:
                msg = "Ошибка: Некорректный формат условия SET."
                msg += " Используйте: column = value"
                print(msg)
                return None

            parts = clause.split('=', 1)
            if len(parts) != 2:
                print("Ошибка: Некорректный формат условия SET.")
                return None

            column = parts[0].strip()
            value = parts[1].strip()
            
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
                
            set_clause[column] = value

        return set_clause
    except Exception as error:
        print(f"Ошибка разбора условия SET: {error}")
        return None


def parse_insert_values(values_string):
    if not values_string:
        return []

    try:
        return shlex.split(values_string)
    except ValueError as error:
        print(f"Ошибка разбора значений: {error}")
        return None
