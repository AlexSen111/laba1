import sys

import src.toolkit.errors

from src.toolkit.calculator import calculation
from src.toolkit.calculator import convert_to_postfix
from src.toolkit.calculator import tokenization
from src.toolkit.calculator import unary_operators
from src.toolkit.calculator import validation
from src.toolkit.converter import converter
from src.toolkit.converter import unit_type


def main() -> None:
    """if len(sys.argv) < 3:
    print("Usage:")
    print('  python -m toolkit calc "EXPRESSION"')
    print("  python -m toolkit convert VALUE --from UNIT --to UNIT")
    print("  python -m toolkit --help")
    sys.exit(0)"""

    command: str = sys.argv[1].lower()
    if command == "convert":
        if len(sys.argv) < 7:
            print("Ошибка: недостаточно входных данных", file=sys.stderr)
            print("Правильное использование конвертера: python -m toolkit convert VALUE --from UNIT --to UNIT")
            sys.exit(2)
        else:
            value: float = float(sys.argv[2])
            start_unit: str = sys.argv[4]
            end_unit: str = sys.argv[6]
        try:
            unit_type(start_unit)
            unit_type(end_unit)
            try:
                answer = converter(value, start_unit, end_unit)
                print(answer)
            except src.toolkit.errors.IncompatibleUnitsError as e:
                print(f"{e}", file=sys.stderr)
                sys.exit(2)
            except src.toolkit.errors.WrongTemperatureError as e:
                print(f"{e}", file=sys.stderr)
                sys.exit(2)
        except src.toolkit.errors.UnknownUnitError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
    elif command == "calc":
        expression: str = sys.argv[2]
        unary_handling: str = unary_operators(expression)
        tokenize: list = tokenization(unary_handling)
        try:
            validation(tokenize)
            to_postfix: list = convert_to_postfix(tokenize)
            answer: float | int = calculation(to_postfix)
            print(answer)
        except src.toolkit.errors.DivisionError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
        except src.toolkit.errors.TwoBinaryOperatorsError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
        except src.toolkit.errors.EmptyExpressionError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
        except src.toolkit.errors.MissingOperatorError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
        except src.toolkit.errors.UnknownSymbolError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
        except src.toolkit.errors.MissingOperandError as e:
            print(f"{e}", file=sys.stderr)
            sys.exit(2)
    elif command == "--help":
        print("Toolkit CLI")
        print("Допустимые команды:")
        print('calc "EXPRESSION" - Рассчитать математическое выражение (Важно: EXPRESSION вызывается в кавычках)')
        print("convert VALUE --from UNIT --to UNIT - Конвертировать значение между единицами измерения")
        print("--help - Вызвать данное диалоговое окно")
    else:
        print(f"Ошибка: неизвестная команда {command}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
