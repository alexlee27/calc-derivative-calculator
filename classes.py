"""Classes for mathematical expressions"""
from typing import *


class Expr:
    """An abstract class representing a mathematial expression.
    """
    def __str__(self) -> Any:
        return NotImplementedError

    def differentiate(self, respect_to: str) -> Any:
        """Differentiate the expression.
        """
        return NotImplementedError


class Plus(Expr):
    """Represents the binary operation of adding two expressions.

    Instance Attributes:
        - left: the expression to the left of the plus sign
        - right: the expression to the right of the plus sign
    """
    left: Expr
    right: Expr

    def __init__(self, left: Expr, right: Expr) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return '(' + str(self.left) + ' + ' + str(self.right) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        return Plus(self.left.differentiate(respect_to), self.right.differentiate(respect_to))


class Multiply(Expr):
    """Represents the binary operation of multiplying two expressions.

    Instance Attributes:
        - left: the expression to the left of the times sign
        - right: the expression to the right of the times sign
    """
    left: Expr
    right: Expr

    def __init__(self, left: Expr, right: Expr) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return '(' + str(self.left) + ' * ' + str(self.right) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if isinstance(self.left, Num) and not isinstance(self.right, Num):
            return Multiply(self.left, self.right.differentiate(respect_to))

        if isinstance(self.right, Num) and not isinstance(self.left, Num):
            return Multiply(self.right, self.left.differentiate(respect_to))

        return Plus(Multiply(self.left.differentiate(respect_to), self.right), Multiply(self.left, self.right.differentiate(respect_to)))


class Num(Expr):
    """Represents a constant number.

    Instance Attributes:
        - n: the number self represents
    """
    n: int | float | str

    def __init__(self, n: int | float | str) -> None:
        self.n = n

    def __str__(self) -> str:
        return str(self.n)

    def differentiate(self, respect_to: str) -> Expr:
        return Num(0)


class Power(Expr):
    """Represents a power.

    Instance Attributes:
        - base: the base of the power
        - exponent: the exponent of the power
    """
    base: Expr
    exponent: Expr

    def __init__(self, base: Expr, exponent: Expr) -> None:
        self.base = base
        self.exponent = exponent

    def __str__(self) -> str:
        return '(' + str(self.base) + ')^' + str(self.exponent)

    def differentiate(self, respect_to: str) -> Expr:
        if isinstance(self.base, Num) and isinstance(self.exponent, Num):
            return self

        # Power rule
        if not isinstance(self.base, Num) and isinstance(self.exponent, Num) and isinstance(self.exponent.n, int):
            return Multiply(Multiply(self.exponent, Power(self.base, Num(self.exponent.n - 1))), self.base.differentiate(respect_to))


class Var(Expr):
    """Represents a single variable.

    Instance Attributes:
        - var: the name of the variable
    """
    var: str

    def __init__(self, var: str) -> None:
        self.var = var

    def __str__(self) -> str:
        return self.var

    def differentiate(self, respect_to: str) -> Expr:
        if respect_to == self.var:
            return Num(1)
        else:
            return self


class Trig(Expr):
    """Represents a trigonometric function.

    Instance Attributes:
        - name: the name of the trig function
        - param: the parameter passed into the trig function

    Representation Invariants:
        - self.name in {'sin', 'cos', 'tan', 'sec', 'csc', 'cot'}
    """
    name: str
    param: Expr

    def __init__(self, name: str, param: Expr) -> None:
        self.name = name
        self.param = param

    def __str__(self) -> str:
        return self.name + '(' + str(self.param) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if self.name == 'sin':
            return Multiply(Trig('cos', self.param), self.param.differentiate(respect_to))
        if self.name == 'cos':
            return Multiply(Multiply(Num(-1), Trig('cos', self.param)), self.param.differentiate(respect_to))
        if self.name == 'tan':
            return Multiply(Power(Trig('sec', self.param), Num(2)), self.param.differentiate(respect_to))
        # Implement sec csc cot as well
