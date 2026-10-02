import pytest

import src.toolkit.calculator
import src.toolkit.errors


def test_calculate():
    assert src.toolkit.calculator.calculation(["2", "3", "+"]) == 5


def test_division_error():
    with pytest.raises(src.toolkit.errors.DivisionError):
        src.toolkit.calculator.validation(["2", "/", "0"])


def test_missing_operator_error():
    with pytest.raises(src.toolkit.errors.MissingOperatorError):
        src.toolkit.calculator.validation(["2", "2"])


def test_empty_expression_error():
    with pytest.raises(src.toolkit.errors.EmptyExpressionError):
        src.toolkit.calculator.validation([])


def test_missing_operand_error():
    with pytest.raises(src.toolkit.errors.MissingOperandError):
        src.toolkit.calculator.validation(["2", "+"])


def test_two_binary_operators_error():
    with pytest.raises(src.toolkit.errors.TwoBinaryOperatorsError):
        src.toolkit.calculator.validation(["2", "*", "*", "2"])


def test_unknown_sumbol_error():
    with pytest.raises(src.toolkit.errors.UnknownSymbolError):
        src.toolkit.calculator.validation(["2^2"])
