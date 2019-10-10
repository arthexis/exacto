# Exacto

Exacto is a collection of Python tools that simplify splitting strings according to non-trivial business rules. You may find this package useful if: 

  - A regular expression is not enough for your use case.
  - You want to avoid writing and maintaining manual parsing code.
  - You don't want to mess around with LLVM or FSMs.
 
However, if performance is your primary goal, these tools may not be for you. 

# Usage

```python
from exacto import split, lift, quote, nest

# Simple example with default rules: split on whitespace
result = split("Hello   World")  
assert list(result) == ["Hello", "World"]

# Complicated example with custom separator and quotes
result = split("ENV='Prod-172.0.10.10'.VER='2.1'", quote("'"), ".")
assert list(result) == ["ENV='Prod Env'", "VER='2.1'"]

# Extract embedded tokens
result = lift("Hello [FOO] is [BAR]", nest("[", "]"))
assert list(result) == ["FOO", "BAR"]
```

