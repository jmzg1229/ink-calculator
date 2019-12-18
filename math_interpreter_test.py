
# Mathematical Interpretation Tool (MIT, lol)

# Required packages:
# pytest

# For mathml experimental module:
# lxml
# StringIO (already in Python)

import pytest

# mathml import
from mathml import MathMLInterpreter
from expression_classes import PythonExpression, SympyExpression

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

def test_mathml_python_expression_06_basic_symbols():
    # 1 + 2 - 3
    scorrect = 'x + y - z'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mi> x </mi>
      <mo> + </mo>
      <mi> y </mi>
      <mo> - </mo>
      <mi> z </mi>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic symbols expressions don't match"

    # All symbols registered
    syms_registered = (x in ('x','y','z') for x in expr_instance.symbol_library)
    assert all(syms_registered)

def test_mathml_python_expression_07_basic_equation():
    # 1 + 2 - 3
    scorrect = '1 + 2 - 3 = 0'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 1 </mn>
      <mo> + </mo>
      <mn> 2 </mn>
      <mo> - </mo>
      <mn> 3 </mn>
      <mo> = </mo>
      <mn> 0 </mn>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic operands expressions don't match"

def test_mathml_python_expression_08_basic_power():
    # 1 + 2 - 3
    scorrect = '2 ** 3'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <msup>
        <mrow>
          <mn> 2 </mn>
        </mrow>
        <mrow>
          <mn> 3 </mn>
        </mrow>
      </msup>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic operands expressions don't match"

def test_mathml_python_expression_09_basic_subscript():
    # 2 ** 3 -> 8
    scorrect = 'P_{0}'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <msub>
        <mrow>
          <mi> P </mi>
        </mrow>
        <mrow>
          <mn> 0 </mn>
        </mrow>
      </msub>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=PythonExpression)
    py_expr = expr_instance.expr
    assert py_expr == scorrect, "Basic subscript expressions don't match"

    # All symbols registered
    syms_registered = (x in ('P_{0}',) for x in expr_instance.symbol_library)
    assert all(syms_registered)

### SympyExpression Tests ###########

def test_mathml_sympy_expression_00_basic_number():
    # 1 + 2 - 3 -> 0
    scorrect = '2'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 2 </mn>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic SymPy number expressions don't match"

def test_mathml_sympy_expression_01_basic_operands():
    # 1 + 2 - 3 -> 0
    scorrect = '-3 + 1 + 2'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 1 </mn>
      <mo> + </mo>
      <mn> 2 </mn>
      <mo> - </mo>
      <mn> 3 </mn>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic SymPy operands expressions don't match"


def test_mathml_sympy_expression_02_basic_symbols():
    # 1 + 2 - 3
    scorrect = '-z + x + y'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mi> x </mi>
      <mo> + </mo>
      <mi> y </mi>
      <mo> - </mo>
      <mi> z </mi>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic SymPy operands expressions don't match"

    # All symbols registered
    syms_registered = (x in ('x','y','z') for x in expr_instance.symbol_library)
    assert all(syms_registered)

def test_mathml_sympy_expression_03_basic_equation():
    # 1 + 2 - 3
    scorrect = 'Eq(x + y, 3)'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mi> x </mi>
      <mo> + </mo>
      <mi> y </mi>
      <mo> = </mo>
      <mn> 3 </mn>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic equations expressions don't match"

    # All symbols registered
    syms_registered = (x in ('x','y') for x in expr_instance.symbol_library)
    assert all(syms_registered)

def test_mathml_sympy_expression_04_basic_power():
    # 2 ** 3 -> 8
    scorrect = '2**3'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <msup>
        <mrow>
          <mn> 2 </mn>
        </mrow>
        <mrow>
          <mn> 3 </mn>
        </mrow>
      </msup>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic power expressions don't match"

def test_mathml_sympy_expression_05_basic_subscript():
    # 2 ** 3 -> 8
    scorrect = 'P_{0}'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <msub>
        <mrow>
          <mi> P </mi>
        </mrow>
        <mrow>
          <mn> 0 </mn>
        </mrow>
      </msub>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Basic subscript expressions don't match"

    # All symbols registered
    syms_registered = (x in ('P_{0}') for x in expr_instance.symbol_library)
    assert all(syms_registered)

def test_mathml_sympy_expression_06_division_subscript():
    # 2 ** 3 -> 8
    scorrect = 'P/P_{0}'
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mfrac>
        <mrow>
          <mi> P </mi>
        </mrow>
        <mrow>
          <msub>
            <mrow>
              <mi> P </mi>
            </mrow>
            <mrow>
              <mn> 0 </mn>
            </mrow>
          </msub>
        </mrow>
      </mfrac>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_instance.expr
    assert str(sympy_expr) == scorrect, "Division subscript expressions don't match"
    # All symbols registered
    syms_registered = (x in ('P','P_{0}') for x in expr_instance.symbol_library)
    assert all(syms_registered)

def test_mathml_sympy_expression_group_expression():
    # Groups of expressions: x+y=2, x-y=1
    scorrect = ['Eq(x + y, 2)', 'Eq(x - y, 1)']
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mtable columnalign='left'>
        <mtr>
          <mtd>
            <mi> x </mi>
            <mo> + </mo>
            <mi> y </mi>
            <mo> = </mo>
            <mn> 2 </mn>
          </mtd>
        </mtr>
        <mtr>
          <mtd>
            <mi> x </mi>
            <mo> - </mo>
            <mi> y </mi>
            <mo> = </mo>
            <mn> 1 </mn>
          </mtd>
        </mtr>
      </mtable>
    </math>"""
    intp = MathMLInterpreter()
    expr_instance = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr_group = expr_instance
    assert [str(e.expr) for e in sympy_expr_group] == scorrect