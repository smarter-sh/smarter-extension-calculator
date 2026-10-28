"""Tests of the calculator tool and its evaluator."""

import math
import unittest

from calculator.evaluator import CalculatorError, evaluate
from calculator.tools import Calculator

from smarter.apps.llmtool.extension.testing import call_tool


class TestEvaluator(unittest.TestCase):
    """Test the safe evaluator."""

    def test_expressions(self):
        cases = {
            "2 + 3 * (4 - 1)": 11,
            "-2 ** 2": -4,
            "+7 % 4": 3,
            "10 / 4": 2.5,
            "sin(pi / 2) + log(e)": 2.0,
            "max(1, 2, 3) - abs(-1)": 2,
            "round(sqrt(2), 3)": 1.414,
        }
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                self.assertTrue(math.isclose(evaluate(expression), expected))

    def test_refused(self):
        for expression in (
            "__import__('os')",
            "open('/etc/passwd')",
            "(1).__class__",
            "x + 1",
            "'a' * 3",
            "True + 1",
            "1 if 1 else 2",
            "pi()",
            "sqrt(x=4)",
            "9 ** 9 ** 9",
            "1 / 0",
            "sqrt(-1)",
            "2 +",
            "sin",
        ):
            with self.subTest(expression=expression):
                with self.assertRaises(CalculatorError):
                    evaluate(expression)


class TestCalculator(unittest.TestCase):
    """Test the tool."""

    def test_cache_ttl(self):
        """The tool changes nothing, and its result doesn't depend on who asks, so a result is cached for an hour."""
        self.assertEqual(Calculator.cache_ttl, 3600)

    def test_call(self):
        self.assertEqual(call_tool(Calculator, {"expression": "2 + 2"}), {"result": 4})
        self.assertEqual(
            call_tool(Calculator, {"expression": "1 / 0"}), {"error": "Could not evaluate 1 / 0: division by zero"}
        )
        self.assertIn("Invalid arguments", call_tool(Calculator, {"expression": ""})["error"])
        self.assertEqual(Calculator.problems(), [])
