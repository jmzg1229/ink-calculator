
# Mathematical Interpretation Tool (MIT, lol)

# Required packages:
# pytest

# For mathml experimental module:
# lxml
# StringIO (already in Python)

import pytest

# mathml import
from mathml import MathMLInterpreter, PythonExpression

### if name main section:

# Convert MathML to Python expression using MathMLInterpreter and PythonExpression
# s is raw MathML expression string

# Basic example:
# s = "<MathML string here>"
# intp = MathMLInterpreter()
# expr_inst = intp.get_expression(s, Expr=PythonExpression)
# print("Final expression: '{}'".format(expr_inst.expr))

def test_mathml_python_expression_01_basic_operands():
    # 1 + 2 - 3
    scorrect = '1 + 2 - 3'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 1 </mn>
      <mo> + </mo>
      <mn> 2 </mn>
      <mo> - </mo>
      <mn> 3 </mn>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic operands expressions don't match"



def test_mathml_python_expression_02_basic_parenthesis():
    # 3 - (1 + 2)
    scorrect = '3 - (1 + 2)'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 3 </mn>
      <mo> - </mo>
        <mfenced>
        <mrow>
        <mfenced>
          <mn> 1 </mn>
          <mo> + </mo>
          <mn> 2 </mn>
        </mfenced>
        </mrow>
      </mfenced>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic parenthesis expressions don't match"


def test_mathml_python_expression_03_basic_fraction():
    # frac(4, 2)
    scorrect = '4 / 2'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mfrac>
        <mrow>
          <mn> 4 </mn>
        </mrow>
        <mrow>
          <mn> 2 </mn>
        </mrow>
      </mfrac>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic fraction expressions don't match"


def test_mathml_python_expression_04_parenthesis_fraction():
    scorrect = '4 / (2 + 3)'
    # frac(4, 2 + 3)
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mfrac>
        <mrow>
          <mn> 4 </mn>
        </mrow>
        <mrow>
            <mn> 2 </mn>
            <mo> + </mo>
            <mn> 3 </mn>
        </mrow>
      </mfrac>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Parenthesis fraction expressions don't match"


def test_mathml_python_expression_05_minimal_parenthesis():
    scorrect = '(2 + 3)'
    # (2 + 3) is correct, but (((2 + 3))) is MathML given
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
    <mfenced> 
      <mfenced>
        <mrow>
            <mn> 2 </mn>
            <mo> + </mo>
            <mn> 3 </mn>
        </mrow>
      </mfenced>
    </mfenced>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Parenthesis fraction expressions don't match"


