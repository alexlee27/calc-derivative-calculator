"""The runner file"""

from classes import *

# todo: github testing; remove this comment later
class ParenthesesError(Exception):
    """Raised when there is an invalid input of parentheses.

    Instance Attributes:
        - msg: the error message
    """
    msg = 'The parentheses are mismatched. Please check your input and try again!'


class LogBaseVarError(Exception):
    """Raised when the user attempts to put a variable in the base of a logarithm

    Instance Attributes:
        - msg: the error message
    """
    msg = 'Variables in the bases of logarithms are not supported. Please try again!'


def string_to_expr(text: str, variables: set[str]) -> Expr:
    """Converts a string math input to an Expr binary tree.

    Involves the Shunting yard algorithm (https://en.wikipedia.org/wiki/Shunting_yard_algorithm).
    """
    input_array = text.split(' ')
    # Note that output_stack only contains Expr objects
    output_stack = []
    operator_stack = []

    for token in input_array:
        typ = token_type(token)
        if typ == 'Num':
            output_stack.append(str_to_num(token, variables))

        elif typ == 'Func':
            operator_stack.append(token)

        elif typ == 'BinOp':
            while len(operator_stack) > 0 and operator_stack[-1] != '(' \
                    and (precedence(operator_stack[-1]) > precedence(token)
                         or (precedence(operator_stack[-1]) == precedence(token)
                             and is_left_associative(token))):
                subtree1 = output_stack.pop()
                subtree2 = output_stack.pop()

                tree = str_to_bin_op(operator_stack.pop(), subtree2, subtree1)

                output_stack.append(tree)

            operator_stack.append(token)
        elif typ == '(':
            operator_stack.append(token)

        else:  # typ == ')'
            try:
                while operator_stack[-1] != '(':
                    operator = operator_stack.pop()
                    operator_type = token_type(operator)

                    if operator_type == 'Func':
                        subtree = output_stack.pop()
                        tree = str_to_func(operator, subtree, variables)
                        output_stack.append(tree)

                    elif operator_type == 'BinOp':
                        subtree1 = output_stack.pop()
                        subtree2 = output_stack.pop()
                        tree = str_to_bin_op(operator, subtree2, subtree1)
                        output_stack.append(tree)
                # top of operator_stack is now '('
                operator_stack.pop()  # discarding the '('

                if len(operator_stack) > 0 and token_type(operator_stack[-1]) == 'Func':
                    subtree = output_stack.pop()
                    tree = str_to_func(operator_stack.pop(), subtree, variables)
                    output_stack.append(tree)
            except IndexError:
                print(ParenthesesError.msg)
    while len(operator_stack) > 0:
        if operator_stack[-1] == '(':
            raise ParenthesesError

        operator = operator_stack.pop()
        operator_type = token_type(operator)

        if operator_type == 'Func':
            subtree = output_stack.pop()
            tree = str_to_func(operator, subtree, variables)
            output_stack.append(tree)

        elif operator_type == 'BinOp':
            subtree1 = output_stack.pop()
            subtree2 = output_stack.pop()
            tree = str_to_bin_op(operator, subtree2, subtree1)
            output_stack.append(tree)

    # Outside the for loop
    return output_stack.pop()


def token_type(token: str) -> str:
    """Outputs 'Num', 'BinOp', 'Func', '(', or ')'.

    Preconditions:
        - token is a valid mathematical input
    """
    if token == '(' or token == ')':
        return token
    if token in {'^', '*', '/', '+', '-'}:
        return 'BinOp'
    if 'log' in token or 'ln' in token or token in Trig.VALID_NAMES:
        return 'Func'
    else:
        return 'Num'


def precedence(operator: str) -> int:
    """Returns the mathematical precedence of the operator

    Preconditions:
        - operator in {'^', '*', '/', '+', '-'}
    """
    operator_to_precedence = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    return operator_to_precedence[operator]


def is_left_associative(operator: str) -> bool:
    """Returns whether operator is left associative or not.

    Preconditions:
        - operator in {'^', '*', '/', '+', '-'}
    """
    return operator != '^'


def str_to_num(token: str, variables: set[str]) -> Num:
    """Converts a string token into a Num object.

    Preconditions:
        - token is a valid Num input
    """
    if token in variables:
        return Var(token)
    else:
        try:
            return Const(int(token))
        except ValueError:
            pass
        try:
            return Const(float(token))
        except ValueError:
            return Const(token)


def str_to_bin_op(token: str, left: Expr, right: Expr) -> BinOp:
    """Converts a string token into a Num object.

    Preconditions:
        - token in {'^', '*', '/', '+', '-'}
    """
    if token == '^':
        return Power(left, right)
    if token == '*':
        return Multiply(left, right)
    if token == '/':
        return Multiply(left, Power(right, Const(-1)))
    if token == '+':
        return Plus(left, right)
    if token == '-':
        return Plus(left, Multiply(Const(-1), right))


def str_to_func(token: str, arg: Expr, variables: set[str]) -> Func:
    """Converts a string token into a Num object.

    Preconditions:
        - 'log' in token or 'ln' in token or token in Trig.VALID_NAMES
    """
    if 'ln' in token:
        return Log(Const('e'), arg)
    if 'log' in token:
        num_object = str_to_num(token[3:], variables)
        try:
            if isinstance(num_object, Const):
                return Log(num_object, arg)
            raise LogBaseVarError
        except LogBaseVarError as error:
            print(error.msg)
    if token in Trig.VALID_NAMES:
        return Trig(token, arg)
