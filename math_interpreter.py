
# Mathematical Interpretation Tool (MIT, lol)

# Required packages:
# sympy
# antlr-python-runtime (for Latex parsing)

# sympy import
from sympy.parsing.latex import parse_latex

### if name main section:

# Convert latex to sympy expression using parse_latex(s)
# s is a RAW string of latex expression
s = r"\frac {1 + \sqrt {\a}} {\b}"
expr = parse_latex(s)
print("Latex:", s)
print("Sympy expression:", expr)

# Get variables in expression