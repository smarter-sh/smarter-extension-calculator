"""The calculator extension's tools."""

from pydantic import BaseModel, Field, JsonValue

from smarter.apps.llmtool.extension import ExtensionContext, ExtensionToolError, SmarterExtensionTool

from .evaluator import CalculatorError, evaluate


class CalculatorArguments(BaseModel):
    """The arguments of the calculator tool."""

    expression: str = Field(
        ...,
        min_length=1,
        description="A math expression, with numbers, + - * / ** %, parentheses, pi, e, and the functions "
        "of Python's math module, e.g. '2 + 3 * (4 - 1)' or 'sin(pi / 2) + log(10)'.",
    )


class Calculator(SmarterExtensionTool):
    """
    Evaluate a math expression exactly. Use it for every calculation, rather than calculating in
    your head.
    """

    name = "calculator"
    arguments_model = CalculatorArguments
    cache_ttl = 3600
    """An expression always has the same result, whoever asks."""

    def call(self, arguments: CalculatorArguments, context: ExtensionContext) -> JsonValue:
        try:
            return {"result": evaluate(arguments.expression)}
        except CalculatorError as e:
            raise ExtensionToolError(f"Could not evaluate {arguments.expression}: {e}") from e
