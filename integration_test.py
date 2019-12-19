import pytest

from mathml import MathMLInterpreter
from expression_classes import SympyExpression
from analysis_classes import SympyAnalysis, SympyGroupAnalysis
from solver_classes import SympySolver

from sympy import FiniteSet

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

def test_sys_of_equation_solving():
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

    # Interpret and express in Sympy terms
    intp = MathMLInterpreter()
    expr_inst = intp.get_expression(s, Expr=SympyExpression)
    sympy_expr_group = expr_inst
    assert [str(e) for e in sympy_expr_group] == scorrect, "Group Expression Interpretation failed."

    # Analyze expression
    expr_group_analysis = SympyGroupAnalysis(sympy_expr_group)

    # Evaluate
    solver = SympySolver(sympy_expr_group)
    sol = solver.solve()
    print(sol)
    sol_correct_dict = {'x': 1.5, 'y': 0.5}
    sol_correct = FiniteSet(tuple(sol_correct_dict[str(s)] for s in solver.symbols()))
    sol_float = FiniteSet(*(tuple(float(n) for n in s) for s in sol))
    assert sol_float == sol_correct , "Linear solver failed"

    #raise NotImplementedError("This test hasn't been written yet.")