"""The runner file"""

from classes import *


def string_to_expr(input: str, variables: set[str]) -> Expr:
    """Converts a string math input to an Expr binary tree.

    Involves the Shunting yard algorithm (https://en.wikipedia.org/wiki/Shunting_yard_algorithm).
    """
    input_array = input.split('')
    # Note that output_stack only contains Expr objects
    output_stack = []
    operator_stack = []
    for token in input_array:
        typ = token_type(token)
        if typ == 'Num':
            output_stack.append(str_to_Num(token, variables))
        elif typ == 'Func':
            operator_stack.append(token)
        elif typ == 'BinOp':
            while len(operator_stack) > 0 and operator_stack[-1] != '(' \
                    and (precedence(operator_stack[-1]) > precedence(token)
                         or (precedence(operator_stack[-1]) == precedence(token)
                             and is_left_associative(token))):
                tree = str_to_BinOp(token)

                subtree1 = output_stack.pop()
                subtree2 = output_stack.pop()

                tree.left = subtree2
                tree.right = subtree1

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
                        tree = str_to_Func(operator)

                        subtree = output_stack.pop()

                        tree.arg = subtree

                        output_stack.append(tree)
                    elif operator_type == 'BinOp':
                        tree = str_to_BinOp(operator)

                        subtree1 = output_stack.pop()
                        subtree2 = output_stack.pop()

                        tree.left = subtree2
                        tree.right = subtree1

                        output_stack.append(tree)
                # top of op stack is now '('
                operator_stack.pop() # Discarding the '('
                if token_type(operator_stack[-1]) == 'Func':
                    tree = str_to_Func(operator_stack[-1])

                    subtree = output_stack.pop()

                    tree.arg = subtree

                    output_stack.append(tree)
            except IndexError:
                print(ParenthesesError.msg)
    while len(operator_stack) > 0:
        if operator_stack[-1] == '(':
            raise ParenthesesError
        operator = operator_stack.pop()
        operator_type = token_type(operator)
        if operator_type == 'Func':
            tree = str_to_Func(operator)

            subtree = output_stack.pop()

            tree.arg = subtree

            output_stack.append(tree)
        elif operator_type == 'BinOp':
            tree = str_to_BinOp(operator)

            subtree1 = output_stack.pop()
            subtree2 = output_stack.pop()

            tree.left = subtree2
            tree.right = subtree1

            output_stack.append(tree)

    # Outside the for loop
    return output_stack.pop()


def token_type(token: str) -> str:
    """Outputs 'Num', 'BinOp', 'Func', '(', or ')'.
    """
    if token == '(' or token == ')':
        return token
    ...  # TODO: IMPLEMENT


def precedence(token: str) -> int:
    ...  # TODO: IMPLEMENT


def is_left_associative(token: str) -> int:
    ...  # TODO: IMPLEMENT

def str_to_Num(token: str, variables: set[str]) -> Num:
    ...  # TODO: IMPLEMENT

def str_to_BinOp(token: str) -> BinOp:
    ...  # TODO: IMPLEMENT

def str_to_Func(token: str) -> Func:
    ...  # TODO: IMPLEMENT


class ParenthesesError(Exception):
    """Raised when there is an invalid input of parentheses.

    Instance Attributes:
        - msg: the error message
    """
    msg: str

    def __init__(self) -> None:
        self.msg = 'The parentheses are mismatched. Please check your input and try again!'
