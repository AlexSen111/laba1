from re import findall

import src.toolkit.errors


def unary_operators(user_input: str) -> str:
    """Функция, принимающая входную строку и заменяющая унарные операторы в ней

    Args:
        user_input (str): входная строка

    Returns:
        str: выходная строка с изменёнными унарными операторами
    """
    bin_and_un_plus: str = (
        r"(?=([0-9]+[*, /, //, %, +, -][+][0-9]+))"  # проверка последовательностей вида число<оператор>+число
    )
    negative_case_plus = r"[*, /, //, %, +, -][+]+"  # здесь я проверяю, чтобы последовательность из бинарного и унарного не встречалась >1 раза между числами
    bin_and_un_minus = r"(?=([0-9]+[*, /, //, %, +, -][-][0-9]+))"  # аналогично плюсу
    negative_case_minus = r"[*, /, //, %, +, -][-]+"  # аналогично плюсу
    valid_plus = findall(bin_and_un_plus, user_input)
    invalid_plus = findall(negative_case_plus, user_input)
    if len(valid_plus) == len(invalid_plus):  # если все последовательности валидные, то можно их заменить
        user_input = (
            user_input.replace("*+", "*")
            .replace("-+", "-")
            .replace("//+", "//")
            .replace("/+", "/")
            .replace("%+", "%")
            .replace("++", "+")
        )
    valid_minus = findall(bin_and_un_minus, user_input)
    invalid_minus = findall(negative_case_minus, user_input)
    if len(valid_minus) == len(invalid_minus):
        user_input = (
            user_input.replace("/-", "/u-")
            .replace("*-", "*u-")
            .replace("--", "+")
            .replace("+-", "-")
            .replace("//-", "//u-")
            .replace("%-", "%u-")
        )
    return user_input


def tokenization(user_input: str) -> list:
    """Функция, получающая на вход строку (с заменёнными унарными операторами) и токенизирующая её (разбивает на числа и операторы)

    Args:
        user_input (str): входная строка с заменёнными унарными операторами

    Returns:
        list: список из токенов (чисел и операторов)
    """
    tokenized_input: list = (
        user_input.replace("u-", "u")
        .replace("+", " + ")
        .replace("-", " - ")
        .replace("*", " * ")
        .replace("%", " % ")
        .replace("//", "i_d")
        .replace("/", " / ")
        .replace("i_d", " // ")
        .replace("u", " u- ")
        .split()
    )
    if tokenized_input[0] == "-" and len(tokenized_input) > 1 and tokenized_input[1] not in "+-*/%":
        tokenized_input[0] = tokenized_input[0] + tokenized_input[1]
        tokenized_input.pop(1)
    elif tokenized_input[0] == "+" and len(tokenized_input) > 1 and tokenized_input[1] not in "+-*/%":
        tokenized_input.pop(0)
    if "u-" in tokenized_input:
        a = tokenized_input.index("u-")
        tokenized_input[a] = "-" + tokenized_input[a + 1]
        tokenized_input.pop(a + 1)
    # каюсь, оставил часть обработки унарных знаков в токенизации, потому что не понял, как их нормально сделать в функции unary_operators
    return tokenized_input


def validation(tokenized_input: list):
    """Функция, принимающая токенизированный вход и проверяющая валидность выражения

    Args:
        tokenized_input (list): список токенов

    Raises:
        EmptyExpressionError: Если пустое выражение
        MissingOperandError: Выражение состоит только из операторов
        MissingOperandError: Пропущен один из операндов
        UnknownSymbolError: Выражение имеет недопустимый символ
        DivisionError: В выражении присутствует деление (/, //, %) на 0
        TwoBinaryOperatorsError: Выражение имеет два бинарных оператора подряд
        MissingOperatorError: Пропущен оператор между операндами
    """
    if len(tokenized_input) == 0:
        raise src.toolkit.errors.EmptyExpressionError("Ошибка: пустое выражение")
    if all([i in "+-*/%" for i in tokenized_input]):
        raise src.toolkit.errors.MissingOperandError("Ошибка: отсутствуют операнды(числа)")
    if tokenized_input[0] not in ["+", "-", "//", "*", "%", "/"] and tokenized_input[-1] in [
        "+",
        "-",
        "//",
        "*",
        "%",
        "/",
    ]:
        raise src.toolkit.errors.MissingOperandError("Ошибка: отсутствует операнд")
    for a in tokenized_input:
        for j in a:
            if j not in "0123456789+-*/%":
                raise src.toolkit.errors.UnknownSymbolError("Ошибка: недопустимый символ")
    for i in range(len(tokenized_input) - 1):
        if tokenized_input[i] in ["/", "//", "%"] and tokenized_input[i + 1] == "0":
            raise src.toolkit.errors.DivisionError("Ошибка: деление на ноль запрещено")
        if tokenized_input[i] in ["*", "/", "//", "%", "+", "-"] and tokenized_input[i + 1] in [
            "*",
            "/",
            "//",
            "%",
            "+",
            "-",
        ]:
            raise src.toolkit.errors.TwoBinaryOperatorsError("Ошибка: два бинарных оператора подряд")
        if tokenized_input[i] not in ["*", "/", "//", "%", "+", "-"] and tokenized_input[i + 1] not in [
            "*",
            "/",
            "//",
            "%",
            "+",
            "-",
        ]:
            raise src.toolkit.errors.MissingOperatorError("Ошибка: отсутствует оператор между числами")


def convert_to_postfix(tokenized_input: list) -> list:
    """Функция, получающая выражение в виде списка в инфиксной записи и преобразовывающая её в постфиксную

    Args:
        tokenized_input (list): Список токенов

    Returns:
        list: Список токенов, преобразованных в постфиксную запись
    """
    operation_priorities: dict = {"+": 1, "-": 1, "*": 2, "/": 2, "//": 2, "%": 2}
    stack: list = []
    postfix_output: list = []
    for token in tokenized_input:
        if token in operation_priorities:
            oper_priority: int = operation_priorities[token]
            while len(stack) > 0:
                top: int = stack[-1]
                top_priority: int = operation_priorities[top]
                if top_priority >= oper_priority:
                    postfix_output.append(stack.pop())
                else:
                    break
            stack.append(token)
        else:
            postfix_output.append(token)
    while len(stack) > 0:
        postfix_output.append(stack.pop())
    return postfix_output


def calculation(postfix_input: list) -> float | int:
    """Функция, получающая выражение в постфиксной записи и выводящая его значение

    Args:
        postfix_input (list): Выражение в постфиксной нотации

    Returns:
        float | int: Ответ
    """
    stack: list = []
    for token in postfix_input:
        if token in ["+", "//", "*", "/", "%", "-"]:
            right_operand: int | float = stack.pop()
            left_operand: int | float = stack.pop()
            if token == "+":
                stack.append(left_operand + right_operand)
            elif token == "-":
                stack.append(left_operand - right_operand)
            elif token == "/":
                stack.append(left_operand / right_operand)
            elif token == "*":
                stack.append(left_operand * right_operand)
            elif token == "//":
                stack.append(left_operand // right_operand)
            elif token == "%":
                stack.append(left_operand % right_operand)
        else:
            stack.append(float(token) if "." in token else int(token))
    return stack[0]
