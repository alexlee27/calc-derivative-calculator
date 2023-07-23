"""The runner file"""

from classes import *
from tree_visualization import *


class CustomError(Exception):
    """A class for custom errors.

    Instance Attributes:
        - msg: the error message
    """
    msg = ''


class ParenthesesError(CustomError):
    """Raised when there is an invalid input of parentheses.

    Instance Attributes:
        - msg: the error message
    """
    msg = 'The parentheses are mismatched. Please check your input and try again!'


class LogNoBaseError(CustomError):
    """Raised when the user does not define the base of a logarithm that is not the natural logarithm (ln).

    Instance Attributes:
        - msg: the error message
    """
    msg = 'Please define the base of the logarithm! Type the input in the form log_(base)(argument).'


class InvalidInputError(CustomError):
    """Raised when the user enters invalid math input.

    Instance Attributes:
        - msg: the error message
    """
    msg = 'Please check your input.'


def tokenizer(text: str) -> list[str]:
    """Converts a string math input into a list of tokens that can be processed by the parser function."""
    names_2_char = {'ln', 'pi'}
    names_3_char = {'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'log'}
    names_6_char = {'arcsin', 'arccos', 'arctan'}

    bin_operators = {'+', '*', '/', '^'}
    result = []
    i = 0
    prev_type = None
    logs_and_open_paren = []
    while i < len(text):
        if text[i] == ' ':
            pass
        elif i + 2 <= len(text) and text[i:i+2] in names_2_char:
            if prev_type in {')', 'digit', 'letter'}:
                result.append('*')
            result.append(text[i:i+2])
            if result[-1] == 'ln':
                prev_type = 'function'
            else:  # pi
                prev_type = 'letter'
            i += 1
        elif i + 3 <= len(text) and text[i:i+3] in names_3_char:
            if prev_type in {')', 'digit', 'letter'}:
                result.append('*')
            result.append(text[i:i+3])
            prev_type = 'function'
            if result[-1] == 'log':
                if text[i + 3] == '_':
                    i += 3
                    logs_and_open_paren.append('log')
                else:
                    raise LogNoBaseError
            else:
                i += 2
        elif i + 6 <= len(text) and text[i:i+6] in names_6_char:
            if prev_type in {')', 'digit', 'letter'}:
                result.append('*')
            result.append(text[i:i + 6])
            prev_type = 'function'
            i += 5
        else:
            if text[i] in bin_operators:
                result.append(text[i])
                prev_type = 'operator'
            elif text[i] == '-':
                if not (i + 1 < len(text) and ord('0') <= ord(text[i + 1]) <= ord('9')):
                    if prev_type in {None, '('}:
                        result.append('-1')
                        result.append('*')
                    else:
                        result.append(text[i])
                elif i + 1 < len(text) and ord('0') <= ord(text[i + 1]) <= ord('9'):
                    if prev_type not in {None, '('}:
                        result.append('+')
                else:
                    raise InvalidInputError
                prev_type = '-'
            elif text[i] == '(':
                if prev_type in {')', 'digit', 'letter'}:
                    if len(logs_and_open_paren) > 0 and logs_and_open_paren[-1] == 'log':
                        logs_and_open_paren.pop()
                    else:
                        result.append('*')
                # elif prev_type == '-':
                #     result.append('-1')
                #     result.append('*')
                result.append(text[i])
                prev_type = '('
                logs_and_open_paren.append('(')
            elif text[i] == ')':
                result.append(text[i])
                prev_type = ')'
                assert logs_and_open_paren[-1] == '('
                logs_and_open_paren.pop()
            elif (ord('A') <= ord(text[i]) <= ord('Z')) or (ord('a') <= ord(text[i]) <= ord('z')):
                if prev_type in {')', 'digit', 'letter'}:
                    result.append('*')
                # elif prev_type == '-':
                #     result.append('-1')
                #     result.append('*')
                result.append(text[i])
                prev_type = 'letter'
            elif ord('0') <= ord(text[i]) <= ord('9'):
                token_accumlator = ''
                if prev_type in {')', 'letter'}:
                    result.append('*')
                elif prev_type == '-':
                    token_accumlator = '-'
                token_accumlator += text[i]
                while i + 1 < len(text) and ord('0') <= ord(text[i + 1]) <= ord('9'):
                    token_accumlator += text[i + 1]
                    i += 1
                result.append(token_accumlator)
                prev_type = 'digit'
            else:
                raise InvalidInputError
        i += 1

    return result


def string_to_expr(text: str, variables: set[str]) -> Expr | CustomError:
    """A parser function that converts a string math input to an Expr binary tree.
    Returns the Exception object if there is an error.

    Involves using the Shunting yard algorithm (https://en.wikipedia.org/wiki/Shunting_yard_algorithm).
    """
    try:
        input_array = tokenizer(text)
        # Note that output_stack only contains Expr objects
        output_stack = []
        operator_stack = []

        for token in input_array:
            typ = token_type(token)
            if typ == 'Num':
                output_stack.append(str_to_num(token, variables))

            elif typ == 'Func':
                operator_stack.append(token)

            elif typ == 'LogNoBase':
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
                while operator_stack[-1] != '(':
                    operator = operator_stack.pop()
                    operator_type = token_type(operator)

                    if operator_type == 'Func':
                        subtree = output_stack.pop()
                        tree = str_to_func(operator, subtree, variables)
                        output_stack.append(tree)

                    elif operator_type == 'LogNoBase':
                        # Keep the logarithm in the operator stack, but with the base augmented.
                        subtree = output_stack.pop()
                        new_operator = (operator_stack.pop(), subtree)
                        operator_stack.append(new_operator)

                    elif operator_type == 'LogWithBase':
                        base = operator[1]
                        exponent = output_stack.pop()
                        tree = get_log_custom_base(base, exponent)
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
                elif len(operator_stack) > 0 and token_type(operator_stack[-1]) == 'LogNoBase':
                    # Keep the logarithm in the operator stack, but with the base augmented.
                    subtree = output_stack.pop()
                    new_operator = (operator_stack.pop(), subtree)
                    operator_stack.append(new_operator)
                elif len(operator_stack) > 0 and token_type(operator_stack[-1]) == 'LogWithBase':
                    base = operator_stack.pop()[1]
                    exponent = output_stack.pop()
                    tree = get_log_custom_base(base, exponent)
                    output_stack.append(tree)
        while len(operator_stack) > 0:
            if operator_stack[-1] == '(':
                raise ParenthesesError

            operator = operator_stack.pop()
            operator_type = token_type(operator)

            if operator_type == 'Func':
                subtree = output_stack.pop()
                tree = str_to_func(operator, subtree, variables)
                output_stack.append(tree)

            elif operator_type == 'LogNoBase':
                # Keep the logarithm in the operator stack, but with the base augmented.
                subtree = output_stack.pop()
                new_operator = (operator_stack.pop(), subtree)
                operator_stack.append(new_operator)

            elif operator_type == 'LogWithBase':
                base = operator[1]
                exponent = output_stack.pop()
                tree = get_log_custom_base(base, exponent)
                output_stack.append(tree)

            elif operator_type == 'BinOp':
                subtree1 = output_stack.pop()
                subtree2 = output_stack.pop()
                tree = str_to_bin_op(operator, subtree2, subtree1)
                output_stack.append(tree)

        # Outside the for loop
        return output_stack.pop()
    except CustomError as error:
        return error
    except Exception as error:
        error = InvalidInputError()
        return error


def token_type(token: Any) -> str:
    """Outputs 'Num', 'BinOp', 'Func', '(', or ')'.

    Preconditions:
        - token is a valid operator
    """
    if token == '(' or token == ')':
        return token
    if token in {'^', '*', '/', '+', '-'}:
        return 'BinOp'
    if token == 'ln' or token in Trig.VALID_NAMES:
        # originally 'ln' in token
        return 'Func'
    elif token == 'log':
        return 'LogNoBase'
    elif isinstance(token, tuple) and token[0] == 'log':
        return 'LogWithBase'
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
        return Pow(left, right)
    if token == '*':
        return Multiply(left, right)
    if token == '/':
        return Multiply(left, Pow(right, Const(-1)))
    if token == '+':
        return Plus(left, right)
    if token == '-':
        return Plus(left, Multiply(Const(-1), right))


def str_to_func(token: str, arg: Expr, variables: set[str]) -> Func:
    """Converts a string token into a Num object.

    Preconditions:
        - 'ln' in token or token in Trig.VALID_NAMES
    """
    if 'ln' in token:
        return Log(Const('e'), arg)
    if token in Trig.VALID_NAMES:
        return Trig(token, arg)


def get_log_custom_base(base: Expr, arg: Expr) -> Expr:
    """Return a Log object with the input base and argument.
    """
    return Log(base, arg)

def main() -> None:
    """The main function of this file.
    """
    while True:
        infix_expression = input('\nEnter a math expression to differentiate (type \'stop\' to stop): ')
        if len(infix_expression) == 4 and infix_expression.lower() == 'stop':
            break
        variable = input('Enter the name of the variable to differentiate with respect to: ')
        expr = string_to_expr(infix_expression, {variable})
        if expr is not None:
            differentiated = expr.differentiate(variable)
            prev = differentiated
            simplified = prev.simplify(expand=False)
            while str(simplified) != str(prev):
                print(prev)
                prev, simplified = simplified, simplified.simplify(expand=False)
            print(simplified)
            visualization_runner(simplified)
    print('Program is done')


def differentiate(input_text: str, expand: bool, variable: str = 'x') -> tuple[str, str, str, str, str]:
    """Differentiates the mathematical expression represented by input_text,
    returns a tuple in the form (input_simplfied_latex, differentiated_latex, input_simplified_string,
     differentiated_string, expand)
    """
    expr = string_to_expr(input_text, {variable})
    if isinstance(expr, Expr):
        prev1 = None
        curr = expr
        # Simplifying input first
        while str(curr) != str(prev1):
            prev1, curr = curr, curr.rearrange().fractionify()
            print('prev1: ' + str(prev1))
            print('curr : ' + str(curr))

            prev2 = None
            while str(curr) != str(prev2):
                # print(prev2)
                prev2, curr = curr, curr.simplify(expand=expand)
                print('prev2: ' + str(prev2))
                print('curr : ' + str(curr))
        simplified_input = curr.trig_simplify().fractionify()

        differentiated = simplified_input.differentiate(variable)
        print('differentiated')
        prev1 = None
        curr = differentiated
        while str(curr) != str(prev1):
            prev1, curr = curr, curr.rearrange().fractionify()
            print('prev1: ' + str(prev1))
            print('curr : ' + str(curr))

            prev2 = None
            while str(curr) != str(prev2):
                # print(prev2)
                prev2, curr = curr, curr.simplify(expand=expand)
                print('prev2: ' + str(prev2))
                print('curr : ' + str(curr))
            # print(simplified)
        # todo: toggle below for graph
        # visualization_runner(curr)
        differentiated = curr.trig_simplify().fractionify()
        return simplified_input.get_latex(), differentiated.get_latex(), str(simplified_input), str(differentiated),\
            str(expand).lower()
    elif isinstance(expr, CustomError):
        return '\\text{' + expr.msg + '}', '', '', '', ''


def input_preview(input_text: str, variable: str = 'x') -> str:
    """Returns the LaTeX code for input_text, provided it is valid.
    """
    expr = string_to_expr(input_text, {variable})
    if isinstance(expr, Expr):
        return expr.get_latex()
    elif isinstance(expr, CustomError):
        return '\\text{' + expr.msg + '}'


def simplify(input_text: str, expand: bool, variable: str = 'x') -> tuple[str, str]:
    """Simplifies the expression, returns its LaTeX code and its string form."""
    expr = string_to_expr(input_text, {variable})
    if isinstance(expr, Expr):
        prev1 = None
        curr = expr
        # Simplifying input first
        while str(curr) != str(prev1):
            prev1, curr = curr, curr.rearrange().fractionify()
            print('prev1: ' + str(prev1))
            print('curr : ' + str(curr))

            prev2 = None
            while str(curr) != str(prev2):
                # print(prev2)
                prev2, curr = curr, curr.simplify(expand=expand)
                print('prev2: ' + str(prev2))
                print('curr : ' + str(curr))
        simplified_input = curr.trig_simplify().fractionify()
        return simplified_input.get_latex(), str(simplified_input)
    elif isinstance(expr, CustomError):
        return '\\text{' + expr.msg + '}', ''


def testing(input_text: str, exp: bool, variable: str = 'x') -> str:
    expr = string_to_expr(input_text, {variable})
    if expr is not None:
        prev1 = None
        curr = expr
        while str(curr) != str(prev1):
            prev1, curr = curr, curr.rearrange()
            print('prev1: ' + str(prev1))
            print('curr : ' + str(curr))

            prev2 = None
            while str(curr) != str(prev2):
                # print(prev2)
                prev2, curr = curr, curr.simplify(expand=exp)  # todo: toggle expand
                print('prev2: ' + str(prev2))
                print('curr : ' + str(curr))
            # print(simplified)
        # todo: toggle below for graph
        # visualization_runner(curr)
        print(curr.get_latex())
    else:
        return '\\text{Error has occurred!}'


def tester() -> None:
    """Tester function.
    """
    while True:
        infix_expression = input('\nEnter a math expression to test (type \'stop\' to stop): ')
        if len(infix_expression) == 4 and infix_expression.lower() == 'stop':
            break
        variable = input('Enter the name of the variable to differentiate with respect to: ')
        expr = string_to_expr(infix_expression, {variable})
        print(expr)
        print(expr.get_latex())
        if expr is not None:
            prompt = input('\'s\' for simplifying, \'r\' for rearranging, \'t\' for trig simplifying')
            while prompt.lower() in {'s', 'r', 't'}:
                if prompt.lower() == 's':
                    prev = expr
                    simplified = prev.simplify(expand=False)
                    print(prev)
                    prev, simplified = simplified, simplified.simplify(expand=False)
                    print(simplified)
                    print(simplified.get_latex())
                    # visualization_runner(simplified)
                    expr = simplified
                if prompt.lower() == 'r':
                    # print('1')
                    prev = expr
                    rearranged = prev.rearrange()
                    # while str(rearranged) != str(prev):
                    #     print(prev)
                    #     prev, rearranged = rearranged, rearranged.rearrange()
                    # print('2')
                    print(rearranged)
                    visualization_runner(rearranged)
                    expr = rearranged
                if prompt.lower() == 't':
                    print(expr)
                    trig_simplified = expr.trig_simplify()
                    print(trig_simplified)
                    print(trig_simplified.get_latex())
                    expr = trig_simplified

                prompt = input('\'s\' for simplifying, \'r\' for rearranging')
    print('Program is done')


if __name__ == '__main__':
    prompt = input('\'d\' to differentiate, \'t\' to test:')
    if prompt == 'd':
        main()
    if prompt == 't':
        tester()
