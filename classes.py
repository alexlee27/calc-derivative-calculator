"""Classes for mathematical expressions"""
from __future__ import annotations
from typing import *


# todo: run a bunch of test cases for Plus.simplify, Plus.rearrange, Multiply.simplify, and Multiply.rearrange
# x ^ e, x ^ pi, x ^ x works
# Func ^ f(x) (e.g. ( ln ( e ) ) ^ x ) works
# Func ^ Func (e.g. ( cos ( 1 ) ) ^ sin ( 1 ) ) works
# filtered fractions in Multiply objects
# (-1) ^ x, -1 ^ x, -(1 ^ x); fixed how input deals with negative signs with non-digits
# 0 ^ Func and 0 ^ f(x) simplifies to 0
# sorted by argument first for (trig) functions
# implemented e ^ ln x = x simplification; a ^ (... * loga x * ...) = x ^ ... simplification (an O(n) algorithm that looks through all nodes in the exponent?)
# implemented logx ( x )????
# used gcd for fraction simplification
# created new method call 'trig_simplify'
# made it so non-constants can be used in logarithm base
# implemented logarithm rules
# implemented something + ( -1 * something ) = 0 simplification
# implemented a ^ (b + c) = a^b * a^c (where b + c can't be simplified)
# implemented simplification of a + b/c, a/b + c
# detected a/b as digit
# debugged -x^3 -1 -1
# enabled clearing steps in html
# debugged simplification/trig simplification for sin(x)+cos(x)+tan(x)+cot(x)+csc(x)+sec(x)
# implemented differentiation for powers with fraction exponents
# implemented arrangement order for a/b
# todo: arccsc, arcsec, arccot


class Expr:
    """An abstract class representing a mathematial expression.
    """

    def __str__(self) -> str:
        raise NotImplementedError

    # def __len__(self) -> int:
    #     """Returns the number of leaves in the Expr tree."""
    #     raise NotImplementedError

    def get_latex(self) -> str:
        """Get the LaTeX code for the expression."""
        raise NotImplementedError

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        """Differentiate the expression."""
        raise NotImplementedError

    def simplify(self, expand: bool) -> Expr:
        """Simplify the expression.
        If expand is True, it will expand terms as well (e.g. expanding multinomials, distribution in multiplication).
        """
        return self

    def rearrange(self) -> Expr:
        """Rearrange the expression."""
        return self

    def trig_simplify(self) -> Expr:
        """Simplify any trigonometric functions."""
        return self

    def fractionify(self) -> Expr:
        """Put any terms with negative exponents in the denominators of fractions."""
        return self

    def __lt__(self, other) -> bool:
        """Return whether self is less (lower priority) than other."""
        type_to_priority = {'Power': 6, 'Exponential': 5, 'Function': 4, 'Other': 3, 'Non-digit': 2, 'Digit': 1}
        self_type, self_base, self_exponent, self_coefficient, self_function_name, self_function_arg = get_arrangement_type(
            self)
        other_type, other_base, other_exponent, other_coefficient, other_function_name, other_function_arg = get_arrangement_type(
            other)
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
                if self_function_arg < other_function_arg:
                    return True
                elif self_function_arg > other_function_arg:
                    return False
                # At this point, self_function_arg is same object as other_function_arg
                # For exponents: other types > int > float
                elif isinstance(self_exponent, Const) and isinstance(other_exponent, Const) and isinstance(
                        self_exponent.name, float) and isinstance(other_exponent.name, int):
                    return True
                elif isinstance(self_exponent, Const) and isinstance(other_exponent, Const) and isinstance(
                        self_exponent.name, int) and isinstance(other_exponent.name, float):
                    return False
                elif isinstance(self_exponent, Const) and isinstance(self_exponent.name, int) and not_int_or_float(
                        other_exponent):
                    return True
                elif not_int_or_float(self_exponent) and isinstance(other_exponent, Const) and isinstance(
                        other_exponent.name, int):
                    return False
                elif isinstance(self_exponent, Const) and isinstance(self_exponent.name, float) and not_int_or_float(
                        other_exponent):
                    return True
                elif not_int_or_float(self_exponent) and isinstance(other_exponent, Const) and isinstance(
                        other_exponent.name, float):
                    return False
                # At this point, self_exponent and other_exponent are both float, int, or something else
                elif func_name_priority(self_function_name) < func_name_priority(other_function_name):
                    return True
                elif func_name_priority(self_function_name) > func_name_priority(other_function_name):
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
            elif self_type == 'Other':
                pass
            elif self_type == 'Non-digit':
                # print('inside __lt__')
                self_list = process_to_list(self_base)
                other_list = process_to_list(other_base)
                # print(str(self_base))
                # print(str(other_base))
                # print(self_list)
                # print(other_list)

                i = 0
                while i < len(self_list) and i < len(other_list):
                    if self_list[i][0] > other_list[i][0]:  # Note that 'b' > 'a' evaluates to True
                        # print('2nd one has higher priority')
                        return True
                    elif self_list[i][0] == other_list[i][0]:  # Bases are the same; look at exponents
                        if (isinstance(self_list[i][1], int) or isinstance(self_list[i][1], float)) and \
                                (isinstance(other_list[i][1], int) or isinstance(other_list[i][1], float)):
                            if self_list[i][1] < other_list[i][1]:  # Note that 2 < 3 evaluates to True
                                # print('2nd one has higher priority')
                                return True
                            if self_list[i][1] > other_list[i][1]:
                                # print('1st one has higher priority')
                                return False
                        if isinstance(self_list[i][1], str) and isinstance(other_list[i][1], str):
                            if self_list[i][1] > other_list[i][1]:  # Note that 'b' > 'a' evaluates to True
                                # print('2nd one has higher priority')
                                return True
                            if self_list[i][1] < other_list[i][1]:
                                # print('1st one has higher priority')
                                return False
                        if not isinstance(self_list[i][1], str) and isinstance(other_list[i][1], str):
                            # Alphabets take precedence over digits
                            # print('2nd one has higher priority')
                            return True
                        if isinstance(self_list[i][1], str) and not isinstance(other_list[i][1], str):
                            # Alphabets take precedence over digits
                            # print('1st one has higher priority')
                            return False
                    elif self_list[i][0] < other_list[i][0]:
                        # print('1st one has higher priority')
                        return False
                    i += 1
            elif self_type == 'Digit':
                # Const == Const * (Const ^ -1) > Const ^ Digit > Const ^ Non-digit
                if isinstance(self, Pow) and isinstance(other, Pow):
                    self_exp_type = get_arrangement_type(self_exponent)[0]
                    other_exp_type = get_arrangement_type(other_exponent)[0]
                    if self_exp_type == 'Non-digit' and other_exp_type == 'Digit':
                        return True
                    elif self_exp_type == 'Digit' and other_exp_type == 'Non-digit':
                        return False
                if isinstance(self, Pow) and isinstance(other, Const):
                    return True
                if isinstance(self, Const) and isinstance(other, Pow):
                    return False
                if isinstance(self, Pow) and isinstance(other, Multiply):
                    return True
                if isinstance(self, Multiply) and isinstance(other, Pow):
                    return False
                # At this point, both (Const or a/b) or Const ^ Digit or Const ^ Non-digit
                # Converting a/b into a float
                if isinstance(self_base, Multiply) and isinstance(self_base.left, Const) and \
                        isinstance(self_base.left.name, int) and \
                        isinstance(self_base.right, Pow) and isinstance(self_base.right.left, Const) and \
                        isinstance(self_base.right.left.name, int) and isinstance(self_base.right.right, Const) and \
                        self_base.right.right.name == -1:
                    self_base = Const(self_base.left.name / self_base.right.left.name)

                # Converting a/b into a float
                if isinstance(other_base, Multiply) and isinstance(other_base.left, Const) and \
                        isinstance(other_base.left.name, int) and \
                        isinstance(other_base.right, Pow) and isinstance(other_base.right.left, Const) and \
                        isinstance(other_base.right.left.name, int) and isinstance(other_base.right.right, Const) and \
                        other_base.right.right.name == -1:
                    other_base = Const(other_base.left.name / other_base.right.left.name)

                if isinstance(self_base, Const) and isinstance(other_base, Const):
                    if self_base.name < other_base.name:
                        return True
                    if self_base.name > other_base.name:
                        return False
                    if isinstance(self, Pow):
                        if self_exponent < other_exponent:
                            return True
                        elif self_exponent > other_exponent:
                            return False

                # if isinstance(self, Pow) and isinstance(other, Const):
                #     return True
                # if isinstance(self, Const) and isinstance(other, Pow):
                #     return False
                # if isinstance(self_base, Const) and isinstance(other_base, Const):
                #     return self_base.name < other_base.name
            return False


def not_int_or_float(expr: Expr) -> bool:
    """Return true if expr does NOT represent an int or a float."""
    return not (isinstance(expr, Const) and (isinstance(expr.name, int) or isinstance(expr.name, float)))


def func_name_priority(name: str) -> int:
    """Returns the priority of the name of the function.
    sin > cos > tan > csc > sec > cot > arcsin > arccos > arctan > log.
    -1 is returned if name is an invalid function name.

    Preconditions:
        - name in {'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'arcsin', 'arccos', 'arctan', 'log'}
    """
    hashmap = {'sin': 10, 'cos': 9, 'tan': 8, 'csc': 7, 'sec': 6, 'cot': 5, 'arcsin': 4, 'arccos': 3, 'arctan': 2,
               'log': 1}
    if name in hashmap:
        return hashmap[name]
    return -1


# class Nothing(Expr):
#     """A class representing an Expr dummy holder."""
#
#     def __init__(self) -> None:
#         pass
#
#     def __str__(self) -> str:
#         return 'nothing '

class Diff(Expr):
    """A class for displaying d/dx[...] (where x is the variable of differentiation).
    Not used for actual calculations.

    Instance Attributes:
        - content: the Expr inside ...
        - variable_of_diff: the variable of differentiation
    """
    content: Expr
    variable_of_diff: str

    def __init__(self, content: Expr, variable_of_diff: str) -> None:
        self.content = content
        self.variable_of_diff = variable_of_diff

    def __str__(self) -> str:
        return 'd/d' + self.variable_of_diff + '[' + str(self.content) + ']'

    def get_latex(self) -> str:
        return '\\frac{d}{d' + self.variable_of_diff + '}\\left[' + self.content.get_latex() + '\\right]'


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

    # def __len__(self) -> int:
    #     return len(self.left) + len(self.right)


class Num(Expr):
    """An abstract class representing a number (constant or variable).

    Instance Attributes:
        - num: the number the Num object represents.
    """
    name: Any

    def __init__(self, name: Any) -> None:
        self.name = name

    def __str__(self) -> str:
        # if isinstance(self.name, float):
        #     result = f'{self.name:.7f}'
        #     i = len(result) - 1
        #     while result[i] == '0':
        #         i -= 1
        #     if result[i] == '.':
        #         return result[:i]
        #     else:
        #         return result[:i + 1]
        return str(self.name) + ' '

    # def __len__(self) -> int:
    #     return 1

    def get_latex(self) -> str:
        # if isinstance(self.name, float):
        #     result = f'{self.name:.7f}'
        #     i = len(result) - 1
        #     while result[i] == '0':
        #         i -= 1
        #     if result[i] == '.':
        #         return result[:i]
        #     else:
        #         return result[:i + 1]
        return str(self.name) + ' '


class Func(Expr):
    """An abstract class representing a mathematical function.

    Instance Attributes:
        - name: the name of the function
        - arg: the argument of the function
    """
    name: str
    arg: Expr

    def __init__(self, arg: Expr) -> None:
        self.arg = arg

    # def __len__(self) -> int:
    #     return len(self.arg)


class Plus(BinOp):
    """Represents the binary operation of adding two expressions.

    Instance Attributes:
        - left: the expression to the left of the plus sign
        - right: the expression to the right of the plus sign
    """
    num_non_plus: int = 0

    def __init__(self, left: Expr, right: Expr) -> None:
        super().__init__(left, right)
        if not isinstance(self.left, Plus):
            self.num_non_plus += 1
        else:
            self.num_non_plus += self.left.num_non_plus
        if not isinstance(self.right, Plus):
            self.num_non_plus += 1
        else:
            self.num_non_plus += self.right.num_non_plus

    def __str__(self) -> str:
        if isinstance(self.right, Const) and (isinstance(self.right.name, int) or isinstance(self.right.name, float)) \
                and self.right.name < 0:
            return '( ' + str(self.left) + '+ ( ' + str(self.right) + ') ) '
        return '( ' + str(self.left) + '+ ' + str(self.right) + ') '

    def get_latex(self) -> str:
        # self.right is a negative digit
        if isinstance(self.right, Const) and (isinstance(self.right.name, int) or isinstance(self.right.name, float)) \
                and self.right.name < 0:
            return self.left.get_latex() + ' ' + self.right.get_latex()

        # whatever + (negative digit * whatever)
        if isinstance(self.right, Multiply) and isinstance(self.right.left, Const) \
                and (isinstance(self.right.left.name, int) or isinstance(self.right.left.name, float)) \
                and self.right.left.name < 0:
            return self.left.get_latex() + ' ' + self.right.get_latex()

        return self.left.get_latex() + '+ ' + self.right.get_latex()

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if not isinstance(self.left, Plus) and not isinstance(self.right, Plus):
            steps = [(Plus(Diff(self.left, respect_to), Diff(self.right, respect_to)), 'Differentiation is linear; differentiate each of the summands: ',
                      f'\\displaystyle\\left[u_1({respect_to})+u_2({respect_to})+\\cdots+u_n({respect_to})\\right]\'=u_1\'({respect_to})+u_2\'({respect_to})+\\cdots+u_n\'({respect_to})')]
        else:
            steps = []
        left_differentiated, left_steps = self.left.differentiate(respect_to)
        right_differentiated, right_steps = self.right.differentiate(respect_to)
        for item in left_steps:
            steps.append((Plus(item[0], Diff(self.right, respect_to)), item[1], item[2]))
        for item in right_steps:
            steps.append((Plus(left_steps[-1][0], item[0]), item[1], item[2]))
        return Plus(left_differentiated, right_differentiated), steps

    def simplify(self, expand: bool) -> Expr:
        # self.left == self.right
        if str(self.left) == str(self.right):
            return Multiply(Const(2), self.left.simplify(expand)).simplify(expand)
        # self.left is Num(0)
        if isinstance(self.left, Const) and self.left.name == 0:
            return self.right.simplify(expand)
        # self.right is Num(0)
        if isinstance(self.right, Const) and self.right.name == 0:
            return self.left.simplify(expand)
        # Num + Num
        if isinstance(self.left, Const) and isinstance(self.right, Const) and \
                (isinstance(self.left.name, int) or isinstance(self.left.name, float)) and \
                (isinstance(self.right.name, int) or isinstance(self.right.name, float)):
            return Const(self.left.name + self.right.name)

        # something1 / expr + something2 / expr = (something1 + something2) / expr
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply) and \
                isinstance(self.left.right, Pow) and isinstance(self.right.right, Pow) and \
                isinstance(self.left.right.right, Const) and self.left.right.right.name == -1 and \
                str(self.left.right) == str(self.right.right):
            return Multiply(Plus(self.left.left.simplify(expand), self.right.left.simplify(expand)).simplify(expand),
                            self.left.right.simplify(expand)).simplify(expand)

        # a/b + c/d, where a, b, c, d are numbers
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply) and \
                isinstance(self.left.left, Const) and isinstance(self.left.left.name, int) and \
                isinstance(self.right.left, Const) and isinstance(self.right.left.name, int) and \
                isinstance(self.left.right, Pow) and isinstance(self.right.right, Pow) and \
                isinstance(self.left.right.left, Const) and isinstance(self.left.right.left.name, int) and \
                isinstance(self.left.right.right, Const) and self.left.right.right.name == -1 and \
                isinstance(self.right.right.left, Const) and isinstance(self.right.right.left.name, int) and \
                isinstance(self.right.right.right, Const) and self.right.right.right.name == -1:
            a, b, c, d = self.left.left.name, self.left.right.left.name, self.right.left.name, self.right.right.left.name
            common_denom = lcm(b, d)
            b_multiplier = common_denom // b
            d_multiplier = common_denom // d
            return Multiply(Const(a * b_multiplier + c * d_multiplier), Pow(Const(common_denom), Const(-1))).simplify(
                expand)

        # a + b/c, where a, b, c are numbers
        if isinstance(self.left, Const) and isinstance(self.left.name, int) and \
                isinstance(self.right, Multiply) and isinstance(self.right.left, Const) and \
                isinstance(self.right.left.name, int) and \
                isinstance(self.right.right, Pow) and isinstance(self.right.right.left, Const) and \
                isinstance(self.right.right.left.name, int) and \
                isinstance(self.right.right.right, Const) and self.right.right.right.name == -1:
            return Plus(Multiply(self.left, Pow(Const(1), Const(-1))), self.right).simplify(expand)

        # a/b + c, where a, b, c are numbers
        if isinstance(self.right, Const) and isinstance(self.right.name, int) and \
                isinstance(self.left, Multiply) and isinstance(self.left.left, Const) and \
                isinstance(self.left.left.name, int) and \
                isinstance(self.left.right, Pow) and isinstance(self.left.right.left, Const) and \
                isinstance(self.left.right.left.name, int) and \
                isinstance(self.left.right.right, Const) and self.left.right.right.name == -1:
            return Plus(self.left, Multiply(self.right, Pow(Const(1), Const(-1)))).simplify(expand)

        # if not expand:
        #     # something1 / expr1 + something2 / expr2 = (something1 * expr2 + something2 * expr1) / (expr1 * expr2)
        #     if isinstance(self.left, Multiply) and isinstance(self.right, Multiply) and \
        #             isinstance(self.left.right, Pow) and isinstance(self.right.right, Pow) and \
        #             isinstance(self.left.right.right, Const) and self.left.right.right.name == -1 and \
        #             isinstance(self.right.right.right, Const) and self.right.right.right.name == -1:
        #         expr1 = self.left.right.left.simplify(expand)
        #         expr2 = self.right.right.left.simplify(expand)
        #         return Multiply(Plus(Multiply(self.left.left.simplify(expand), expr2).simplify(expand),
        #                              Multiply(self.right.left.simplify(expand), expr1)),
        #                         Pow(Multiply(expr1, expr2).simplify(expand), Const(-1)).simplify(expand))

        # Multiply + Multiply
        if isinstance(self.left, Multiply) and isinstance(self.right, Multiply):
            #           +
            #          / \
            #         *   *
            #        /\   /\
            #       a  b c  d
            # Case 1: a and c are the same object
            if str(self.left.left) == str(self.right.left):
                factor_simplified = Plus(self.left.right.simplify(expand), self.right.right.simplify(expand)).simplify(
                    expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.left.simplify(expand))  # .simplify(expand)
            # Case 2: a and d are the same object
            if str(self.left.left) == str(self.right.right):
                factor_simplified = Plus(self.left.right.simplify(expand), self.right.left.simplify(expand)).simplify(
                    expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.left.simplify(expand))  # .simplify(expand)
            # Case 3: b and c are the same object
            if str(self.left.right) == str(self.right.left):
                factor_simplified = Plus(self.left.left.simplify(expand), self.right.right.simplify(expand)).simplify(
                    expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.right.simplify(expand))  # .simplify(expand)
            # Case 4: b and d are the same object
            if str(self.left.right) == str(self.right.right):
                factor_simplified = Plus(self.left.left.simplify(expand), self.right.left.simplify(expand)).simplify(
                    expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.right.simplify(expand))  # .simplify(expand)

        if isinstance(self.left, Multiply):
            #           +
            #          / \
            #         *   c
            #        /\
            #       a  b
            # Case 1: a and c are the same object
            if str(self.left.left) == str(self.right):
                factor_simplified = Plus(self.left.right.simplify(expand), Const(1)).simplify(expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.right.simplify(expand))

            # Case 2: b and c are the same object
            if str(self.left.right) == str(self.right):
                factor_simplified = Plus(self.left.left.simplify(expand), Const(1)).simplify(expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.right.simplify(expand))

        if isinstance(self.right, Multiply):
            #           +
            #          / \
            #         a   *
            #             /\
            #            b  c
            # Case 1: a and b are the same object
            if str(self.left) == str(self.right.left):
                factor_simplified = Plus(Const(1), self.right.right.simplify(expand)).simplify(expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.simplify(expand))

            # Case 2: a and c are the same object
            if str(self.left) == str(self.right.right):
                factor_simplified = Plus(Const(1), self.right.left.simplify(expand)).simplify(expand)
                if isinstance(factor_simplified, Const) and factor_simplified.name == 0:
                    return Const(0)
                if not expand:
                    return Multiply(factor_simplified, self.left.simplify(expand))

        #       +
        #      / \
        #     +   A
        #    / \
        #  ...  A      (where A is an arbitrary arrangement type)
        if isinstance(self.left, Plus) and not isinstance(self.right, Plus):
            if get_arrangement_type(self.left.right)[0] == get_arrangement_type(self.right)[0]:
                r_simplified = self.right.simplify(expand)
                lr_simplified = self.left.right.simplify(expand)
                lr_and_r_simplified = Plus(lr_simplified, r_simplified).simplify(expand)
                if str(lr_and_r_simplified) != str(Plus(lr_simplified, r_simplified)):
                    return Plus(self.left.left, lr_and_r_simplified).simplify(expand)
                else:
                    return Plus(self.left.simplify(expand), r_simplified)

        # # Multiply + Expr or Expr + Multiply
        # if isinstance(self.left, Multiply) or isinstance(self.right, Multiply):
        #     result = Plus(self.left.simplify(expand), self.right.simplify(expand)).simplify(expand)

        # Plus + Plus or Plus + Expr or Expr + Plus
        # if isinstance(self.left, Plus) or isinstance(self.right, Plus):
        #     return Plus(self.left.simplify(expand), self.right.simplify(expand)).simplify(expand)

        return Plus(self.left.simplify(expand), self.right.simplify(expand))

    def rearrange(self) -> Expr:
        """Rearrange the Plus expression."""

        # Step 1: Insert all the non-Plus Expr objects into a list
        old_lst = expr_to_list(self, self)
        # assert(len(lst) >= 2)
        lst = []
        for item in old_lst:
            lst.append(item.rearrange())
        # print([str(item) for item in lst])

        # Step 2: Sort the list
        lst.sort(reverse=True)

        # print([str(item) for item in lst])

        # Step 3: Insert all the objects into a new Plus binary tree
        tree = Plus(lst[0], lst[1])
        for i in range(2, len(lst)):
            tree = Plus(tree, lst[i])

        return tree

    def trig_simplify(self) -> Expr:
        return Plus(self.left.trig_simplify(), self.right.trig_simplify())

    def fractionify(self) -> Expr:
        return Plus(self.left.fractionify(), self.right.fractionify())


def expr_to_list(obj: Expr, root: BinOp) -> list:
    """Takes all descendants of obj that are not the same type as root, and puts them into a list.
    """
    if not isinstance(obj, type(root)):
        return [obj]
    else:
        return expr_to_list(obj.left, root) + expr_to_list(obj.right, root)


class Multiply(BinOp):
    """Represents the binary operation of multiplying two expressions.

    Instance Attributes:
        - left: the expression to the left of the times sign
        - right: the expression to the right of the times sign
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        if isinstance(self.right, Const) and (isinstance(self.right.name, int) or isinstance(self.right.name, float)) \
                and self.right.name < 0:
            return '( ' + str(self.left) + '* ( ' + str(self.right) + ') ) '
        return '( ' + str(self.left) + '* ' + str(self.right) + ') '

    def get_latex(self) -> str:
        if isinstance(self.left, Plus):
            left_latex = '\\left( ' + self.left.get_latex() + '\\right) '
        else:
            left_latex = self.left.get_latex()
        if isinstance(self.right, Pow) and isinstance(self.right.right, Const) and self.right.right.name == -1:
            return '\\frac{ ' + left_latex + '}{ ' + self.right.left.get_latex() + '} '

        right_latex = self.right.get_latex()
        if isinstance(self.right, Plus) or right_latex[0] == '-':
            right_latex = '\\left( ' + right_latex + '\\right) '

        # digit * not a digit
        if isinstance(self.left, Const) and (isinstance(self.left.name, int) or isinstance(self.left.name, float)):
            if not (isinstance(self.right, Const)
                    and (isinstance(self.right.name, int) or isinstance(self.right.name, float))):
                if self.left.name == -1:

                    return '- ' + right_latex
                else:
                    return left_latex + ' ' + right_latex
        return left_latex + '\\cdot ' + right_latex

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        left_type = get_arrangement_type(self.left)[0]
        right_type = get_arrangement_type(self.right)[0]
        if respect_to != 'c':
            constant_var = 'c'
        else:
            constant_var = 'a'
        if left_type in {'Non-digit', 'Digit'} and right_type in {'Non-digit', 'Digit'}:
            return Const(0), [(Const(0), 'The derivative of a constant is zero: ',
                              f'\\displaystyle {constant_var}\'=0')]

        if isinstance(self.left, Const) and not isinstance(self.right, Const):
            steps = [(Multiply(self.left, Diff(self.right, respect_to)), 'Differentiation is linear; pull out constant factors: ',
                      f'\\displaystyle\\left[{constant_var}\\cdot u({respect_to})\\right]\'={constant_var}\\cdot u\'({respect_to})')]
            right_differentiated, right_steps = self.right.differentiate(respect_to)
            for item in right_steps:
                steps.append((Multiply(self.left, item[0]), item[1], item[2]))
            return Multiply(self.left, right_differentiated), steps

        if isinstance(self.right, Const) and not isinstance(self.left, Const):
            steps = [(Multiply(self.right, Diff(self.left, respect_to)), 'Differentiation is linear; pull out constant factors: ',
                      f'\\displaystyle\\left[a\\{constant_var}dot u({respect_to})\\right]\'={constant_var}\\cdot u\'({respect_to})')]
            left_differentiated, left_steps = self.left.differentiate(respect_to)
            for item in left_steps:
                steps.append((Multiply(self.right, item[0]), item[1], item[2]))
            return Multiply(self.right, left_differentiated), steps

        def expand(expr: Multiply) -> Expr:
            """Expand the Multiply expression. Only used in Multiply.differentiate.
            """
            if isinstance(expr.left, Plus):
                return Plus(expand(Multiply(expr.left.left, expr.right)),
                            expand(Multiply(expr.left.right, expr.right)))
            if isinstance(expr.right, Plus):
                return Plus(expand(Multiply(expr.left, expr.right.left)),
                            expand(Multiply(expr.left, expr.right.right)))
            return expr

        if not isinstance(self.left, Multiply) and not isinstance(self.right, Multiply):
            steps = [(Plus(Multiply(Diff(self.left, respect_to), self.right),
                          Multiply(self.left, Diff(self.right, respect_to))), 'Apply the product rule: ',
                      f'\\displaystyle\\left[u_1({respect_to})\\cdot u_2({respect_to})\\cdots u_n({respect_to})\\right]\'=u_1\'({respect_to})\\cdot u_2({respect_to})\\cdots u_n({respect_to})+u_1({respect_to})\\cdot u_2\'({respect_to})\\cdots u_n({respect_to})+\\cdots+u_1({respect_to})\\cdot u_2({respect_to})\\cdots u_n\'({respect_to})')]
        else:
            steps = []

        left_differentiated, left_steps = self.left.differentiate(respect_to)
        right_differentiated, right_steps = self.right.differentiate(respect_to)
        for item in left_steps:
            steps.append((Plus(expand(Multiply(item[0], self.right)), Multiply(self.left, Diff(self.right, respect_to))), item[1], item[2]))
        left_expanded = expand(Multiply(left_steps[-1][0], self.right))
        for item in right_steps:
            steps.append((Plus(left_expanded, expand(Multiply(self.left, item[0]))), item[1], item[2]))

        return Plus(Multiply(left_differentiated, self.right),
                    Multiply(self.left, right_differentiated)), steps

    def simplify(self, expand: bool) -> Expr:
        # Preventing simplification of 1 * (something ^ -1) into (something ^ -1)
        # if isinstance(self.right, Pow) and isinstance(self.right.right, Const) and self.right.right.name == -1:
        #     if isinstance(self.left, Const) and self.left.name == 1:
        #         return Multiply(Const(1), Pow(self.right.left.simplify(expand), Const(-1)))
        if expand:
            if isinstance(self.left, Plus):
                right_simplified = self.right.simplify(expand)
                return Plus(Multiply(right_simplified, self.left.left.simplify(expand)),
                            Multiply(right_simplified, self.left.right.simplify(expand))).simplify(expand)
            if isinstance(self.right, Plus):
                left_simplified = self.left.simplify(expand)
                return Plus(Multiply(left_simplified, self.right.left.simplify(expand)),
                            Multiply(left_simplified, self.right.right.simplify(expand))).simplify(expand)

        if isinstance(self.left, Const):
            if self.left.name == 1:
                return self.right.simplify(expand)
            elif self.left.name == 0:
                return Const(0)

        if isinstance(self.right, Const):
            if self.right.name == 1:
                return self.left.simplify(expand)
            elif self.right.name == 0:
                return Const(0)

        if str(self.left) == str(self.right):
            return Pow(self.left.simplify(expand), Const(2))

        if isinstance(self.left, Const) and isinstance(self.right, Const) and not isinstance(self.left.name, str) \
                and not isinstance(self.right.name, str):
            return Const(self.left.name * self.right.name)

        # Pow * Pow
        if isinstance(self.left, Pow) and isinstance(self.right, Pow):
            # Same bases
            if str(self.left.left) == str(self.right.left):
                exponents_simplified = Plus(self.left.right.simplify(expand).fractionify(),
                                            self.right.right.simplify(expand).fractionify()).simplify(expand)
                # Adding fractionify for cases like 2 + 2 ^ (-1)

                # If the exponents can get simplified:
                if str(exponents_simplified) != str(Plus(self.left.right, self.right.right)):
                    return Pow(self.left.left.simplify(expand),
                               exponents_simplified)
            # Same exponents
            if str(self.left.right) == str(self.right.right):
                bases_simplified = Multiply(self.left.left.simplify(expand), self.right.left.simplify(expand)).simplify(
                    expand)
                # If the bases can get simplified
                if str(bases_simplified) != str(Multiply(self.left.left, self.right.left)):
                    return Pow(bases_simplified, self.left.right.simplify(expand))

        # (base ^ exp) * base
        if isinstance(self.left, Pow) and str(self.left.left) == str(self.right):
            exponents_simplified = Plus(self.left.right.simplify(expand).fractionify(), Const(1)).simplify(expand)
            # If the exponents can get simplified
            if str(exponents_simplified) != str(Plus(self.left.right, Const(1))):
                return Pow(self.right.simplify(expand), exponents_simplified)

        # base * (base ^ exp)
        if isinstance(self.right, Pow) and str(self.right.left) == str(self.left):
            exponents_simplified = Plus(self.right.right.simplify(expand).fractionify(), Const(1)).simplify(expand)
            # If the exponents can get simplified
            if str(exponents_simplified) != str(Plus(self.right.right, Const(1))):
                return Pow(self.left.simplify(expand), exponents_simplified)

        # # something * ( numerator / denominator) = (something * numerator) / denominator
        # if isinstance(self.right, Multiply) and isinstance(self.right.right, Pow) and \
        #         isinstance(self.right.right.right, Const) and self.right.right.right.name == -1:
        #

        # Simplifying n / m (fractions)
        if isinstance(self.left, Const) and isinstance(self.left.name, int) and isinstance(self.right, Pow) and \
                isinstance(self.right.left, Const) and isinstance(self.right.left.name, int) and \
                isinstance(self.right.right, Const) and self.right.right.name == -1:
            numerator = self.left.name
            denominator = self.right.left.name
            divisor = gcd(numerator, denominator)

            new_denominator = denominator // divisor
            if new_denominator == 1:
                return Const(numerator // divisor)
            else:
                return Multiply(Const(numerator // divisor), Pow(Const(new_denominator), Const(-1)))

        #       *
        #      / \
        #     *   A
        #    / \
        #  ...  A      (where A is an arbitrary arrangement type)
        if isinstance(self.left, Multiply) and not isinstance(self.right, Multiply):
            if get_arrangement_type(self.left.right)[0] == get_arrangement_type(self.right)[0]:
                r_simplified = self.right.simplify(expand)
                lr_simplified = self.left.right.simplify(expand)
                lr_and_r_simplified = Multiply(lr_simplified, r_simplified).simplify(expand)
                if str(lr_and_r_simplified) != str(Multiply(lr_simplified, r_simplified)):
                    return Multiply(self.left.left, lr_and_r_simplified).simplify(expand)
                else:
                    return Multiply(self.left.simplify(expand), r_simplified)

        #  # <some_type> * (<some_type> * Expr)
        # if isinstance(self.right, Multiply) and type(self.left) == type(self.right.left):
        #     return Multiply(Multiply(self.left.simplify(expand),
        #                              self.right.left.simplify(expand)).simplify(expand), self.right.right.simplify(expand))  # .simplify(expand)
        #
        # # <some_type> * (Expr * <some_type>)
        # if isinstance(self.right, Multiply) and type(self.left) == type(self.right.right):
        #     return Multiply(Multiply(self.left.simplify(expand),
        #                              self.right.right.simplify(expand)).simplify(expand), self.right.left.simplify(expand))  # .simplify(expand)
        #
        # # (<some_type> * Expr) * <some_type>
        # if isinstance(self.left, Multiply) and type(self.right) == type(self.left.left):
        #     return Multiply(Multiply(self.right.simplify(expand), self.left.left.simplify(expand)).simplify(expand),
        #                     self.left.right.simplify(expand))  # .simplify(expand)
        #
        # # (Expr * <some_type>) * <some_type>
        # if isinstance(self.left, Multiply) and type(self.right) == type(self.left.right):
        #     return Multiply(Multiply(self.right.simplify(expand), self.left.right.simplify(expand)).simplify(expand),
        #                     self.left.left.simplify(expand))  # .simplify(expand)

        # # Multiply * Multiply
        # if isinstance(self.left, Multiply) and isinstance(self.right, Multiply):
        #     # TODO: DEBUG FOR INPUT a * b * c * d * e ^ 999
        #
        #     #           *
        #     #          / \
        #     #         *   *
        #     #        /\   /\
        #     #       a  b c  d
        #     # Case 1: a and c are the same type
        #     if type(self.left.left) == type(self.right.left):
        #         return Multiply(Multiply(self.left.left.simplify(expand), self.right.left.simplify(expand)).simplify(expand),
        #                         Multiply(self.left.right.simplify(expand),
        #                                  self.right.right.simplify(expand)).simplify(expand))  # .simplify(expand)
        #     # Case 2: a and d are the same type
        #     if type(self.left.left) == type(self.right.right):
        #         return Multiply(Multiply(self.left.left.simplify(expand), self.right.right.simplify(expand)).simplify(expand),
        #                         Multiply(self.left.right.simplify(expand),
        #                                  self.right.left.simplify(expand)).simplify(expand))  # .simplify(expand)
        #     # Case 3: b and c are the same type
        #     if type(self.left.right) == type(self.right.left):
        #         return Multiply(Multiply(self.left.right.simplify(expand), self.right.left.simplify(expand)).simplify(expand),
        #                         Multiply(self.left.left.simplify(expand),
        #                                  self.right.right.simplify(expand)).simplify(expand))  # .simplify(expand)
        #     # Case 4: b and d are the same type
        #     if type(self.left.right) == type(self.right.right):
        #         return Multiply(Multiply(self.left.right.simplify(expand), self.right.right.simplify(expand)).simplify(expand),
        #                         Multiply(self.left.left.simplify(expand),
        #                                  self.right.left.simplify(expand)).simplify(expand))  # .simplify(expand)

        return Multiply(self.left.simplify(expand), self.right.simplify(expand))

    def rearrange(self) -> Any:
        """Rearrange the Multiply expression."""
        # Step 1: Insert all the non-Plus Expr objects into a list
        old_lst = expr_to_list(self, self)
        # assert(len(lst) >= 2)
        lst = []
        for item in old_lst:
            lst.append(item.rearrange())
        # print([str(item) for item in lst])

        # Step 2: Sort the list
        lst.sort(reverse=True)

        # print([str(item) for item in lst])

        # Step 3: Insert all the objects into a new Multiply binary tree
        #      *
        #     / \
        # coeff  *
        #       / \
        #     ... power

        i = 0
        if get_arrangement_type(lst[i])[0] == 'Power':  # Is it a Power?
            power_tree = Multiply(Const(1), lst[i])
            i += 1
            # Create power_tree
            power_tree, i, end_of_power = get_power_tree(i, lst, power_tree)

            if i == len(lst) and isinstance(end_of_power.left, Multiply):  # All items were Power objects
                if end_of_power:
                    end_of_power.left = end_of_power.left.right
                # if fractions:
                #     return Multiply(power_tree, Pow(fractions, Const(-1)))
                return power_tree
            elif get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:  # Is it a "Rest"?
                rest_tree = lst[i]
                i += 1
                # Create rest_tree
                rest_tree, i = get_rest_tree(i, lst, rest_tree)

                # Attach rest_tree to power_tree
                if end_of_power and isinstance(end_of_power.left, Multiply):
                    end_of_power.left.left = rest_tree
                else:  # If power_tree contains only 1 Power object
                    power_tree.left = rest_tree

                if i == len(lst):
                    return power_tree
                elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                    non_digit_tree = lst[i]
                    i += 1
                    # Create non_digit_tree
                    non_digit_tree, i = get_non_digit_tree(i, lst, non_digit_tree)
                    if i == len(lst):
                        # if fractions:
                        #     return Multiply(Multiply(non_digit_tree, power_tree), Pow(fractions, Const(-1)))
                        # else:
                        return Multiply(non_digit_tree, power_tree)
                    else:  # Must be a Digit
                        digit_tree = lst[i]
                        i += 1
                        # Create digit_tree
                        digit_tree = get_digit_tree(i, lst, digit_tree)
                        # if fractions:
                        #     return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), power_tree),
                        #                     Pow(fractions, Const(-1)))
                        # else:
                        return Multiply(Multiply(digit_tree, non_digit_tree), power_tree)
                else:  # Must be a Digit
                    digit_tree = lst[i]
                    i += 1
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    # if fractions:
                    #     return Multiply(Multiply(digit_tree, power_tree),
                    #                     Pow(fractions, Const(-1)))
                    # else:
                    return Multiply(digit_tree, power_tree)
            elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                if end_of_power and isinstance(end_of_power.left, Multiply):
                    end_of_power.left = end_of_power.left.right
                else:  # If power_tree contains only 1 Power object
                    power_tree = power_tree.right
                non_digit_tree = lst[i]
                i += 1
                # Create non_digit_tree
                non_digit_tree, i = get_non_digit_tree(i, lst, non_digit_tree)
                if i == len(lst):
                    # if fractions:
                    #     return Multiply(Multiply(non_digit_tree, power_tree), Pow(fractions, Const(-1)))
                    # else:
                    return Multiply(non_digit_tree, power_tree)
                else:  # Must be a Digit
                    digit_tree = lst[i]
                    i += 1
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    # if fractions:
                    #     return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), power_tree),
                    #                     Pow(fractions, Const(-1)))
                    # else:
                    return Multiply(Multiply(digit_tree, non_digit_tree), power_tree)
            else:  # Must be a digit tree
                if end_of_power and isinstance(end_of_power.left, Multiply):
                    end_of_power.left = end_of_power.left.right
                else:  # If power_tree contains only 1 Power object
                    power_tree = power_tree.right
                digit_tree = lst[i]
                i += 1
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                # if fractions:
                #     return Multiply(Multiply(digit_tree, power_tree), Pow(fractions, Const(-1)))
                # else:
                return Multiply(digit_tree, power_tree)
        elif get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:  # Is it a Rest?
            rest_tree = lst[i]
            i += 1
            # Create rest_tree
            rest_tree, i = get_rest_tree(i, lst, rest_tree)
            if i == len(lst):
                # if fractions:
                #     return Multiply(rest_tree, Pow(fractions, Const(-1)))
                # else:
                return rest_tree
            elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                non_digit_tree = lst[i]
                i += 1
                # Create non_digit_tree
                non_digit_tree, i = get_non_digit_tree(i, lst, non_digit_tree)
                if i == len(lst):
                    # if fractions:
                    #     return Multiply(Multiply(non_digit_tree, rest_tree), Pow(fractions, Const(-1)))
                    # else:
                    return Multiply(non_digit_tree, rest_tree)
                else:  # Must be a Digit
                    digit_tree = lst[i]
                    i += 1
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    # if fractions:
                    #     return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), rest_tree),
                    #                     Pow(fractions, Const(-1)))
                    # else:
                    return Multiply(Multiply(digit_tree, non_digit_tree), rest_tree)
            else:  # Must be a Digit
                digit_tree = lst[i]
                i += 1
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                # if fractions:
                #     return Multiply(Multiply(digit_tree, rest_tree), Pow(fractions, Const(-1)))
                # else:
                return Multiply(digit_tree, rest_tree)
        elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
            non_digit_tree = lst[i]
            i += 1
            # Create non_digit_tree
            non_digit_tree, i = get_non_digit_tree(i, lst, non_digit_tree)
            if i == len(lst):
                # if fractions:
                #     return Multiply(non_digit_tree, Pow(fractions, Const(-1)))
                # else:
                return non_digit_tree
            else:  # Must be a digit
                digit_tree = lst[i]
                i += 1
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                # if fractions:
                #     return Multiply(Multiply(digit_tree, non_digit_tree), Pow(fractions, Const(-1)))
                # else:
                return Multiply(digit_tree, non_digit_tree)
        else:  # Must be a Digit
            digit_tree = lst[i]
            i += 1
            # Create digit_tree
            digit_tree = get_digit_tree(i, lst, digit_tree)
            return digit_tree

        # todo: try using memoization??

        # # Deal with everything else... except for numbers (coefficients)
        #
        #     if i == len(lst):  # If the end of lst has been reached
        #         return power_tree
        #
        #     non_digit_tree = None
        #     if get_arrangement_type(lst[i])[0] == 'Non-digit':
        #         non_digit_tree = lst[i]
        #         i += 1
        #
        #     while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Non-digit':  # Fetching Non-digits first
        #         non_digit_tree = Multiply(non_digit_tree, lst[i])
        #         i += 1
        #
        #     if i == len(lst):  # If the end of lst has been reached
        #         return Multiply(non_digit_tree, power_tree)
        #
        # if not power_tree:  # If there are no Power objects
        #     ...

    def trig_simplify(self) -> Expr:
        # sin ^ n * cos ^ m
        if isinstance(self.left, Pow) and isinstance(self.right, Pow) and isinstance(self.left.left, Trig) and \
                isinstance(self.right.left, Trig):
            if self.left.left.name == 'sin' and self.right.left.name == 'cos' and str(self.left.left.arg) == str(
                    self.right.left.arg):
                arg = self.left.left.arg.trig_simplify()
                if isinstance(self.left.right, Const) and isinstance(self.left.right.name, int) and \
                        isinstance(self.right.right, Const) and isinstance(self.right.right.name, int):
                    sin_exp = self.left.right.name
                    cos_exp = self.right.right.name
                    sin_exp_abs = abs(sin_exp)
                    cos_exp_abs = abs(cos_exp)
                    if sin_exp > 0 and cos_exp < 0:
                        assert sin_exp_abs != 1
                        if sin_exp_abs > cos_exp_abs:
                            new_exp = sin_exp_abs - cos_exp_abs
                            if new_exp != 1:
                                left = Pow(Trig('sin', arg), Const(new_exp))
                            else:
                                left = Trig('sin', arg)
                            if cos_exp_abs != 1:
                                right = Pow(Trig('tan', arg), Const(cos_exp_abs))
                            else:
                                right = Trig('tan', arg)
                            return Multiply(left, right)
                        elif sin_exp_abs < cos_exp_abs:
                            new_exp = cos_exp_abs - sin_exp_abs
                            if new_exp != 1:
                                return Multiply(Pow(Trig('tan', arg), Const(sin_exp_abs)),
                                                Pow(Trig('sec', arg), Const(new_exp)))
                            else:
                                return Multiply(Pow(Trig('tan', arg), Const(sin_exp_abs)), Trig('sec', arg))
                        else:  # sin_exp_abs == cos_exp_abs
                            return Pow(Trig('tan', arg), Const(sin_exp_abs))
                    if sin_exp < 0 and cos_exp > 0:
                        assert cos_exp_abs != 1
                        if cos_exp_abs > sin_exp_abs:
                            new_exp = cos_exp_abs - sin_exp_abs
                            if new_exp != 1:
                                left = Pow(Trig('cos', arg), Const(new_exp))
                            else:
                                left = Trig('cos', arg)
                            if sin_exp_abs != 1:
                                right = Pow(Trig('cot', arg), Const(sin_exp_abs))
                            else:
                                right = Trig('cot', arg)
                            return Multiply(left, right)
                        elif cos_exp_abs < sin_exp_abs:
                            new_exp = sin_exp_abs - cos_exp_abs
                            if new_exp != 1:
                                return Multiply(Pow(Trig('csc', arg), Const(new_exp)),
                                                Pow(Trig('cot', arg), Const(cos_exp_abs)))
                            else:
                                return Multiply(Trig('csc', arg), Pow(Trig('cot', arg), Const(cos_exp_abs)))
                        else:  # sin_exp_abs == cos_exp_abs
                            return Pow(Trig('cot', arg), Const(sin_exp_abs))

        # sin * cos ^ n
        if isinstance(self.left, Trig) and isinstance(self.right, Pow) and isinstance(self.right.left, Trig):
            if self.left.name == 'sin' and self.right.left.name == 'cos' and str(self.left.arg) == str(
                    self.right.left.arg):
                arg = self.left.arg.trig_simplify()
                if isinstance(self.right.right, Const) and isinstance(self.right.right.name, int):
                    cos_exp = self.right.right.name
                    cos_exp_abs = abs(cos_exp)
                    if cos_exp < 0:
                        if cos_exp_abs > 1:
                            if cos_exp_abs - 1 != 1:
                                return Multiply(Trig('tan', arg), Pow(Trig('sec', arg), Const(cos_exp_abs - 1)))
                            else:
                                return Multiply(Trig('tan', arg), Trig('sec', arg))
                        elif cos_exp_abs == 1:
                            return Trig('tan', arg)
                        # Don't do anything for cos_exp_abs == 0

        # sin ^ n * cos
        if isinstance(self.left, Pow) and isinstance(self.left.left, Trig) and isinstance(self.right, Trig):
            if self.left.left.name == 'sin' and self.right.name == 'cos' and str(self.left.left.arg) == str(
                    self.right.arg):
                arg = self.right.arg.trig_simplify()
                if isinstance(self.left.right, Const) and isinstance(self.left.right.name, int):
                    sin_exp = self.left.right.name
                    sin_exp_abs = abs(sin_exp)
                    if sin_exp < 0:
                        if sin_exp_abs > 1:
                            if sin_exp_abs - 1 != 1:
                                return Multiply(Trig('cot', arg), Pow(Trig('csc', arg), Const(sin_exp_abs - 1)))
                            else:
                                return Multiply(Trig('cot', arg), Trig('csc', arg))
                        elif sin_exp_abs == 1:
                            return Trig('cot', arg)
                        # Don't do anything for sin_exp_abs == 0

        if isinstance(self.left, Multiply):
            lr_and_r_trig_simplified = Multiply(self.left.right, self.right).trig_simplify()
            if str(lr_and_r_trig_simplified) != str(Multiply(self.left.right, self.right)):
                return Multiply(self.left.left.trig_simplify(), lr_and_r_trig_simplified).trig_simplify()

        return Multiply(self.left.trig_simplify(), self.right.trig_simplify())

    def fractionify(self) -> Expr:
        numerator, denominator = filter_neg_powers(self)
        if denominator:
            if isinstance(denominator, Const) and denominator.name == 1:
                return numerator.fractionify()
            else:
                return Multiply(numerator.fractionify(), Pow(denominator.fractionify(), Const(-1)))
        return Multiply(self.left.fractionify(), self.right.fractionify())


def filter_neg_powers(expr: Expr) -> tuple[Expr, Optional[Expr]]:
    """Return a tuple in the form (numerator, denominator), where numerator is the modified expr object with all
    Pows with negative exponents removed, and denominator is an Expr object consisting of terms that should be in the
    denominator.
    """
    if not isinstance(expr, Multiply):
        if isinstance(expr, Pow):
            negative, abs_of_exponent = is_minus(expr.right)
            if negative:
                if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                    return Const(1), expr.left
                return Const(1), Pow(expr.left, abs_of_exponent)
        return expr, None
    else:
        left_numer, left_denom = filter_neg_powers(expr.left)
        right_numer, right_denom = filter_neg_powers(expr.right)
        if left_denom and right_denom:
            if isinstance(left_numer, Const) and left_numer.name == 1:
                return right_numer, Multiply(left_denom, right_denom)
            if isinstance(right_numer, Const) and right_numer.name == 1:
                return left_numer, Multiply(left_denom, right_denom)
            return Multiply(left_numer, right_numer), Multiply(left_denom, right_denom)
        elif left_denom:
            if isinstance(left_numer, Const) and left_numer.name == 1:
                return right_numer, left_denom
            if isinstance(right_numer, Const) and right_numer.name == 1:
                return left_numer, left_denom
            return Multiply(left_numer, right_numer), left_denom
        elif right_denom:
            if isinstance(left_numer, Const) and left_numer.name == 1:
                return right_numer, right_denom
            if isinstance(right_numer, Const) and right_numer.name == 1:
                return left_numer, right_denom
            return Multiply(left_numer, right_numer), right_denom
        # At this point, not left_denom and not right_denom
        else:
            if isinstance(left_numer, Const) and left_numer.name == 1:
                return right_numer, None
            if isinstance(right_numer, Const) and right_numer.name == 1:
                return left_numer, None
            return Multiply(left_numer, right_numer), None


def gcd(x, y) -> int:
    """Compute the greatest common divisor of x and y.
    """
    if y == 0:
        return abs(x)
    else:
        return gcd(y, x % y)


def lcm(x, y) -> int:
    """Compute the lowest common multiple of x and y.
    """
    d = gcd(x, y)
    return x * y // d


def get_power_tree(i: int, lst: list, power_tree: Expr) -> tuple:
    """Returns a tuple in the form of (power_tree, new_index, end_of_power).
    """
    end_of_power = None
    while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Power':
        # if isinstance(lst[i], Pow):
        #     negative, abs_of_exponent = is_minus(lst[i].right)
        #     if negative:
        #         if fractions is None:  # If this is the first fraction
        #             fractions = Pow(lst[i].left, abs_of_exponent)
        #         else:
        #             fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
        #     else:
        #         power_tree = Multiply(power_tree, lst[i])
        # else:
        power_tree = Multiply(power_tree, lst[i])
        if i == 1:
            end_of_power = power_tree
        i += 1
    return (power_tree, i, end_of_power)


def get_rest_tree(i: int, lst: list, rest_tree: Expr) -> tuple:
    """Returns a tuple in the form of (rest_tree, new_index)
    """
    while i < len(lst) and get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:
        # if isinstance(lst[i], Pow):
        #     negative, abs_of_exponent = is_minus(lst[i].right)
        #     if negative:
        #         if fractions is None:  # If this is the first fraction
        #             fractions = Pow(lst[i].left, abs_of_exponent)
        #         else:
        #             fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
        #     else:
        #         rest_tree = Multiply(rest_tree, lst[i])
        # else:
        rest_tree = Multiply(rest_tree, lst[i])
        i += 1
    return (rest_tree, i)


def get_non_digit_tree(i: int, lst: list, non_digit_tree: Expr) -> tuple:
    """Returns a tuple in the form of (non_digit_tree, new_index, fractions).
    """
    while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Non-digit':
        # if isinstance(lst[i], Pow):
        #     negative, abs_of_exponent = is_minus(lst[i].right)
        #     if negative:
        #         if fractions is None:  # If this is the first fraction
        #             fractions = Pow(lst[i].left, abs_of_exponent)
        #         else:
        #             fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
        #     else:
        #         non_digit_tree = Multiply(non_digit_tree, lst[i])
        # else:
        non_digit_tree = Multiply(non_digit_tree, lst[i])
        i += 1
    return (non_digit_tree, i)


def get_digit_tree(i: int, lst: list, digit_tree: Expr) -> Expr:
    """Returns an updated digit_tree."""
    while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Digit':
        digit_tree = Multiply(digit_tree, lst[i])
        i += 1
    return digit_tree


def is_minus(expr: Expr) -> tuple[bool, Expr]:  # todo: test
    """Returns a tuple in the form of (boolean, abs_value), where boolean is whether expr is negative, and
    abs_value is the absolute value of expr.

    Note: even if expr is, in fact, negative, if it is not simplified then it may not return True.
    """
    if isinstance(expr, Const) and (isinstance(expr.name, int) or isinstance(expr.name, float)) and expr.name < 0:
        return (True, Const(-expr.name))
    if isinstance(expr, Multiply):
        left_is_minus, left_abs_value = is_minus(expr.left)
        right_is_minus, right_abs_value = is_minus(expr.right)
        if left_is_minus and not right_is_minus:
            return (True, Multiply(left_abs_value, right_abs_value))
        elif right_is_minus and not left_is_minus:
            return (True, Multiply(left_abs_value, right_abs_value))
    return (False, expr)


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

    def get_latex(self) -> str:
        if self.name == 'pi':
            return '\\' + self.name + ' '
        else:
            return super().get_latex()

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if respect_to != 'c':
            constant_var = 'c'
        else:
            constant_var = 'a'
        return Const(0), [(Const(0), 'The derivative of a constant is zero: ', f'\\displaystyle {constant_var}\'=0')]

    def simplify(self, expand: bool) -> Expr:
        # if isinstance(self.name, float):
        #     numerator = round(self.name, 7)
        #     denominator = 1
        #     while numerator != round(numerator):
        #         numerator = round(numerator * 10, 7)
        #         denominator *= 10
        #     numerator = round(numerator)
        #     return Multiply(Const(numerator), Pow(Const(denominator), Const(-1)))
        return self


class Pow(BinOp):
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
        return '( ' + str(self.left) + ') ^ ( ' + str(self.right) + ') '

    def get_latex(self) -> str:
        # if isinstance(self.right, Const) and self.right.name == -1:
        #     return '\\frac{1}{ ' + self.left.get_latex() + '} '
        if isinstance(self.left, Trig):
            return '{ \\' + self.left.name + '} ' + '^' + '{ ' + self.right.get_latex() + '} ' + '\\left( ' + self.left.arg.get_latex() + '\\right) '
        if isinstance(self.left, Log):
            if isinstance(self.left.base, Const) and self.left.base.name == 'e':
                return '{ \\ln } ' + '^' + '{ ' + self.right.get_latex() + '} ' + '\\left( ' + self.left.arg.get_latex() + '\\right) '
            return '{\\log_{ ' + self.left.base.get_latex() + '} } ' + '^' + '{ ' + self.right.get_latex() + '} ' \
                + '\\left( ' + self.left.arg.get_latex() + '\\right) '
        if isinstance(self.left, Plus) or isinstance(self.left, Multiply) or isinstance(self.left, Pow) or \
                is_minus(self.left)[0]:
            left_latex = '\\left( ' + self.left.get_latex() + '\\right) '
        else:
            left_latex = self.left.get_latex()
        right_latex = self.right.get_latex()
        return '{ ' + left_latex + '} ' + '^ { ' + right_latex + '} '

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if respect_to != 'c':
            constant_var = 'c'
        else:
            constant_var = 'a'
        if isinstance(self.left, Const) and isinstance(self.right, Const):
            return Const(0), [(Const(0), 'The derivative of a constant is zero: ', f'\\displaystyle {constant_var}\'=0')]

        # Power rule for int or float exponents
        if not isinstance(self.left, Const) and isinstance(self.right, Const) \
                and (isinstance(self.right.name, int) or (isinstance(self.right.name, float))):
            steps = [(Multiply(Multiply(self.right,
                                       Pow(self.left, Const(self.right.name - 1))), Diff(self.left, respect_to)), 'Applying the power rule and chain rule: ',
                      f'\\displaystyle \\left[u^{{{constant_var}}}({respect_to})\\right]\'={constant_var}\\cdot u^{{{constant_var} - 1}}({respect_to})\\cdot u\'({respect_to})')]
            left_differentiated, left_steps = self.left.differentiate(respect_to)
            for item in left_steps:
                steps.append((Multiply(Multiply(self.right,
                                               Pow(self.left, Const(self.right.name - 1))), item[0]), item[1], item[2]))
            return Multiply(Multiply(self.right,
                                     Pow(self.left, Const(self.right.name - 1))), left_differentiated), steps

        # # Power rule for str exponents
        # if not isinstance(self.left, Const) and isinstance(self.right, Const) and isinstance(self.right.name, str):
        #     steps = [Multiply(Multiply(self.right,
        #                                Pow(self.left, Plus(self.right, Const(-1)))), Diff(self.left, respect_to))]
        #     left_differentiated, left_steps = self.left.differentiate(respect_to)
        #     for item in left_steps:
        #         steps.append(Multiply(Multiply(self.right,
        #                                        Pow(self.left, Plus(self.right, Const(-1)))), item))
        #     return Multiply(Multiply(self.right,
        #                              Pow(self.left, Plus(self.right, Const(-1)))), left_differentiated), steps

        base_type = get_arrangement_type(self.left)[0]
        exp_type = get_arrangement_type(self.right)[0]
        if exp_type in {'Non-digit', 'Digit'}:
            if base_type in {'Non-digit', 'Digit'}:
                return Const(0), [(Const(0), 'The derivative of a constant is zero: ', f'\\displaystyle {constant_var}\'=0')]
            else:
                steps = [(Multiply(Multiply(self.right, Pow(self.left, Plus(self.right, Const(-1)))), Diff(self.left, respect_to)), 'Applying the power rule and chain rule: ',
                      f'\\displaystyle \\left[u^{{{constant_var}}}({respect_to})\\right]\'={constant_var}\\cdot u^{{{constant_var} - 1}}({respect_to})\\cdot u\'({respect_to})')]
                left_differentiated, left_steps = self.left.differentiate(respect_to)
                for item in left_steps:
                    steps.append((Multiply(Multiply(self.right,
                                                   Pow(self.left, Plus(self.right, Const(-1)))), item[0]), item[1], item[2]))
                return Multiply(Multiply(self.right,
                                         Pow(self.left, Plus(self.right, Const(-1)))), left_differentiated), steps

        # e ^ f(x)
        if isinstance(self.left, Const) and self.left.name == 'e' and not isinstance(self.right, Const):
            steps = [(Multiply(self, Diff(self.right, respect_to)), 'Rule for differentiating exponentials and chain rule: ',
                      f'\\displaystyle \\left[e^{{u({respect_to})}}\\right]\'=e^{{u({respect_to})}}\\cdot u\'({respect_to})')]
            right_differentiated, right_steps = self.right.differentiate(respect_to)
            for item in right_steps:
                steps.append((Multiply(self, item[0]), item[1], item[2]))
            return Multiply(self, right_differentiated), steps

        # Const ^ f(x)
        if isinstance(self.left, Const) and not isinstance(self.right, Const):
            steps = [(Multiply(self, Multiply(Log(Const('e'), self.left), Diff(self.right, respect_to))),
                      'Rule for differentiating exponentials and chain rule: ',
                      f'\\displaystyle\\left[{{{constant_var}}}^{{u({respect_to})}}\\right]\'={{{constant_var}}}^{{u({respect_to})}}\\cdot \ln({constant_var})\\cdot u\'({respect_to})')]
            right_differentiated, right_steps = self.right.differentiate(respect_to)
            for item in right_steps:
                steps.append((Multiply(self, Multiply(Log(Const('e'), self.left), item[0])), item[1], item[2]))
            return Multiply(self, Multiply(Log(Const('e'), self.left), right_differentiated)), steps

        steps = [(Diff(Pow(Const('e'), Multiply(self.right, Log(Const('e'), self.left))), respect_to), 'Use the following identity: ',
                  f'\\displaystyle{{u_1({respect_to})}}^{{u_2({respect_to})}}=e^{{u_2({respect_to})\\cdot \ln(u_1({respect_to}))}}')]
        differentiated, differentiated_steps = \
            Pow(Const('e'), Multiply(self.right, Log(Const('e'), self.left))).differentiate(respect_to)
        for item in differentiated_steps:
            steps.append(item)
        return differentiated, steps

    def simplify(self, expand: bool) -> Expr:
        if isinstance(self.right, Const):
            if self.right.name == 1:
                return self.left.simplify(expand)
            if self.right.name == 0:
                return Const(1)
        if isinstance(self.left, Const):
            if self.left.name == 1:
                return Const(1)
            if self.left.name == 0:
                return Const(0)

        if expand:
            # Binomial expansion
            if isinstance(self.right, Const) and isinstance(self.right.name, int) and self.right.name > 1 and \
                    isinstance(self.left, Plus) and ((self.left.num_non_plus == 2 and self.right.name <= 100) or
                                                     (self.left.num_non_plus <= 20 and self.right.name == 2) or
                                                     (self.left.num_non_plus + self.right.name <= 10)):
                n = self.right.name
                x = self.left.left.simplify(expand)
                y = self.left.right.simplify(expand)
                tree = Pow(x, Const(n)).simplify(expand)
                for k in range(1, n + 1):
                    tree = Plus(tree, Multiply(
                        Multiply(Const(choose(n, k)), Pow(x, Const(n - k)).simplify(expand)).simplify(expand),
                        Pow(y, Const(k)).simplify(expand)).simplify(expand)).simplify(expand)
                return tree

        if isinstance(self.left, Const) and isinstance(self.left.name, int) and \
                isinstance(self.right, Const) and isinstance(self.right.name, int):
            if self.right.name >= 0:
                return Const(self.left.name ** self.right.name)
            else:
                return Pow(Const(self.left.name ** (-self.right.name)), Const(-1))

        if isinstance(self.left, Multiply):
            right_simplified = self.right.simplify(expand)
            return Multiply(Pow(self.left.left.simplify(expand), right_simplified).simplify(expand),
                            Pow(self.left.right.simplify(expand), right_simplified).simplify(expand)).simplify(expand)

        if isinstance(self.left, Pow):
            return Pow(self.left.left.simplify(expand),
                       Multiply(self.left.right.simplify(expand), self.right.simplify(expand)).simplify(
                           expand)).simplify(expand)

        # a ^ loga(something)
        if isinstance(self.right, Log) and str(self.left) == str(self.right.base):
            return self.right.arg.simplify(expand)

        if isinstance(self.right, Multiply):
            log_arg, new_exponent = remove_log(self.left, self.right)
            if log_arg:
                return Pow(log_arg.simplify(expand), new_exponent.simplify(expand)).simplify(expand)

        # a ^ (b + c) = a^b * a^c (where b + c can't be simplified)
        if isinstance(self.right, Plus):
            base_simplified = self.left.simplify(expand)
            exponent_simplified = self.right.simplify(expand)
            if str(exponent_simplified) == str(self.right):
                return Multiply(Pow(base_simplified, self.right.left).simplify(expand),
                                Pow(base_simplified, self.right.right).simplify(expand)).simplify(expand)
            return Pow(base_simplified, exponent_simplified)

        return Pow(self.left.simplify(expand), self.right.simplify(expand))

    def rearrange(self) -> Expr:
        return Pow(self.left.rearrange(), self.right.rearrange())

    def trig_simplify(self) -> Expr:
        if isinstance(self.left, Trig) and self.left.name in {'sin', 'cos', 'tan', 'csc', 'sec', 'cot'}:
            negative, abs_of_exponent = is_minus(self.right)
            if negative:
                if self.left.name == 'sin':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('csc', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('csc', self.left.arg.trig_simplify()), abs_of_exponent)
                elif self.left.name == 'cos':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('sec', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('sec', self.left.arg.trig_simplify()), abs_of_exponent)
                elif self.left.name == 'tan':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('cot', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('cot', self.left.arg.trig_simplify()), abs_of_exponent)
                elif self.left.name == 'csc':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('sin', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('sin', self.left.arg.trig_simplify()), abs_of_exponent)
                elif self.left.name == 'sec':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('cos', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('cos', self.left.arg.trig_simplify()), abs_of_exponent)
                elif self.left.name == 'cot':
                    if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                        return Trig('tan', self.left.arg.trig_simplify())
                    else:
                        return Pow(Trig('tan', self.left.arg.trig_simplify()), abs_of_exponent)

        return Pow(self.left.trig_simplify(), self.right.trig_simplify())

    def fractionify(self) -> Expr:
        negative, abs_of_exponent = is_minus(self.right)
        if negative:
            if isinstance(abs_of_exponent, Const) and abs_of_exponent.name == 1:
                return Multiply(Const(1), Pow(self.left, Const(-1)))
            return Multiply(Const(1), Pow(Pow(self.left, abs_of_exponent), Const(-1)))
        return Pow(self.left.fractionify(), self.right.fractionify())


def choose(n, k):
    """Calculates n choose k. Used for calculating binomial coefficients.
    Credits: user448810 and Beginner on https://stackoverflow.com/questions/15301885/best-way-of-calculating-n-choose-k
    """
    if k == 0:
        return 1
    return (n * choose(n - 1, k - 1)) // k


def remove_log(base: Expr, expr: Multiply) -> tuple:
    """If there is log_base(arg) in expr, replace it with Const(1).
    Returns a tuple in the form (argument_of_log, new_expr), where new_expr is the mutated expr object.
    """
    if isinstance(expr.left, Log) and str(expr.left.base) == str(base):
        return (expr.left.arg, expr.right)
    if isinstance(expr.right, Log) and str(expr.right.base) == str(base):
        return (expr.right.arg, expr.left)
    if isinstance(expr.right, Multiply):
        right_result = remove_log(base, expr.right)
        if right_result[0]:
            return (right_result[0], Multiply(expr.left, right_result[1]))
    if isinstance(expr.left, Multiply):
        left_result = remove_log(base, expr.left)
        if left_result[0]:
            return (left_result[0], Multiply(left_result[1], expr.right))
    return (None, None)


class Var(Num):
    """Represents a single variable.

    Instance Attributes:
        - name: the name of the variable
    """
    name: str

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if respect_to != 'c':
            constant_var = 'c'
        else:
            constant_var = 'a'
        if respect_to == self.name:
            return Const(1), [(Const(1), 'Differentiating the variable of differentiation gives 1: ',
                              f'{respect_to}\'=1')]
        else:
            return Const(0), [(Const(0), 'The derivative of a constant is zero: ', f'\\displaystyle {constant_var}\'=0')]


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
        return self.name + ' ( ' + str(self.arg) + ') '

    def get_latex(self) -> str:
        return '\\' + self.name + ' \\left( ' + self.arg.get_latex() + '\\right) '

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if self.name == 'sin':
            steps = [(Multiply(Trig('cos', self.arg), Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\sin(u({respect_to}))\\right]\'=\\cos(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Trig('cos', self.arg), item[0]), item[1], item[2]))
            return Multiply(Trig('cos', self.arg), arg_differentiated), steps
        if self.name == 'cos':
            steps = [(Multiply(Multiply(Const(-1), Trig('sin', self.arg)), Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\cos(u({respect_to}))\\right]\'=-\\sin(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Multiply(Const(-1), Trig('sin', self.arg)), item[0]), item[1], item[2]))
            return Multiply(Multiply(Const(-1), Trig('sin', self.arg)), arg_differentiated), steps
        if self.name == 'tan':
            steps = [(Multiply(Pow(Trig('cos', self.arg), Const(-2)), Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\tan(u({respect_to}))\\right]\'=\\sec^2(u({respect_to}))\\cdot u\'({respect_to})=\\cos^{{-2}}(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Pow(Trig('cos', self.arg), Const(-2)), item[0]), item[1], item[2]))
            return Multiply(Pow(Trig('cos', self.arg), Const(-2)), arg_differentiated), steps
            # return Multiply(Pow(Trig('sec', self.arg), Const(2)),
            #                 self.arg.differentiate(respect_to)
            #                 )
        if self.name == 'sec':
            steps = [(Multiply(Multiply(Trig('sin', self.arg), Pow(Trig('cos', self.arg), Const(-2))),
                              Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\sec(u({respect_to}))\\right]\'=\\sec(u({respect_to}))\\cdot\\tan(u({respect_to}))\\cdot u\'({respect_to})=\\sin(u({respect_to}))\\cdot\\cos^{{-2}}(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Multiply(Trig('sin', self.arg), Pow(Trig('cos', self.arg), Const(-2))),
                                      item[0]), item[1], item[2]))
            return Multiply(Multiply(Trig('sin', self.arg), Pow(Trig('cos', self.arg), Const(-2))),
                            arg_differentiated), steps
            # return Multiply(Trig('sec', self.arg),
            #                 Multiply(Trig('tan', self.arg),
            #                          self.arg.differentiate(respect_to)
            #                          )
            #                 )
        if self.name == 'csc':
            steps = [(Multiply(Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))), Trig('cos', self.arg)),
                         Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                 f'\\displaystyle \\left[\\csc(u({respect_to}))\\right]\'=-\\csc(u({respect_to}))\\cdot\\cot(u({respect_to}))\\cdot u\'({respect_to})=-\\sin^{{-2}}(u({respect_to}))\\cdot\\cos(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))),
                                               Trig('cos', self.arg)), item[0]), item[1], item[2]))
            return Multiply(Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))), Trig('cos', self.arg)),
                            arg_differentiated), steps
            # return Multiply(Const(-1),
            #                 Multiply(Trig('csc', Var('x')),
            #                          Multiply(Trig('cot', Var('x')),
            #                                   self.arg.differentiate(respect_to)
            #                                   )
            #                          )
            #                 )
        if self.name == 'cot':
            steps = [(Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))),
                              Diff(self.arg, respect_to)), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                 f'\\displaystyle \\left[\\cot(u({respect_to}))\\right]\'=-\\csc^{{2}}(u({respect_to}))\\cdot u\'({respect_to})=-\\sin^{{-2}}(u({respect_to}))\\cdot u\'({respect_to})')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))),
                                      item[0]), item[1], item[2]))
            return Multiply(Multiply(Const(-1), Pow(Trig('sin', self.arg), Const(-2))),
                            arg_differentiated), steps
            # return Multiply(Const(-1),
            #                 Multiply(Pow(Trig('csc', self.arg), Const(2)),
            #                          self.arg.differentiate(respect_to)
            #                          )
            #                 )

        if self.name == 'arcsin':  #todo did up to here steps
            steps = [(Multiply(Diff(self.arg, respect_to),
                              Pow(Plus(Const(1),
                                       Multiply(Const(-1),
                                                Pow(self.arg,
                                                    Const(2)))), Multiply(Const(-1), Pow(Const(2), Const(-1))))),
                      'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\arcsin(u({respect_to}))\\right]\'=\\frac{{u\'({respect_to})}}{{\\sqrt{{1-u^2({respect_to})}}}}=u\'(x)\\cdot (1-u^2({respect_to}))^{{\\frac{{-1}}{{2}}}}')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(item[0],
                                      Pow(Plus(Const(1),
                                               Multiply(Const(-1),
                                                        Pow(self.arg,
                                                            Const(2)))),
                                          Multiply(Const(-1), Pow(Const(2), Const(-1))))), item[1], item[2]))
            return Multiply(arg_differentiated,
                            Pow(Plus(Const(1),
                                     Multiply(Const(-1),
                                              Pow(self.arg,
                                                  Const(2)))), Multiply(Const(-1), Pow(Const(2), Const(-1))))), steps
        if self.name == 'arccos':
            steps = [(Multiply(Const(-1), Diff(Trig('arcsin', self.arg), respect_to)), 'Use the following identity: ',
                      f'\\displaystyle \\left[\\arccos(u({respect_to}))\\right]\'=-\\left[\\arcsin(u({respect_to}))\\right]\'')]
            differentiated, differentiated_steps = Trig('arcsin', self.arg).differentiate(respect_to)
            for item in differentiated_steps:
                steps.append((Multiply(Const(-1), item[0]), item[1], item[2]))
            return Multiply(Const(-1), differentiated), steps
        if self.name == 'arctan':
            steps = [(Multiply(Diff(self.arg, respect_to),
                              Pow(Plus(Pow(self.arg, Const(2)), Const(1)), Const(-1))), 'Apply the following trigonometric differentiation rule and the chain rule: ',
                      f'\\displaystyle \\left[\\arctan(u({respect_to}))\\right]\'=\\frac{{u\'({respect_to})}}{{u^2({respect_to})+1}}=u\'({respect_to})\\cdot (u^2({respect_to})+1)^{{-1}}')]
            arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
            for item in arg_steps:
                steps.append((Multiply(item[0],
                                      Pow(Plus(Pow(self.arg, Const(2)), Const(1)), Const(-1))), item[1], item[2]))
            return Multiply(arg_differentiated,
                            Pow(Plus(Pow(self.arg, Const(2)), Const(1)), Const(-1))), steps

    def simplify(self, expand: bool) -> Expr:
        if self.name == 'tan':
            return Multiply(Trig('sin', self.arg.simplify(expand)),
                            Pow(Trig('cos', self.arg.simplify(expand)), Const(-1)))
        if self.name == 'sec':
            return Multiply(Const(1), Pow(Trig('cos', self.arg.simplify(expand)), Const(-1)))
        if self.name == 'csc':
            return Multiply(Const(1), Pow(Trig('sin', self.arg.simplify(expand)), Const(-1)))
        if self.name == 'cot':
            return Multiply(Const(1), Pow(Trig('tan', self.arg.simplify(expand)), Const(-1)))
        return Trig(self.name, self.arg.simplify(expand))

    def trig_simplify(self) -> Expr:
        return Trig(self.name, self.arg.trig_simplify())

    def fractionify(self) -> Expr:
        return Trig(self.name, self.arg.fractionify())


class Log(Func):
    """Represents a logarithmic function.

    Instance Attributes:
        - name: 'log'
        - base: the base of the logarithm
        - arg: the argument of the logarithm

    Representation Invariants:
        - isinstance(self.base, Num)
    """
    name = 'log'
    base: Expr
    arg: Expr

    def __init__(self, base: Expr, arg: Expr) -> None:
        try:
            if isinstance(arg, Const) and (arg.name == 0 or arg.name == 1):
                raise LogBaseError
            self.base = base
            super().__init__(arg)
        except LogBaseError as error:
            print(error.msg)

    def __str__(self) -> str:
        if isinstance(self.base, Const) and self.base.name == 'e':
            return 'ln ( ' + str(self.arg) + ') '
        else:
            return 'log' + str(self.base) + '( ' + str(self.arg) + ') '

    def get_latex(self) -> str:
        if isinstance(self.base, Const) and self.base.name == 'e':
            return '\\ln \\left( ' + self.arg.get_latex() + '\\right) '
        else:
            return '\\log_{' + self.base.get_latex() + '} \\left( ' + self.arg.get_latex() + '\\right) '

    def differentiate(self, respect_to: str) -> tuple[Expr, list]:
        if respect_to != 'c':
            constant_var = 'c'
        else:
            constant_var = 'a'

        if isinstance(self.base, Const):
            if not isinstance(self.arg, Const):
                if self.base.name == 'e':
                    steps = [(Multiply(Diff(self.arg, respect_to), Pow(self.arg, Const(-1))), 'Apply the following logarithm differentiation rule: ',
                              f'\\left[\\ln(u({respect_to}))\\right]\'=\\displaystyle \\frac{{u\'({respect_to})}}{{u({respect_to})}}=u\'({respect_to})\\cdot (u({respect_to}))^{{-1}}')]
                    arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
                    for item in arg_steps:
                        steps.append((Multiply(item[0], Pow(self.arg, Const(-1))), item[1], item[2]))
                    return Multiply(arg_differentiated, Pow(self.arg, Const(-1))), steps
                else:
                    steps = [(Multiply(Diff(self.arg, respect_to),
                                      Pow(Multiply(self.arg, Log(Const('e'), self.base)), Const(-1))), 'Apply the following logarithm differentiation rule: ',
                              f'\\displaystyle \\left[\\log_{{{constant_var}}}(u({respect_to}))\\right]\'= \\frac{{u\'({respect_to})}}{{\\ln({constant_var})\\cdot u({respect_to})}}=u\'({respect_to})\\cdot (\\ln({constant_var})\\cdot u({respect_to}))^{{-1}}')]
                    arg_differentiated, arg_steps = self.arg.differentiate(respect_to)
                    for item in arg_steps:
                        steps.append((Multiply(item[0],
                                              Pow(Multiply(self.arg, Log(Const('e'), self.base)), Const(-1))), item[1], item[2]))
                    return Multiply(arg_differentiated,
                                    Pow(Multiply(self.arg, Log(Const('e'), self.base)), Const(-1))), steps
            else:
                # Then it is a constant!
                return Const(0), [(Const(0), 'The derivative of a constant is zero: ', f'\\displaystyle {constant_var}\'=0')]
        steps = [(Diff(Multiply(Log(Const('e'), self.arg), Pow(Log(Const('e'), self.base), Const(-1))), respect_to), 'Use the following identity: ',
                  f'\\displaystyle\\log_{{u_1({respect_to})}}(u_2({respect_to}))=\\frac{{\\ln({{u_2({respect_to})}})}}{{\\ln(u_1({respect_to}))}}=\\ln({{u_2({respect_to})}})\\cdot (\\ln(u_1({respect_to})))^{{-1}}')]
        differentiated, differentiated_steps = \
            Multiply(Log(Const('e'), self.arg), Pow(Log(Const('e'), self.base), Const(-1))).differentiate(respect_to)
        for item in differentiated_steps:
            steps.append(item)
        return differentiated, steps

    def simplify(self, expand: bool) -> Expr:
        if str(self.arg) == str(self.base):
            return Const(1)

        if isinstance(self.arg, Const) and self.arg.name == 1:
            return Const(0)

        base_simplified = self.base.simplify(expand)
        arg_simplified = self.arg.simplify(expand)

        # logb(m * n) = logb(m) + logb(n)
        if isinstance(self.arg, Multiply):
            if str(arg_simplified) == str(self.arg):
                return Plus(Log(base_simplified, self.arg.left.simplify(expand)).simplify(expand),
                            Log(base_simplified, self.arg.right.simplify(expand)).simplify(expand)).simplify(expand)

        # logb(m ^ n) = n * logb(m)
        if isinstance(self.arg, Pow):
            if str(arg_simplified) == str(self.arg):
                return Multiply(self.arg.right.simplify(expand),
                                Log(base_simplified, self.arg.left.simplify(expand)).simplify(expand)).simplify(expand)

        if isinstance(base_simplified, Const):
            return Log(base_simplified, arg_simplified)
        else:
            # return ln(arg) / ln(base)
            return Multiply(Log(Const('e'), arg_simplified).simplify(expand),
                            Pow(Log(Const('e'), base_simplified).simplify(expand), Const(-1)).simplify(
                                expand)).simplify(expand)

    def trig_simplify(self) -> Expr:
        return Log(self.base.trig_simplify(), self.arg.trig_simplify())

    def fractionify(self) -> Expr:
        return Log(self.base.fractionify(), self.arg.fractionify())


def process_to_list(obj: Expr) -> list[tuple[str, int | float | str]]:
    """For processing 'Non-digit' Expr objects. Outputs a list, with each element being a tuple in the form
    of (base, exponent)

    Example: a * b ^ 2 * c ^ 3 is processed to [('a', 1), ('b', 2), ('c', 3)]

    Preconditions:
        - obj is a valid 'Non-digit' object
    """
    if isinstance(obj, Const) and isinstance(obj.name, str):  # 13
        return [(obj.name, 1)]
    if isinstance(obj, Multiply):  # 15
        return process_to_list(obj.left) + process_to_list(obj.right)
    if isinstance(obj, Pow) and isinstance(obj.left, Const) and isinstance(obj.right, Const) and \
            isinstance(obj.left.name, str):  # 16, 17
        return [(obj.left.name, obj.right.name)]
    return []


def get_arrangement_type(expr: Expr) -> tuple:  # TODO: TEST
    """Returns a tuple in the form of:
    (type, base, exponent, coefficient, function_name, function_argument)
    """
    if isinstance(expr, Var):
        return ('Power', expr, Const(1), Const(1), None, None)  # 4
    if isinstance(expr, Func):
        return ('Function', expr, Const(1), Const(1), expr.name, expr.arg)  # 10
    if isinstance(expr, Const) and isinstance(expr.name, str):
        return ('Non-digit', expr, Const(1), Const(1), None, None)  # 13
    if isinstance(expr, Const) and (isinstance(expr.name, int) or isinstance(expr.name, float)):
        return ('Digit', expr, Const(1), Const(1), None, None)  # 18
    if isinstance(expr, Multiply):
        if isinstance(expr.left, Const) and isinstance(expr.left.name, int) and \
                isinstance(expr.right, Pow) and isinstance(expr.right.left, Const) and \
                isinstance(expr.right.left.name, int) and \
                isinstance(expr.right.right, Const) and expr.right.right.name == -1:
            return ('Digit', expr, Const(1), Const(1), None, None)  # 20
        expr_left_type = get_arrangement_type(expr.left)[0]
        if expr_left_type == 'Non-digit':
            if get_arrangement_type(expr.right)[0] == 'Non-digit':
                return ('Non-digit', expr, Const(1), Const(1), None, None)  # 15
        if expr_left_type == 'Digit':
            if get_arrangement_type(expr.right)[0] == 'Non-digit':
                return ('Non-digit', expr.right, Const(1), expr.left, None, None)  # 14
        if expr_left_type in {'Non-digit', 'Digit'}:
            if isinstance(expr.right, Pow) and isinstance(expr.right.left, Var) \
                    and get_arrangement_type(expr.right.right)[0] in {'Non-digit', 'Digit'}:
                return ('Power', expr.right.left, expr.right.right, expr.left, None, None)  # 1
            if isinstance(expr.right, Var):
                return ('Power', expr.right, Const(1), expr.left, None, None)  # 3
            if isinstance(expr.right, Pow) and get_arrangement_type(expr.right.left)[0] in {'Non-digit', 'Digit'} \
                    and get_arrangement_type(expr.right.right)[0] == 'Power':
                return ('Exponential', expr.right.left, expr.right.right, expr.left, None, None)  # 5, 8
            if isinstance(expr.right, Func):
                return ('Function', expr, Const(1), expr.left, expr.right.name, expr.right.arg)  # 9
            if isinstance(expr.right, Pow) and isinstance(expr.right.left, Func) \
                    and get_arrangement_type(expr.right.right)[0] in {'Non-digit', 'Digit'}:
                return ('Function', expr.right.left, expr.right.right, expr.left, expr.right.left.name,
                        expr.right.left.arg)  # 11
    if isinstance(expr, Pow):
        if isinstance(expr.left, Const):
            if get_arrangement_type(expr.right)[0] in {'Non-digit', 'Digit'}:
                if isinstance(expr.left.name, str):
                    # Note: We consider the entirety of expr to be the base here; expr.left is NOT the base
                    return ('Non-digit', expr, Const(1), Const(1), None, None)  # 16, 17
                if isinstance(expr.left.name, int) or isinstance(expr.left.name, float):
                    return ('Digit', expr.left, expr.right, Const(1), None, None)  # 19

        expr_left_type = get_arrangement_type(expr.left)[0]
        if expr_left_type in {'Non-digit', 'Digit'}:
            if get_arrangement_type(expr.right)[0] == 'Power':
                return ('Exponential', expr.left, expr.right, Const(1), None, None)  # 6, 7
        if get_arrangement_type(expr.right)[0] in {'Non-digit', 'Digit'}:
            if isinstance(expr.left, Var):
                return ('Power', expr.left, expr.right, Const(1), None, None)  # 2
            if isinstance(expr.left, Func):
                return ('Function', expr.left, expr.right, Const(1), expr.left.name, expr.left.arg)  # 12

    return ('Other', expr, Const(1), Const(1), None, None)


class LogBaseError(Exception):
    """Raised when the user attempts to define log(0).

    Instance Attributes:
        - msg: the error message
    """
    msg: str

    def __init__(self) -> None:
        self.msg = 'Logarithm base is invalid!'


class TrigError(Exception):
    """Raised when the user tries to define an undefined trigonometric function.

    Instance Attributes:
        - msg: the error message
    """
    msg: str

    def __init__(self) -> None:
        self.msg = 'The entered trigonometric function does not exist. Please try again!'
