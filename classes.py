"""Classes for mathematical expressions"""
from typing import *


class Expr:
    """An abstract class representing a mathematial expression.
    """
    def __str__(self) -> Any:
        return NotImplementedError

    def differentiate(self, respect_to: str) -> Any:
        """Differentiate the expression."""
        return NotImplementedError

    def simplify(self) -> Any:
        """Simplify the expression."""
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

    def simplify(self) -> Expr:
        # self.left == self.right
        if str(self.left) == str(self.right):
            return Multiply(Num(2), self.left.simplify()).simplify()
        # self.left is Num(0)
        if isinstance(self.left, Num) and self.left.n == 0:
            return self.right.simplify()
        # self.right is Num(0)
        if isinstance(self.right, Num) and self.right.n == 0:
            return self.left.simplify()
        # Num + Num
        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.left.n + self.right.n)

        # Multiply + Multiply
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply):
            #           +
            #          / \
            #         *   *
            #        /\   /\
            #       a  b c  d
            # Case 1: a and c are the same object
            if str(self.left.left) == str(self.right.left):
                return Multiply(Plus(self.left.right.simplify(), self.right.right.simplify()).simplify(), self.left.left.simplify()).simplify()
            # Case 2: a and d are the same object
            if str(self.left.left) == str(self.right.right):
                return Multiply(Plus(self.left.right.simplify(), self.right.left.simplify()).simplify(), self.left.left.simplify()).simplify()
            # Case 3: b and c are the same object
            if str(self.left.right) == str(self.right.left):
                return Multiply(Plus(self.left.left.simplify(), self.right.right.simplify()).simplify(), self.left.right.simplify()).simplify()
            # Case 4: b and d are the same object
            if str(self.left.right) == str(self.right.right):
                return Multiply(Plus(self.left.left.simplify(), self.right.left.simplify()).simplify(), self.left.right.simplify()).simplify()

        # Multiply + Expr or Expr + Multiply
        if isinstance(self.left, Multiply) or isinstance(self.right, Multiply):
            return Plus(self.left.simplify(), self.right.simplify()).simplify()

        # Plus + Plus or Plus + Expr or Expr + Plus
        if isinstance(self.left, Plus) or isinstance(self.right, Plus):
            return Plus(self.left.simplify(), self.right.simplify()).simplify()

        return Plus(self.left.simplify(), self.right.simplify())


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

    def simplify(self) -> Expr:
        if isinstance(self.left, Num):
            if self.left.n == 1:
                return self.right.simplify()
            elif self.left.n == 0:
                return Num(0)

        if isinstance(self.right, Num):
            if self.right.n == 1:
                return self.left.simplify()
            elif self.right.n == 0:
                return Num(0)

        if str(self.left) == str(self.right):
            return Power(self.left.simplify(), Num(2))

        if isinstance(self.left, Num) and isinstance(self.right, Num):
            return Num(self.left.n * self.right.n)

        # Power * Power with same bases
        if isinstance(self.left, Power) and isinstance(self.right, Power) and str(self.left.base) == str(self.right.base):
            return Power(self.left.base.simplify(), Plus(self.left.exponent.simplify(), self.right.exponent.simplify()).simplify())

        # <some_type> * (<some_type> * Expr)
        if isinstance(self.right, Multiply) and type(self.left) == type(self.right.left):
            return Multiply(Multiply(self.left.simplify(), self.right.left.simplify()).simplify(), self.right.right.simplify()).simplify()

        # <some_type> * (Expr * <some_type>)
        if isinstance(self.right, Multiply) and type(self.left) == type(self.right.right):
            return Multiply(Multiply(self.left.simplify(), self.right.right.simplify()).simplify(), self.right.left.simplify()).simplify()

        # (<some_type> * Expr) * <some_type>
        if isinstance(self.left, Multiply) and type(self.right) == type(self.left.left):
            return Multiply(Multiply(self.right.simplify(), self.left.left.simplify()).simplify(),
                            self.left.right.simplify()).simplify()

        # (Expr * <some_type>) * <some_type>
        if isinstance(self.left, Multiply) and type(self.right) == type(self.left.right):
            return Multiply(Multiply(self.right.simplify(), self.left.right.simplify()).simplify(),
                            self.left.left.simplify()).simplify()

        # Multiply * Multiply
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply):
            #           *
            #          / \
            #         *   *
            #        /\   /\
            #       a  b c  d
            # Case 1: a and c are the same type
            if type(self.left.left) == type(self.right.left):
                return Multiply(Multiply(self.left.left.simplify(), self.right.left.simplify()).simplify(),
                                Multiply(self.left.right.simplify(), self.right.right.simplify()).simplify()).simplify()
            # Case 2: a and d are the same type
            if type(self.left.left) == type(self.right.right):
                return Multiply(Multiply(self.left.left.simplify(), self.right.right.simplify()).simplify(),
                                Multiply(self.left.right.simplify(), self.right.left.simplify()).simplify()).simplify()
            # Case 3: b and c are the same type
            if type(self.left.right) == type(self.right.left):
                return Multiply(Multiply(self.left.right.simplify(), self.right.left.simplify()).simplify(),
                                Multiply(self.left.left.simplify(), self.right.right.simplify()).simplify()).simplify()
            # Case 4: b and d are the same type
            if type(self.left.right) == type(self.right.right):
                return Multiply(Multiply(self.left.right.simplify(), self.right.right.simplify()).simplify(),
                                Multiply(self.left.left.simplify(), self.right.left.simplify()).simplify()).simplify()

        return Multiply(self.left.simplify(), self.right.simplify())


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

    def simplify(self) -> Expr:
        return self


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

    def simplify(self) -> Expr:
        return Power(self.base.simplify(), self.exponent.simplify())


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

    def simplify(self) -> Expr:
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

    def simplify(self) -> Expr:
        return Trig(self.name, self.param.simplify())
