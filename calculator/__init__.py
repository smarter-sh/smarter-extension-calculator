"""
Calculator
==========

Evaluates a math expression exactly, so that the LLM computes rather than guesses.

An expression may use numbers, the operators ``+ - * / ** %``, parentheses, the constants ``pi``
and ``e``, every function of Python's ``math`` module, and ``abs``, ``round``, ``pow``, ``min``
and ``max``. It is parsed, not executed: anything else, such as a name or an attribute, is
refused.

This extension has no settings.

Tools
-----

``calculator(expression)``
    The value of the expression, e.g. ``{"result": 11}`` for ``2 + 3 * (4 - 1)``.
"""
