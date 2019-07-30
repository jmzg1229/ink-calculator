
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
from mathml import parseCMML, MathMLInterpreter, PythonExpression

### if name main section:

# Convert MathML to sympy expression using parseCMML
# s is raw MathML expression string

# 3 - 2
s1 = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
  <mn> 3 </mn>
  <mo> - </mo>
  <mn> 2 </mn>
</math>"""

# 3 / 2 = 1.5
# s2 = r'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn> 3 </mn><mo> / </mo><mn> 2 </mn><mo> = </mo><mn> 1.5 </mn></math>'

# (1 + 2) - 3 = 0
s3 = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
  <mfenced>
    <mrow>
      <mn> 1 </mn>
      <mo> + </mo>
      <mn> 2 </mn>
    </mrow>
  </mfenced>
  <mo> - </mo>
  <mn> 3 </mn>
  <mo> = </mo>
  <mn> 0 </mn>
</math>"""

# frac(4, 2) = 2
s4 = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
  <mfrac>
    <mrow>
      <mn> 4 </mn>
    </mrow>
    <mrow>
      <mn> 2 </mn>
    </mrow>
  </mfrac>
  <mo> = </mo>
  <mn> 2 </mn>
</math>"""


s = s1

### Old implementation ###
#result = parseCMML(s)
#print(result)
##########################

intp = MathMLInterpreter(Expr=PythonExpression)

intp.get_expression(s)