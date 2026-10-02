class ConverterError(Exception):
    pass


class UnknownUnitError(ConverterError):
    pass


class IncompatibleUnitsError(ConverterError):
    pass


class WrongTemperatureError(ConverterError):
    pass


class WrongValueError(ConverterError):
    pass


class CalculatorError(Exception):
    pass


class DivisionError(CalculatorError):
    pass


class TwoBinaryOperatorsError(CalculatorError):
    pass


class EmptyExpressionError(CalculatorError):
    pass


class MissingOperatorError(CalculatorError):
    pass


class UnknownSymbolError(CalculatorError):
    pass


class MissingOperandError(CalculatorError):
    pass
