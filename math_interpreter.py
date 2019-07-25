
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

# mathml import
from mathml import parseCMML

### if name main section:

# Convert MathML to sympy expression using parseCMML
# s is raw MathML expression string
#s = r'<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>/</mo><mi>b</mi></math>'
s = r'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1</mn><mo>*</mo><mn>2</mn></math>'
result = parseCMML(s)
print(result)

# Convert latex to sympy expression using parse_latex(s)
# s is a RAW string of latex expression
#s0 = r"\frac {1 + \sqrt {\a}} {\b}"
#s1 = r"\frac {P_{0}} {P}"

#s = s1
#expr = parse_latex(s)
#print("Latex:", s)
#print("Sympy expression:", expr)

# Get variables in expression