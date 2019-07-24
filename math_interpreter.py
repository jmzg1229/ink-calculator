
# Mathematical Interpretation Tool (MIT, lol)

# Required packages:
# For sympy & latex:
# sympy
# antlr-python-runtime (for Latex parsing)
#
# For mathml experimental module:
# lxml
# StringIO

# sympy import
from sympy.parsing.latex import parse_latex

### if name main section:

# Convert latex to sympy expression using parse_latex(s)
# s is a RAW string of latex expression
s0 = r"\frac {1 + \sqrt {\a}} {\b}"
s1 = r"\frac {P_{0}} {P}"

s = s1
expr = parse_latex(s)
print("Latex:", s)
print("Sympy expression:", expr)

# Get variables in expression