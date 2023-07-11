"""Classes for mathematical expressions"""
from typing import *

# todo: run a bunch of test cases for Plus.simplify, Plus.rearrange, Multiply.simplify, and Multiply.rearrange
# x ^ e, x ^ pi, x ^ x works
# Func ^ f(x) (e.g. ( ln ( e ) ) ^ x ) works
# Func ^ Func (e.g. ( cos ( 1 ) ) ^ sin ( 1 ) ) works
# todo: (-1) ^ x, -1 ^ x, -(1 ^ x); fix how input deals with negative signs with non-digits
# todo: 0 ^ Func and 0 ^ f(x)
# todo: sort by argument first for (trig) functions?
# todo: e ^ ln x = x simplification; a ^ (... * loga x * ...) = x ^ ... simplification (an O(n) algorithm that looks through all nodes in the exponent?)
# todo: logx ^ x????


class Expr:
    """An abstract class representing a mathematial expression.
    """

    def __str__(self) -> Any:
        return NotImplementedError

    def get_latex(self) -> Any:
        """Get the LaTeX code for the expression."""
        return NotImplementedError

    def differentiate(self, respect_to: str) -> Any:
        """Differentiate the expression."""
        return NotImplementedError

    def simplify(self) -> Any:
        """Simplify the expression."""
        return NotImplementedError

    def rearrange(self) -> Any:
        """Rearrange the expression."""
        return self

    def __lt__(self, other) -> bool:
        """Return whether self is less (lower priority) than other."""
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
            elif self_type == 'Function':  # todo: sort by argument first?
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
                print('inside __lt__')
                self_list = process_to_list(self_base)
                other_list = process_to_list(other_base)
                print(str(self_base))
                print(str(other_base))
                print(self_list)
                print(other_list)

                i = 0
                while i < len(self_list) and i < len(other_list):
                    if self_list[i][0] > other_list[i][0]:  # Note that 'b' > 'a' evaluates to True
                        print('2nd one has higher priority')
                        return True
                    elif self_list[i][0] == other_list[i][0]:  # Bases are the same; look at exponents
                        if (isinstance(self_list[i][1], int) or isinstance(self_list[i][1], float)) and \
                                (isinstance(other_list[i][1], int) or isinstance(other_list[i][1], float)):
                            if self_list[i][1] < other_list[i][1]:  # Note that 2 < 3 evaluates to True
                                print('2nd one has higher priority')
                                return True
                            if self_list[i][1] > other_list[i][1]:
                                print('1st one has higher priority')
                                return False
                        if isinstance(self_list[i][1], str) and isinstance(other_list[i][1], str):
                            if self_list[i][1] > other_list[i][1]:  # Note that 'b' > 'a' evaluates to True
                                print('2nd one has higher priority')
                                return True
                            if self_list[i][1] < other_list[i][1]:
                                print('1st one has higher priority')
                                return True
                        if not isinstance(self_list[i][1], str) and isinstance(other_list[i][1], str):
                            # Alphabets take precedence over digits
                            print('2nd one has higher priority')
                            return True
                        if isinstance(self_list[i][1], str) and not isinstance(other_list[i][1], str):
                            # Alphabets take precedence over digits
                            print('1st one has higher priority')
                            return False
                    elif self_list[i][0] < other_list[i][0]:
                        print('1st one has higher priority')
                        return False
                    i += 1
            elif self_type == 'Digit':
                if isinstance(self_base, Const) and isinstance(other_base, Const):
                    return self_base.name < other_base.name
            return False


# class Nothing(Expr):
#     """A class representing an Expr dummy holder."""
#
#     def __init__(self) -> None:
#         pass
#
#     def __str__(self) -> str:
#         return 'nothing '


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
        return str(self.name) + ' '

    def get_latex(self) -> str:
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


class Plus(BinOp):
    """Represents the binary operation of adding two expressions.

    Instance Attributes:
        - left: the expression to the left of the plus sign
        - right: the expression to the right of the plus sign
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        return '( ' + str(self.left) + '+ ' + str(self.right) + ') '

    def get_latex(self) -> str:
        return self.left.get_latex() + '+ ' + self.right.get_latex()

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
        if isinstance(self.left, Const) and isinstance(self.right, Const) and \
                (isinstance(self.left.name, int) or isinstance(self.left.name, float)) and \
                (isinstance(self.right.name, int) or isinstance(self.right.name, float)):
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
        old_lst = expr_to_list(self, self)
        # assert(len(lst) >= 2)
        lst = []
        for item in old_lst:
            lst.append(item.rearrange())
        print([str(item) for item in lst])

        # Step 2: Sort the list
        lst.sort(reverse=True)

        print([str(item) for item in lst])

        # Step 3: Insert all the objects into a new Plus binary tree
        tree = Plus(lst[0], lst[1])
        for i in range(2, len(lst)):
            tree = Plus(tree, lst[i])

        return tree


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
        return '( ' + str(self.left) + '* ' + str(self.right) + ') '

    def get_latex(self) -> str:
        if isinstance(self.left, Plus):
            left_latex = '( ' + self.left.get_latex() + ') '
        else:
            left_latex = self.left.get_latex()
        if isinstance(self.right, Pow) and isinstance(self.right.right, Const) and self.right.right.name == -1:
            return '\\displaystyle\\frac{ ' + left_latex + '}{ ' + self.right.left.get_latex() + '} '
        if isinstance(self.right, Plus):
            right_latex = '( ' + self.right.get_latex() + ') '
        else:
            right_latex = self.right.get_latex()
        return left_latex + '\\cdot ' + right_latex

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
            return Pow(self.left.simplify(), Const(2))

        if isinstance(self.left, Const) and isinstance(self.right, Const) and not isinstance(self.left.name, str) \
                and not isinstance(self.right.name, str):
            return Const(self.left.name * self.right.name)

        # Power * Power with same bases
        if isinstance(self.left, Pow) and isinstance(self.right, Pow) \
                and str(self.left.left) == str(self.right.left):
            return Pow(self.left.left.simplify(),
                       Plus(self.left.right.simplify(), self.right.right.simplify()).simplify())

        # (base ^ exp_1) * base
        if isinstance(self.left, Pow) and str(self.left.left) == str(self.right):
            return Pow(self.left.left.simplify(),
                       Plus(self.left.right.simplify(), Const(1)).simplify())

        # Multiply * something else
        if isinstance(self.left, Multiply) and not isinstance(self.right, Multiply):
            left_simplified = self.left.simplify()
            if str(left_simplified) != str(self.left):
                return Multiply(left_simplified, self.right).simplify()
            else:
                lr_and_r_simplified = Multiply(self.left.right, self.right).simplify()
                if str(lr_and_r_simplified) != str(Multiply(self.left.right, self.right)):
                    return Multiply(self.left.left, lr_and_r_simplified).simplify()

        # # <some_type> * (<some_type> * Expr)
        # if isinstance(self.right, Multiply) and type(self.left) == type(self.right.left):
        #     return Multiply(Multiply(self.left.simplify(),
        #                              self.right.left.simplify()).simplify(), self.right.right.simplify())  # .simplify()
        #
        # # <some_type> * (Expr * <some_type>)
        # if isinstance(self.right, Multiply) and type(self.left) == type(self.right.right):
        #     return Multiply(Multiply(self.left.simplify(),
        #                              self.right.right.simplify()).simplify(), self.right.left.simplify())  # .simplify()
        #
        # # (<some_type> * Expr) * <some_type>
        # if isinstance(self.left, Multiply) and type(self.right) == type(self.left.left):
        #     return Multiply(Multiply(self.right.simplify(), self.left.left.simplify()).simplify(),
        #                     self.left.right.simplify())  # .simplify()
        #
        # # (Expr * <some_type>) * <some_type>
        # if isinstance(self.left, Multiply) and type(self.right) == type(self.left.right):
        #     return Multiply(Multiply(self.right.simplify(), self.left.right.simplify()).simplify(),
        #                     self.left.left.simplify())  # .simplify()

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
        #         return Multiply(Multiply(self.left.left.simplify(), self.right.left.simplify()).simplify(),
        #                         Multiply(self.left.right.simplify(),
        #                                  self.right.right.simplify()).simplify())  # .simplify()
        #     # Case 2: a and d are the same type
        #     if type(self.left.left) == type(self.right.right):
        #         return Multiply(Multiply(self.left.left.simplify(), self.right.right.simplify()).simplify(),
        #                         Multiply(self.left.right.simplify(),
        #                                  self.right.left.simplify()).simplify())  # .simplify()
        #     # Case 3: b and c are the same type
        #     if type(self.left.right) == type(self.right.left):
        #         return Multiply(Multiply(self.left.right.simplify(), self.right.left.simplify()).simplify(),
        #                         Multiply(self.left.left.simplify(),
        #                                  self.right.right.simplify()).simplify())  # .simplify()
        #     # Case 4: b and d are the same type
        #     if type(self.left.right) == type(self.right.right):
        #         return Multiply(Multiply(self.left.right.simplify(), self.right.right.simplify()).simplify(),
        #                         Multiply(self.left.left.simplify(),
        #                                  self.right.left.simplify()).simplify())  # .simplify()

        return Multiply(self.left.simplify(), self.right.simplify())

    def rearrange(self) -> Any:
        """Rearrange the Multiply expression."""
        # Step 1: Insert all the non-Plus Expr objects into a list
        old_lst = expr_to_list(self, self)
        # assert(len(lst) >= 2)
        lst = []
        for item in old_lst:
            lst.append(item.rearrange())
        print([str(item) for item in lst])

        # Step 2: Sort the list
        lst.sort(reverse=True)

        print([str(item) for item in lst])

        # Step 3: Insert all the objects into a new Multiply binary tree
        #      *
        #     / \
        # coeff  *
        #       / \
        #     ... power

        i = 0
        fractions = None
        if get_arrangement_type(lst[i])[0] == 'Power':  # Is it a Power?
            power_tree = Const(1)
            # Create power_tree; filter out any Pows with negative exponents
            power_tree, i, end_of_power, fractions = get_power_tree(i, lst, power_tree, fractions)

            if i == len(lst) and isinstance(end_of_power.left, Multiply):  # All items were Power objects
                if end_of_power:
                    end_of_power.left = end_of_power.left.right
                if fractions:
                    return Multiply(power_tree, Pow(fractions, Const(-1)))
                else:
                    return power_tree
            elif get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:  # Is it a "Rest"?
                rest_tree = Const(1)
                # Create rest_tree; filter out any Pows with negative exponents
                rest_tree, i, fractions = get_rest_tree(i, lst, rest_tree, fractions)

                # Attatch rest_tree to power_tree
                if end_of_power:
                    end_of_power.left.left = rest_tree
                else:  # If power_tree contains only 1 Power object
                    power_tree.left = rest_tree

                if i == len(lst):
                    if fractions:
                        return Multiply(power_tree, Pow(fractions, Const(-1)))
                    else:
                        return power_tree
                elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                    non_digit_tree = Const(1)
                    # Create non_digit_tree
                    non_digit_tree, i, fractions = get_non_digit_tree(i, lst, non_digit_tree, fractions)
                    if i == len(lst):
                        if fractions:
                            return Multiply(Multiply(non_digit_tree, power_tree), Pow(fractions, Const(-1)))
                        else:
                            return Multiply(non_digit_tree, power_tree)
                    else:  # Must be a Digit
                        digit_tree = Const(1)
                        # Create digit_tree
                        digit_tree = get_digit_tree(i, lst, digit_tree)
                        if fractions:
                            return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), power_tree),
                                            Pow(fractions, Const(-1)))
                        else:
                            return Multiply(Multiply(digit_tree, non_digit_tree), power_tree)
                else:  # Must be a Digit
                    digit_tree = Const(1)
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    if fractions:
                        return Multiply(Multiply(digit_tree, Multiply(rest_tree, power_tree)),
                                        Pow(fractions, Const(-1)))
                    else:
                        return Multiply(digit_tree, Multiply(rest_tree, power_tree))
            elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                non_digit_tree = Const(1)
                # Create non_digit_tree
                non_digit_tree, i, fractions = get_non_digit_tree(i, lst, non_digit_tree, fractions)
                if i == len(lst):
                    if fractions:
                        return Multiply(Multiply(non_digit_tree, power_tree), Pow(fractions, Const(-1)))
                    else:
                        return Multiply(non_digit_tree, power_tree)
                else:  # Must be a Digit
                    digit_tree = Const(1)
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    if fractions:
                        return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), power_tree),
                                        Pow(fractions, Const(-1)))
                    else:
                        return Multiply(Multiply(digit_tree, non_digit_tree), power_tree)
            else:  # Must be a digit tree
                digit_tree = Const(1)
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                if fractions:
                    return Multiply(Multiply(digit_tree, power_tree), Pow(fractions, Const(-1)))
                else:
                    return Multiply(digit_tree, power_tree)
        elif get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:  # Is it a Rest?
            rest_tree = Const(1)
            # Create rest_tree; filter out any Pows with negative exponents
            rest_tree, i, fractions = get_rest_tree(i, lst, rest_tree, fractions)
            if i == len(lst):
                if fractions:
                    return Multiply(rest_tree, Pow(fractions, Const(-1)))
                else:
                    return rest_tree
            elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
                non_digit_tree = Const(1)
                # Create non_digit_tree
                non_digit_tree, i, fractions = get_non_digit_tree(i, lst, non_digit_tree, fractions)
                if i == len(lst):
                    if fractions:
                        return Multiply(Multiply(non_digit_tree, rest_tree), Pow(fractions, Const(-1)))
                    else:
                        return Multiply(non_digit_tree, rest_tree)
                else:  # Must be a Digit
                    digit_tree = Const(1)
                    # Create digit_tree
                    digit_tree = get_digit_tree(i, lst, digit_tree)
                    if fractions:
                        return Multiply(Multiply(Multiply(digit_tree, non_digit_tree), rest_tree),
                                        Pow(fractions, Const(-1)))
                    else:
                        return Multiply(Multiply(digit_tree, non_digit_tree), rest_tree)
            else:  # Must be a Digit
                digit_tree = Const(1)
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                if fractions:
                    return Multiply(Multiply(digit_tree, rest_tree), Pow(fractions, Const(-1)))
                else:
                    return Multiply(digit_tree, rest_tree)
        elif get_arrangement_type(lst[i])[0] == 'Non-digit':  # Is it a Non-digit?
            non_digit_tree = Const(1)
            # Create non_digit_tree
            non_digit_tree, i, fractions = get_non_digit_tree(i, lst, non_digit_tree, fractions)
            if i == len(lst):
                if fractions:
                    return Multiply(non_digit_tree, Pow(fractions, Const(-1)))
                else:
                    return non_digit_tree
            else:  # Must be a digit
                digit_tree = Const(1)
                # Create digit_tree
                digit_tree = get_digit_tree(i, lst, digit_tree)
                if fractions:
                    return Multiply(Multiply(digit_tree, non_digit_tree), Pow(fractions, Const(-1)))
                else:
                    return Multiply(digit_tree, non_digit_tree)
        else:  # Must be a Digit
            digit_tree = Const(1)
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


def get_power_tree(i: int, lst: list, power_tree: Expr, fractions: Optional[Expr]) -> tuple:
    """Returns a tuple in the form of (power_tree, new_index, end_of_power, fractions),
    where fractions is a Multiply object containing any Pow objects with negative exponents.
    fractions is None if there are no Pow objects with negative exponents.
    """
    end_of_power = None
    while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Power':
        if isinstance(lst[i], Pow):
            negative, abs_of_exponent = is_minus(lst[i].right)
            if negative:
                if fractions is None:  # If this is the first fraction
                    fractions = Pow(lst[i].left, abs_of_exponent)
                else:
                    fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
            else:
                power_tree = Multiply(power_tree, lst[i])
        else:
            power_tree = Multiply(power_tree, lst[i])
        if i == 1:
            end_of_power = power_tree
        i += 1
    return (power_tree, i, end_of_power, fractions)


def get_rest_tree(i: int, lst: list, rest_tree: Expr, fractions: Optional[Expr]) -> tuple:
    """Returns a tuple in the form of (rest_tree, new_index, fractions),
    where fractions is a Multiply object containing any Pow objects with negative exponents.
    fractions is None if there are no Pow objects with negative exponents.
    """
    while i < len(lst) and get_arrangement_type(lst[i])[0] not in {'Non-digit', 'Digit'}:
        if isinstance(lst[i], Pow):
            negative, abs_of_exponent = is_minus(lst[i].right)
            if negative:
                if fractions is None:  # If this is the first fraction
                    fractions = Pow(lst[i].left, abs_of_exponent)
                else:
                    fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
            else:
                rest_tree = Multiply(rest_tree, lst[i])
        else:
            rest_tree = Multiply(rest_tree, lst[i])
        i += 1
    return (rest_tree, i, fractions)


def get_non_digit_tree(i: int, lst: list, non_digit_tree: Expr, fractions: Optional[Expr]) -> tuple:
    """Returns a tuple in the form of (non_digit_tree, new_index, fractions),
    where fractions is a Multiply object containing any Pow objects with negative exponents.
    fractions is None if there are no Pow objects with negative exponents.
    """
    while i < len(lst) and get_arrangement_type(lst[i])[0] == 'Non-digit':
        if isinstance(lst[i], Pow):
            negative, abs_of_exponent = is_minus(lst[i].right)
            if negative:
                if fractions is None:  # If this is the first fraction
                    fractions = Pow(lst[i].left, abs_of_exponent)
                else:
                    fractions = Multiply(fractions, Pow(lst[i].left, abs_of_exponent))
            else:
                non_digit_tree = Multiply(non_digit_tree, lst[i])
        else:
            non_digit_tree = Multiply(non_digit_tree, lst[i])
        i += 1
    return (non_digit_tree, i, fractions)


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

    def differentiate(self, respect_to: str) -> Expr:
        return Const(0)

    def simplify(self) -> Expr:
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
        if isinstance(self.right, Const) and self.right.name == -1:
            return '\\displaystyle\\frac{1}{ ' + self.left.get_latex() + '} '
        if isinstance(self.left, Trig):
            return '{ \\' + self.left.name + '} ' + '^' + '{ ' + self.right.get_latex() + '} ' + '( ' + self.left.arg.get_latex() + ') '
        if isinstance(self.left, Log):
            if self.left.base.name == 'e':
                return '{ \\ln } ' + '^' + '{ ' + self.right.get_latex() + '} ' + '( ' + self.left.arg.get_latex() + ') '
            return '{\\log_{ ' + self.left.base.get_latex() + '} } ' + '^' + '{ ' + self.right.get_latex() + '} ' + '( ' + self.left.arg.get_latex() + ') '
        if isinstance(self.left, Plus) or isinstance(self.left, Multiply) or isinstance(self.left, Pow) or is_minus(self.left)[0]:
            left_latex = '( ' + self.left.get_latex() + ') '
        else:
            left_latex = self.left.get_latex()
        minus, abs_val = is_minus(self.right)
        if minus:
            return '\\displaystyle\\frac{1}{ ' + left_latex + '^ ' + abs_val.get_latex() + '} '
        else:
            return '{ ' + left_latex + '} ' + '^' + '{ ' + self.right.get_latex() + '} '

    def differentiate(self, respect_to: str) -> Expr:
        if isinstance(self.left, Const) and isinstance(self.right, Const):
            return Const(0)

        # Power rule for int or float exponents
        if not isinstance(self.left, Const) and isinstance(self.right, Const) \
                and (isinstance(self.right.name, int) or (isinstance(self.right.name, float))):
            return Multiply(Multiply(self.right,
                                     Pow(self.left, Const(self.right.name - 1))), self.left.differentiate(respect_to))

        # Power rule for str exponenets
        if not isinstance(self.left, Const) and isinstance(self.right, Const) and isinstance(self.right.name, str):
            return Multiply(Multiply(self.right,
                                     Pow(self.left, Plus(self.right, Const(-1)))), self.left.differentiate(respect_to))

        # e ^ f(x)
        if isinstance(self.left, Const) and self.left.name == 'e' and not isinstance(self.right, Const):
            return Multiply(self, self.right.differentiate(respect_to))

        # Const ^ f(x)
        if isinstance(self.left, Const) and not isinstance(self.right, Const):
            return Multiply(self, Multiply(Log(Const('e'), self.left), self.right.differentiate(respect_to)))

        return Pow(Const('e'), Multiply(self.right, Log(Const('e'), self.left))).differentiate(respect_to)

    def simplify(self) -> Expr:
        if isinstance(self.right, Const) and self.right.name == 1:
            return self.left.simplify()

        return Pow(self.left.simplify(), self.right.simplify())

    def rearrange(self) -> Expr:
        return Pow(self.left.rearrange(), self.right.rearrange())


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
        return self.name + ' ( ' + str(self.arg) + ') '

    def get_latex(self) -> str:
        return '\\' + self.name + ' ( ' + self.arg.get_latex() + ') '

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
            return Multiply(Pow(Trig('sec', self.arg), Const(2)),
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
                            Multiply(Pow(Trig('csc', self.arg), Const(2)),
                                     self.arg.differentiate(respect_to)
                                     )
                            )

        if self.name == 'arcsin':
            return Multiply(self.arg.differentiate(respect_to),
                            Pow(Plus(Const(1),
                                     Multiply(Const(-1),
                                              Pow(self.arg,
                                                  Const(2)))), Const(-0.5))
                            )
        if self.name == 'arccos':
            return Multiply(Const(-1), Trig('arcsin', self.arg).differentiate(respect_to))
        if self.name == 'arctan':
            return Multiply(self.arg.differentiate(respect_to),
                            Pow(Plus(Pow(self.arg, Const(2)), Const(1)), Const(-1))
                            )

    def simplify(self) -> Expr:
        return Trig(self.name, self.arg.simplify())


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
            return 'ln ( ' + str(self.arg) + ') '
        else:
            return 'log' + str(self.base) + '( ' + str(self.arg) + ') '

    def get_latex(self) -> str:
        if self.base.name == 'e':
            return '\\ln ( ' + self.arg.get_latex() + ') '
        else:
            return '\\log_{' + self.base.get_latex() + '} ( ' + self.arg.get_latex() + ') '

    def differentiate(self, respect_to: str) -> Expr:
        if not isinstance(self.arg, Const):
            if self.base.name == 'e':
                return Multiply(self.arg.differentiate(respect_to), Pow(self.arg, Const(-1)))
            else:
                return Multiply(self.arg.differentiate(respect_to),
                                Pow(Multiply(self.arg, Log(Const('e'), self.base)), Const(-1))
                                )
        else:
            # Then it is a constant!
            return Const(0)

    def simplify(self) -> Expr:
        if self.base.name == 'e' and isinstance(self.arg, Const) and self.arg.name == 'e':
            return Const(1)
        return Log(self.base, self.arg.simplify())


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
    (type, base, exponent, coefficient, function_name)
    """
    if isinstance(expr, Var):
        return ('Power', expr, Const(1), Const(1), None)  # 4
    if isinstance(expr, Func):
        return ('Function', expr, Const(1), Const(1), expr.name)  # 10
    if isinstance(expr, Const) and isinstance(expr.name, str):
        return ('Non-digit', expr, Const(1), Const(1), None)  # 13
    if isinstance(expr, Const) and (isinstance(expr.name, int) or isinstance(expr.name, float)):
        return ('Digit', expr, Const(1), Const(1), None)  # 18
    if isinstance(expr, Multiply):
        expr_left_type = get_arrangement_type(expr.left)[0]
        if expr_left_type == 'Non-digit':
            if get_arrangement_type(expr.right)[0] == 'Non-digit':
                return ('Non-digit', expr, Const(1), Const(1), None)  # 15
        if expr_left_type == 'Digit':
            if get_arrangement_type(expr.right)[0] == 'Non-digit':
                return ('Non-digit', expr.right, Const(1), expr.left, None)  # 14
        if expr_left_type in {'Non-digit', 'Digit'}:
            if isinstance(expr.right, Pow) and isinstance(expr.right.left, Var) \
                    and get_arrangement_type(expr.right.right)[0] in {'Non-digit', 'Digit'}:
                return ('Power', expr.right.left, expr.right.right, expr.left, None)  # 1
            if isinstance(expr.right, Var):
                return ('Power', expr.right, Const(1), expr.left, None)  # 3
            if isinstance(expr.right, Pow) and get_arrangement_type(expr.right.left)[0] in {'Non-digit',
                                                                                              'Digit'} \
                    and get_arrangement_type(expr.right.right)[0] == 'Power':
                return ('Exponential', expr.right.left, expr.right.right, expr.left, None)  # 5, 8
            if isinstance(expr.right, Func):
                return ('Function', expr, Const(1), expr.left, expr.right.name)  # 9
            if isinstance(expr.right, Pow) and isinstance(expr.right.left, Func) \
                    and get_arrangement_type(expr.right.right)[0] in {'Non-digit', 'Digit'}:
                return ('Function', expr.right.left, expr.right.right, expr.left, expr.right.left.name)  # 11
    if isinstance(expr, Pow):
        if isinstance(expr.left, Const) and isinstance(expr.left.name, str):
            if isinstance(expr.right, Const):
                return ('Non-digit', expr.left, expr.right, Const(1), None)  # 16, 17
        expr_left_type = get_arrangement_type(expr.left)[0]
        if expr_left_type in {'Non-digit', 'Digit'}:
            if get_arrangement_type(expr.right)[0] == 'Power':
                return ('Exponential', expr.left, expr.right, Const(1), None)  # 6, 7
        if get_arrangement_type(expr.right)[0] in {'Non-digit', 'Digit'}:
            if isinstance(expr.left, Var):
                return ('Power', expr.left, expr.right, Const(1), None)  # 2
            if isinstance(expr.left, Func):
                return ('Function', expr.left, expr.right, Const(1), expr.left.name)  # 12

    return ('Other', expr, Const(1), Const(1), None)


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
