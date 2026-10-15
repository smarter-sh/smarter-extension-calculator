"""A safe evaluator of math expressions, which parses them and evaluates only the nodes it allows."""

import ast
import math
import operator
from typing import Callable, Union

Number = Union[int, float]

ALLOWED_NAMES: dict[str, Union[Number, Callable]] = {
    **{name: getattr(math, name) for name in dir(math) if not name.startswith("_")},
    "abs": abs,
    "round": round,
    "pow": pow,
    "min": min,
    "max": max,
}
BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
MAX_EXPONENT = 10_000
"""The largest exponent allowed, so that an expression like 9**9**9 cannot exhaust the platform's memory."""


class CalculatorError(Exception):
    """An expression is not valid, or cannot be evaluated."""


def evaluate(expression: str) -> Number:
    """
    Evaluate a math expression.

    :param expression: e.g. ``sin(pi / 2) + log(10)``.
    :returns: Its value.
    :raises CalculatorError: If the expression is not valid, uses anything that is not allowed, or fails.
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise CalculatorError(f"not a valid expression: {e.msg}") from e
    try:
        value = _evaluate(tree.body)
    except CalculatorError:
        raise
    except (ArithmeticError, ValueError, TypeError) as e:
        raise CalculatorError(str(e)) from e
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculatorError("the expression is not a number")
    return value


def _evaluate(node: ast.AST) -> Union[Number, Callable]:
    """Evaluate one node of an expression's syntax tree."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise CalculatorError(f"{node.id} is not allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and isinstance(right, (int, float)) and abs(right) > MAX_EXPONENT:
            raise CalculatorError(f"exponents larger than {MAX_EXPONENT} are not allowed")
        return BINARY_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.Call) and not node.keywords:
        function = _evaluate(node.func)
        if not callable(function):
            raise CalculatorError("only functions can be called")
        return function(*[_evaluate(argument) for argument in node.args])
    raise CalculatorError(f"{type(node).__name__} is not allowed")
