# Smarter Extension: Calculator

[![Build Status](https://img.shields.io/github/actions/workflow/status/smarter-sh/smarter-extension-calculator/release.yml?label=build&logo=github)](https://github.com/smarter-sh/smarter-extension-calculator/actions/workflows/release.yml)
[![Test Status](https://github.com/smarter-sh/smarter-extension-calculator/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/smarter-sh/smarter-extension-calculator/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/codecov/c/github/smarter-sh/smarter-extension-calculator/main?label=coverage&logo=codecov)](https://codecov.io/gh/smarter-sh/smarter-extension-calculator)
[![Latest Release](https://img.shields.io/github/v/release/smarter-sh/smarter-extension-calculator?label=release)](https://github.com/smarter-sh/smarter-extension-calculator/releases)
[![Official Smarter Extension](https://img.shields.io/badge/Smarter%20Extension-official-0b6e4f)](https://github.com/smarter-sh/extensions-registry)
[![Docs](https://img.shields.io/badge/Read%20the%20Docs-smarter.sh-blue?logo=readthedocs)](https://docs.smarter.sh/en/latest/smarter-framework/smarter-extensions.html)
[![License: GNU AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

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
`python manage.py test_extension <path to this repository>`. CI runs them on every push and pull
request, against a source checkout of Smarter. Release by pushing a `v<version>` tag.
