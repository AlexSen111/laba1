import src.toolkit.errors


def unit_type(unit: str) -> int:
    """Функция, получающая на вход единицу измерения и выводящая её принадлежность к определённой группе

    Args:
        unit (str): Единица измерения

    Raises:
        UnknownUnitError: Если единица не принадлежит ни одной группе

    Returns:
        int: Принадлежность к группе единиц измерения
    """
    length: list = ["mm", "cm", "m", "km"]
    mass: list = ["g", "kg"]
    temp: list = ["c", "f", "k"]
    if unit.lower() in length:
        return 0
    elif unit.lower() in mass:
        return 1
    elif unit.lower() in temp:
        return 2
    else:
        raise src.toolkit.errors.UnknownUnitError(f"Ошибка: неправильная единица измерения: {unit}")


def converter(value: float, start_unit: str, end_unit: str) -> float:
    """Функция, принимающая на вход значение, начальную ед. измерения и конечную ед. измерения. Выводит значение в конечной ед. измерения

    Args:
        value (float): значение в начальной ед. измерения
        start_unit (str): то, откуда переводится значение
        end_unit (str): то, куда переводится значение

    Raises:
        IncompatibleUnitsError: Единицы измерения принадлежат к разным группам
        WrongTemperatureError: Введённая температура ниже абсолютного нуля
        WrongValueError: Введённая длина отрицательна
        WrongValueError: Введённая масса отрицательна

    Returns:
        float: Значение в конечной ед. измерения
    """
    start_unit = start_unit.lower()
    end_unit = end_unit.lower()
    if unit_type(start_unit) != unit_type(end_unit):
        raise src.toolkit.errors.IncompatibleUnitsError(
            f"Ошибка: несовместимые единицы измерения: {start_unit} и {end_unit}"
        )
    elif start_unit == "c" and value < -273.15:
        raise src.toolkit.errors.WrongTemperatureError("Ошибка: введённая температура в цельсиях ниже абсолютного нуля")
    elif start_unit == "k" and value < 0:
        raise src.toolkit.errors.WrongTemperatureError(
            "Ошибка: введённая температура в кельвинах ниже абсолютного нуля"
        )
    elif start_unit == "f" and value < -459.67:
        raise src.toolkit.errors.WrongTemperatureError(
            "Ошибка: введённая температура в фаренгейтах ниже абсолютного нуля"
        )
    elif unit_type(start_unit) == 0 and value < 0:
        raise src.toolkit.errors.WrongValueError(f"Ошибка: длина в {start_unit} не может быть отрицательной")
    elif unit_type(start_unit) == 1 and value < 0:
        raise src.toolkit.errors.WrongValueError(f"Ошибка: масса в {start_unit} не может быть отрицательной")
    else:
        if start_unit == "c" and end_unit == "f":
            return value * 1.8 + 32
        elif start_unit == "f" and end_unit == "c":
            return (value - 32) * (5 / 9)
        elif start_unit == "c" and end_unit == "k":
            return value + 273.15
        elif start_unit == "k" and end_unit == "c":
            return value - 273.15
        elif start_unit == "f" and end_unit == "k":
            return (value - 32) * (5 / 9) + 273.15
        elif start_unit == "k" and end_unit == "f":
            return (value - 273.15) * 1.8 + 32
        elif start_unit == "g" and end_unit == "kg":
            return value / 1000
        elif start_unit == "kg" and end_unit == "g":
            return value * 1000
        elif start_unit == "mm" and end_unit == "cm":
            return value / 10
        elif start_unit == "mm" and end_unit == "m":
            return value / 1000
        elif start_unit == "mm" and end_unit == "km":
            return value / 1_000_000
        elif start_unit == "cm" and end_unit == "mm":
            return value * 10
        elif start_unit == "cm" and end_unit == "m":
            return value / 100
        elif start_unit == "cm" and end_unit == "km":
            return value / 100_000
        elif start_unit == "m" and end_unit == "mm":
            return value * 1000
        elif start_unit == "m" and end_unit == "cm":
            return value * 100
        elif start_unit == "m" and end_unit == "km":
            return value / 1000
        elif start_unit == "km" and end_unit == "mm":
            return value * 1_000_000
        elif start_unit == "km" and end_unit == "cm":
            return value * 100_000
        elif start_unit == "km" and end_unit == "m":
            return value * 1000
