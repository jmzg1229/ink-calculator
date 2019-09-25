import pytest

from mathml import MathMLInterpreter
from expression_classes import SympyExpression
from analysis_classes import SympyAnalysis
from solver_classes import SympySolver

def test_most_basic_evaluation():
    # Evaluate the most basic math expression of all
    s = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
      <mn> 2 </mn>
      <mo> + </mo>
      <mn> 2 </mn>
    </math>"""

    # Interpret and express in Sympy terms
    intp = MathMLInterpreter()
    expr_inst = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr = expr_inst.expr
    assert str(sympy_expr) == '2 + 2', "Sympy expression failed"

    # Analyze expression
    expr_analysis = SympyAnalysis(sympy_expr)
    assert expr_analysis.is_constant(), "Expression constancy detection failed"
    assert expr_analysis.is_evaluable(),"Expression evaluability detection failed"

    # Evaluate
    solver = SympySolver([sympy_expr])
    expr_eval = solver.evalf()
    assert expr_eval[0] == 4, "Evaluation did not succeed"
    pass