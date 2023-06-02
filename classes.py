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

    def rearrange(self) -> Any:
        """Rearrange the expression."""
        return NotImplementedError

    def __lt__(self, other) -> bool:
        """Return whether self is less than other."""
        type_to_priority = {'Power': 6, 'Exponential': 5, 'Function': 4, 'Other': 3, 'Non-digit': 2, 'Digit': 1}
        self_type, self_base, self_exponent, self_coefficient, self_function_name = get_arrangement_type(self)
        other_type, other_base, other_exponent, other_coefficient, other_function_name = get_arrangement_type(other)
        if type_to_priority[self_type] < type_to_priority[other_type]:
            return True
        elif type_to_priority[self_type] > type_to_priority[other_type]:
            return False
        else:
            if self_type == 'Power':
                if self_exponent < other_exponent:
                    return True
                elif self_exponent > other_exponent:
                    return False
                # At this point, self_exponent == other_exponent
                elif self_coefficient < other_coefficient:
                    return True
                elif self_coefficient > other_coefficient:
                    return False
                # At this point, self_coefficient == other_coefficient:
            elif self_type == 'Exponential':
                if self_base < other_base:
                    return True
                elif self_base > other_base:
                    return False
                # At this point, self_base == other_base:
                elif self_exponent < other_exponent:
                    return True
                elif self_exponent > other_exponent:
                    return False
                # At this point, self_exponent == other_exponent
                elif self_coefficient < other_coefficient:
                    return True
                elif self_coefficient > other_coefficient:
                    return False
                # At this point, self_coefficient == other_coefficient:
            elif self_type == 'Function':
                if self_function_name < other_function_name:
                    return True
                elif self_function_name > other_function_name:
                    return False
                # At this point, self_function_name == other_function_name:
                elif self_exponent < other_exponent:
                    return True
                elif self_exponent > other_exponent:
                    return False
                # At this point, self_exponent == other_exponent
                elif self_coefficient < other_coefficient:
                    return True
                elif self_coefficient > other_coefficient:
                    return False
                # At this point, self_coefficient == other_coefficient:
            elif self_type == 'Non-digit':
                self_list = process_to_list(self_base)
                other_list = process_to_list(other_base)

                # todo: loop through the lists

            elif self_type == 'Digit':
                if isinstance(self_base, Const) and isinstance(other_base, Const):
                    return self_base.name < other_base.name
            return False


class BinOp(Expr):
    """An abstract class representing a binary operation.

    Instance Attributes:
        - left: the expression to the left of the operator
        - right: the expression to the right of the operator
    """
    left: Expr
    right: Expr

    def __init__(self, left: Expr, right: Expr) -> None:
        self.left = left
        self.right = right


class Num(Expr):
    """An abstract class representing a number (constant or variable).

    Instance Attributes:
        - num: the number the Num object represents.
    """
    name: Any

    def __init__(self, name: Any) -> None:
        self.name = name

    def __str__(self) -> str:
        return str(self.name)


class Func(Expr):
    """An abstract class representing a mathematical function.

    Instance Attributes:
        - arg: the argument of the function
    """
    arg: Expr

    def __init__(self, arg: Expr) -> None:
        self.arg = arg


class Plus(BinOp):
    """Represents the binary operation of adding two expressions.

    Instance Attributes:
        - left: the expression to the left of the plus sign
        - right: the expression to the right of the plus sign
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' + ' + str(self.right) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        return Plus(self.left.differentiate(respect_to), self.right.differentiate(respect_to))

    def simplify(self) -> Expr:
        # self.left == self.right
        if str(self.left) == str(self.right):
            return Multiply(Const(2), self.left.simplify()).simplify()
        # self.left is Num(0)
        if isinstance(self.left, Const) and self.left.name == 0:
            return self.right.simplify()
        # self.right is Num(0)
        if isinstance(self.right, Const) and self.right.name == 0:
            return self.left.simplify()
        # Num + Num
        if isinstance(self.left, Const) and isinstance(self.right, Const):
            return Const(self.left.name + self.right.name)

        # Multiply + Multiply
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply):
            #           +
            #          / \
            #         *   *
            #        /\   /\
            #       a  b c  d
            # Case 1: a and c are the same object
            if str(self.left.left) == str(self.right.left):
                return Multiply(Plus(self.left.right.simplify(), self.right.right.simplify()).simplify(),
                                self.left.left.simplify())  # .simplify()
            # Case 2: a and d are the same object
            if str(self.left.left) == str(self.right.right):
                return Multiply(Plus(self.left.right.simplify(), self.right.left.simplify()).simplify(),
                                self.left.left.simplify())  # .simplify()
            # Case 3: b and c are the same object
            if str(self.left.right) == str(self.right.left):
                return Multiply(Plus(self.left.left.simplify(), self.right.right.simplify()).simplify(),
                                self.left.right.simplify())  # .simplify()
            # Case 4: b and d are the same object
            if str(self.left.right) == str(self.right.right):
                return Multiply(Plus(self.left.left.simplify(), self.right.left.simplify()).simplify(),
                                self.left.right.simplify())  # .simplify()

        # # Multiply + Expr or Expr + Multiply
        # if isinstance(self.left, Multiply) or isinstance(self.right, Multiply):
        #     result = Plus(self.left.simplify(), self.right.simplify()).simplify()

        # Plus + Plus or Plus + Expr or Expr + Plus
        # if isinstance(self.left, Plus) or isinstance(self.right, Plus):
        #     return Plus(self.left.simplify(), self.right.simplify()).simplify()

        return Plus(self.left.simplify(), self.right.simplify())

    def rearrange(self) -> Expr:
        """Rearrange the Plus expression."""

        # Step 1: Insert all the non-Plus Expr objects into a list
        lst = expr_to_list(self)
        # assert(len(lst) >= 2)

        # Step 2: Sort the list
        lst.sort()

        # Step 3: Insert all the objects into a new Plus binary tree
        tree = Plus(lst[0], lst[1])
        for i in range(2, len(lst)):
            tree = Plus(tree, lst[i])

        return tree

def expr_to_list(obj: Expr) -> list:
    """"""


class Multiply(BinOp):
    """Represents the binary operation of multiplying two expressions.

    Instance Attributes:
        - left: the expression to the left of the times sign
        - right: the expression to the right of the times sign
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        return '(' + str(self.left) + ' * ' + str(self.right) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if isinstance(self.left, Const) and not isinstance(self.right, Const):
            return Multiply(self.left, self.right.differentiate(respect_to))

        if isinstance(self.right, Const) and not isinstance(self.left, Const):
            return Multiply(self.right, self.left.differentiate(respect_to))

        return Plus(Multiply(self.left.differentiate(respect_to), self.right),
                    Multiply(self.left, self.right.differentiate(respect_to)))

    def simplify(self) -> Expr:
        if isinstance(self.left, Const):
            if self.left.name == 1:
                return self.right.simplify()
            elif self.left.name == 0:
                return Const(0)

        if isinstance(self.right, Const):
            if self.right.name == 1:
                return self.left.simplify()
            elif self.right.name == 0:
                return Const(0)

        if str(self.left) == str(self.right):
            return Power(self.left.simplify(), Const(2))

        if isinstance(self.left, Const) and isinstance(self.right, Const) and not isinstance(self.left.name, str) \
                and not isinstance(self.right.name, str):
            return Const(self.left.name * self.right.name)

        # Power * Power with same bases
        if isinstance(self.left, Power) and isinstance(self.right, Power) \
                and str(self.left.left) == str(self.right.left):
            return Power(self.left.left.simplify(),
                         Plus(self.left.right.simplify(), self.right.right.simplify()).simplify())

        # <some_type> * (<some_type> * Expr)
        if isinstance(self.right, Multiply) and type(self.left) == type(self.right.left):
            return Multiply(Multiply(self.left.simplify(),
                                     self.right.left.simplify()).simplify(), self.right.right.simplify())  # .simplify()

        # <some_type> * (Expr * <some_type>)
        if isinstance(self.right, Multiply) and type(self.left) == type(self.right.right):
            return Multiply(Multiply(self.left.simplify(),
                                     self.right.right.simplify()).simplify(), self.right.left.simplify())  # .simplify()

        # (<some_type> * Expr) * <some_type>
        if isinstance(self.left, Multiply) and type(self.right) == type(self.left.left):
            return Multiply(Multiply(self.right.simplify(), self.left.left.simplify()).simplify(),
                            self.left.right.simplify())  # .simplify()

        # (Expr * <some_type>) * <some_type>
        if isinstance(self.left, Multiply) and type(self.right) == type(self.left.right):
            return Multiply(Multiply(self.right.simplify(), self.left.right.simplify()).simplify(),
                            self.left.left.simplify())  # .simplify()

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
                                Multiply(self.left.right.simplify(), self.right.right.simplify()).simplify())  # .simplify()
            # Case 2: a and d are the same type
            if type(self.left.left) == type(self.right.right):
                return Multiply(Multiply(self.left.left.simplify(), self.right.right.simplify()).simplify(),
                                Multiply(self.left.right.simplify(), self.right.left.simplify()).simplify())  # .simplify()
            # Case 3: b and c are the same type
            if type(self.left.right) == type(self.right.left):
                return Multiply(Multiply(self.left.right.simplify(), self.right.left.simplify()).simplify(),
                                Multiply(self.left.left.simplify(), self.right.right.simplify()).simplify())  # .simplify()
            # Case 4: b and d are the same type
            if type(self.left.right) == type(self.right.right):
                return Multiply(Multiply(self.left.right.simplify(), self.right.right.simplify()).simplify(),
                                Multiply(self.left.left.simplify(), self.right.left.simplify()).simplify())  # .simplify()

        return Multiply(self.left.simplify(), self.right.simplify())


class Const(Num):
    """Represents a constant number.

    Instance Attributes:
        - name: the number self represents
            - 'e' represents Euler's number
            - 'pi' represents π (the ratio of a circle's circumference to its diameter)
    """
    name: int | float | str

    def __init__(self, name: int | float | str) -> None:
        super().__init__(name)

    def differentiate(self, respect_to: str) -> Expr:
        return Const(0)

    def simplify(self) -> Expr:
        return self


class Power(BinOp):
    """Represents the binary operation of exponentiation (power).

    Instance Attributes:
        - left: the base of the power
        - right: the exponent of the power
    """
    def __init__(self, base: Expr, exponent: Expr) -> None:
        try:
            if isinstance(base, Const) and base.name == 0 and isinstance(exponent, Const) and exponent.name < 0:
                raise ZeroDivisionError
            super().__init__(base, exponent)
        except ZeroDivisionError:
            print('You may not divide by zero. Please try again!')

    def __str__(self) -> str:
        return '(' + str(self.left) + ')^' + '(' + str(self.right) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if isinstance(self.left, Const) and isinstance(self.right, Const):
            return Const(0)

        # Power rule
        if not isinstance(self.left, Const) and isinstance(self.right, Const) \
                and (isinstance(self.right.name, int) or (isinstance(self.right.name, float))):
            return Multiply(Multiply(self.right,
                                     Power(self.left, Const(self.right.name - 1))), self.left.differentiate(respect_to))

        # e ^ f(x)
        if isinstance(self.left, Const) and self.left.name == 'e':
            return Multiply(self, self.right.differentiate(respect_to))

        # Const ^ f(x)
        if isinstance(self.left, Const):
            return Multiply(self, Multiply(Log(Const('e'), self.left), self.right.differentiate(respect_to)))

    def simplify(self) -> Expr:
        return Power(self.left.simplify(), self.right.simplify())


class Var(Num):
    """Represents a single variable.

    Instance Attributes:
        - name: the name of the variable
    """
    name: str

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def differentiate(self, respect_to: str) -> Expr:
        if respect_to == self.name:
            return Const(1)
        else:
            return Const(0)

    def simplify(self) -> Expr:
        return self


class Trig(Func):
    """Represents a trigonometric function.

    Instance Attributes:
        - name: the name of the trig function
        - arg: the argument passed into the trig function

    Representation Invariants:
        - self.name in {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'arcsin', 'arccos', 'arctan'}
    """
    name: str
    arg: Expr
    VALID_NAMES = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'arcsin', 'arccos', 'arctan'}

    def __init__(self, name: str, arg: Expr) -> None:
        try:
            if name not in self.VALID_NAMES:
                raise TrigError
            self.name = name
            super().__init__(arg)
        except TrigError as error:
            print(error.msg)

    def __str__(self) -> str:
        return self.name + '(' + str(self.arg) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if self.name == 'sin':
            return Multiply(Trig('cos', self.arg),
                            self.arg.differentiate(respect_to)
                            )
        if self.name == 'cos':
            return Multiply(Const(-1),
                            Multiply(Trig('sin', self.arg),
                                     self.arg.differentiate(respect_to)
                                     )
                            )
        if self.name == 'tan':
            return Multiply(Power(Trig('sec', self.arg), Const(2)),
                            self.arg.differentiate(respect_to)
                            )
        if self.name == 'sec':
            return Multiply(Trig('sec', self.arg),
                            Multiply(Trig('tan', self.arg),
                                     self.arg.differentiate(respect_to)
                                     )
                            )
        if self.name == 'csc':
            return Multiply(Const(-1),
                            Multiply(Trig('csc', Var('x')),
                                     Multiply(Trig('cot', Var('x')),
                                              self.arg.differentiate(respect_to)
                                              )
                                     )
                            )
        if self.name == 'cot':
            return Multiply(Const(-1),
                            Multiply(Power(Trig('csc', self.arg), Const(2)),
                                     self.arg.differentiate(respect_to)
                                     )
                            )

        if self.name == 'arcsin':
            return Multiply(self.arg.differentiate(respect_to),
                            Power(Plus(Const(1),
                                       Multiply(Const(-1),
                                                Power(self.arg,
                                                      Const(2)))), Const(-0.5))
                            )
        if self.name == 'arccos':
            return Multiply(Const(-1), Trig('arcsin', self.arg).differentiate(respect_to))
        if self.name == 'arctan':
            return Multiply(self.arg.differentiate(respect_to),
                            Power(Plus(Power(self.arg, Const(2)), Const(1)), Const(-1))
                            )

    def simplify(self) -> Expr:
        return Trig(self.name, self.arg.simplify())


class Log(Func):
    """Represents a logarithmic function.

    Instance Attributes:
        - base: the base of the logarithm
        - arg: the argument of the logarithm

    Representation Invariants:
        - isinstance(self.base, Num)
    """
    base: Const
    arg: Expr

    def __init__(self, base: Const, arg: Expr) -> None:
        try:
            if isinstance(arg, Const) and arg.name == 0:
                raise LogZeroError
            self.base = base
            super().__init__(arg)
        except LogZeroError as error:
            print(error.msg)

    def __str__(self) -> str:
        if self.base.name == 'e':
            return 'ln(' + str(self.arg) + ')'
        else:
            return 'log' + str(self.base) + '(' + str(self.arg) + ')'

    def differentiate(self, respect_to: str) -> Expr:
        if not isinstance(self.arg, Const):
            if self.base.name == 'e':
                return Multiply(self.arg.differentiate(respect_to), Power(self.arg, Const(-1)))
            else:
                return Multiply(self.arg.differentiate(respect_to),
                                Power(Multiply(self.arg, Log(Const('e'), self.base)), Const(-1))
                                )
        else:
            # Then it is a constant!
            return Const(0)

    def simplify(self) -> Expr:
        if self.base.name == 'e' and isinstance(self.arg, Const) and self.arg.name == 'e':
            return Const(1)
        return Log(self.base, self.arg.simplify())


class LogZeroError(Exception):
    """Raised when the user attempts to define log(0).

    Instance Attributes:
        - msg: the error message
    """
    msg: str

    def __init__(self) -> None:
        self.msg = 'You cannot define log(0). Please try again!'


class TrigError(Exception):
    """Raised when the user tries to define an undefined trigonometric function.

    Instance Attributes:
        - msg: the error message
    """
    msg: str

    def __init__(self) -> None:
        self.msg = 'The entered trigonometric function does not exist. Please try again!'
