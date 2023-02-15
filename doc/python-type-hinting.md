# Python Type Hinting

As a team we have committed to adding type hints throughout the Python code. This document defines our approach to type hinting, to ensure consistency in the codebase and avoid repeating discussions about how we apply typing.

## Variables

Specify types for variables initialised with `None`:

```python
description: Optional[str] = None
```

Specify types for empty collections:

```python
items: list[str] = []
mappings: dict[str, int] = {}
```

In all other places, types for variables are optional.

## Standard collections

For standard collections, use lower case names e.g `list` rather than `List`:

```python
items: list[int] = [1]
mappings: set[int] = {1, 2}
```

https://www.python.org/dev/peps/pep-0585/

## Generic types

Specify at least the top-level type parameters for all generic types:

```python
def get_objects_matching(ids: Sequence[str]) -> dict[int, dict]
```

## Optional arguments

For arguments that can be a single type or None, use the shorthand `|`. This is recommended instead of using older `Optional` keyword:

```python
def test(self, var: [None | int]) -> None:
```

For arguments that can be one of multiple types or None, use the shorthand `|`. This is recommended instead of using older `Union` keyword:

```python
def test(self, var: [None | int | str]) -> None:
```

## Abstract vs concrete

- Make argument types as abstract as possible (to be flexible to callers)
- Make return types as specific as possible (to be predictable to callers)

```python
    def increment_values(self, values: Sequence[int]) -> list[int]:
        return [value + 1 for value in values]
```

## Forward declarations

To reference a type before it has been declared e.g. using a class as a type within the class declaration, add the special `annotations` import:

```python
from __future__ import annotations

class TestClass:

  def test(self, var: Sequence[TestClass]) -> None:
```

This import is not necessary in Python 3.10.

https://www.python.org/dev/peps/pep-0563/

## Type Ignore

To mark portions of the program that should not be covered by type hinting, use the following on a particular line:

```python
# type: ignore
```

A `# type: ignore` comment on a line by itself at the top of a file silences all errors in the file.

`# type: ignore` should only be used when unavoidable. Ensure that a comment is added to explain why it has been used and have a prefix of Type ignore:.

## ParamSpec

Use to forward the parameter types of one callable to another callable e.g. to add basic logging to a function, create a decorator `add_logging` to log function calls:

```python
T = TypeVar('T')
P = ParamSpec('P')

def add_logging(f: Callable[P, T]) -> Callable[P, T]:
    '''A type-safe decorator to add logging to a function.'''
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.info(f'{f.__name__} was called')
        return f(*args, **kwargs)
    return inner

@add_logging
def add_two(x: float, y: float) -> float:
    '''Add two numbers together.'''
    return x + y
```

## TypeVar

Use `TypeVar` when the type returned by a function is the same as the type which was passed in i.e. the return type is linked to the parameter type:

```python
T = TypeVar('T')

def increment_value(self, value: T) -> T:
    return value + 1
```

`TypeVar` also accepts extra positional arguments to restrict the type parameter.

```python
T = TypeVar('T', int, float)

def increment_value(self, value: T) -> T:
    return value + 1
```

This tells the typechecker that values other than `int` and `float` are not allowed, resulting in an error:

```python
increment_value(self, "hello") #error
```

## Useful links

- https://www.python.org/dev/peps/pep-0484/
- https://www.pythonsheets.com/notes/python-typing.html
- https://google.github.io/styleguide/pyguide.html#319-type-annotations
