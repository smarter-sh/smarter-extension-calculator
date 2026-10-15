# Smarter Extension: Calculator

An official [Smarter Extension](https://docs.smarter.sh/en/latest/smarter-framework/smarter-extensions.html)
whose `calculator` tool evaluates a math expression, such as `2 + 3 * (4 - 1)` or
`sin(pi / 2) + log(10)`, exactly, rather than letting the LLM guess. Expressions are parsed with
Python's `ast` module, and only numbers, arithmetic operators and the `math` module's functions
are evaluated: never arbitrary code.

List it in an LLMClient's manifest:

```yaml
spec:
  extensions:
    - calculator
```

Run the tests in a Smarter development container with
`python manage.py test_extension <path to this repository>`. Release by pushing a `v<version>` tag.
