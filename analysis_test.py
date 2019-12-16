import pytest

import sympy
from sympy import symbols, Number, Eq

from analysis_classes import SympyAnalysis, SympyGroupAnalysis

def test_init_no_errors():
    x = symbols('x')
    expr = x + 2
    expr_analysis = SympyAnalysis(expr)

def test_relational_detection():
    from sympy import Eq, Ne, Lt, Le, Gt, Ge
    x,y = symbols('x y')
    expr = x + y
    assert SympyAnalysis(expr).rel_name == None
    assert SympyAnalysis(Eq(expr)).rel_name == 'equality'
    assert SympyAnalysis(Ne(expr, 0)).rel_name == 'unequality'
    assert SympyAnalysis(Lt(expr, 0)).rel_name == 'less than'
    assert SympyAnalysis(Le(expr, 0)).rel_name == 'less equal'
    assert SympyAnalysis(Gt(expr, 0)).rel_name == 'greater than'
    assert SympyAnalysis(Ge(expr, 0)).rel_name == 'greater equal'

    assert SympyAnalysis(expr).rel_type == None
    assert SympyAnalysis(Eq(expr)).rel_type == Eq
    assert SympyAnalysis(Ne(expr, 0)).rel_type == Ne
    assert SympyAnalysis(Lt(expr, 0)).rel_type == Lt
    assert SympyAnalysis(Le(expr, 0)).rel_type == Le
    assert SympyAnalysis(Gt(expr, 0)).rel_type == Gt
    assert SympyAnalysis(Ge(expr, 0)).rel_type == Ge

def test_relational_return():
    from sympy import Eq, Ne, Lt, Le, Gt, Ge
    x,y = symbols('x y')
    expr = x + y
    with pytest.raises(Exception):
        SympyAnalysis(expr).get_rel_expr()
    assert SympyAnalysis(Eq(expr)).get_rel_expr() == Eq(expr)
    assert SympyAnalysis(Ne(expr, 0)).get_rel_expr() == Ne(expr, 0)
    assert SympyAnalysis(Lt(expr, 0)).get_rel_expr() == Lt(expr, 0)
    assert SympyAnalysis(Le(expr, 0)).get_rel_expr() == Le(expr, 0)
    assert SympyAnalysis(Gt(expr, 0)).get_rel_expr() == Gt(expr, 0)
    assert SympyAnalysis(Ge(expr, 0)).get_rel_expr() == Ge(expr, 0)

def test_equation_rewritten():
    x,y = symbols('x y')
    expr = x + y
    equ = Eq(expr, 2)
    equ_analysis = SympyAnalysis(equ)
    assert equ_analysis.rel_name == 'equality', "Equality relation not detected"
    assert str(equ_analysis.expr) == 'x + y - 2', "Equation not rewritten into expression"

def test_inequality_rewritten():
    from sympy import Lt
    x,y = symbols('x y')
    expr = x + y
    equ = Lt(expr, 2)
    equ_analysis = SympyAnalysis(equ)
    assert equ_analysis.rel_name == 'less than', "'less than' relation not detected"
    assert str(equ_analysis.expr) == 'x + y - 2', "Relation not rewritten into expression"

def test_linearity_calculation():
    x,y = symbols('x y')
    expr = x + y**2
    expr_analysis = SympyAnalysis(expr)
    linearity_results = expr_analysis.is_linear()
    linearity_correct = False
    assert linearity_results == linearity_correct, "Linearity not calculated correctly"

def test_linearity_detailed_calculation():
    x,y = symbols('x y')
    expr = x + y**2
    expr_analysis = SympyAnalysis(expr)
    linearity_results = expr_analysis.is_linear(detailed=True)
    linearity_correct = {x: {x: True, y: True}, y: {x: True, y: False}}
    assert linearity_results == linearity_correct, "Linearity not calculated correctly"

def test_linearity_partial_calculation():
    x,y = symbols('x y')
    expr = x + y**2
    expr_analysis = SympyAnalysis(expr)
    linearity_results = expr_analysis.is_partially_linear()
    linearity_correct = {x: True, y: False}
    assert linearity_results == linearity_correct, "Linearity not calculated correctly"

def test_constant_calculation():
    x,y = symbols('x y')
    expr = x + y**2
    expr2 = Number(1)
    expr_analysis = SympyAnalysis(expr)
    expr2_analysis = SympyAnalysis(expr2)
    expr_constant_result = expr_analysis.is_constant()
    expr2_constant_result =expr2_analysis.is_constant()
    expr_constant_correct = False
    expr2_constant_correct = True
    assert expr_constant_result == expr_constant_correct, "Constancy not calculated correctly"
    assert expr2_constant_result== expr2_constant_correct,"Constancy not detected"

def test_get_properties():
    x = symbols('x')
    expr = x + 2
    expr_analysis = SympyAnalysis(expr)
    properties = expr_analysis.get_properties(['is_constant'])
    assert properties['is_constant'] is False, "Constancy not received."

def test_group_analysis_init():
    x,y = symbols('x y')
    expr = x + y
    equ = Eq(expr, 2)
    expr_group = [equ]
    group_analysis = SympyGroupAnalysis(expr_group)
    assert(group_analysis.symbols == set([x, y]))
    assert(group_analysis.num_expr == 1)
    assert(len(group_analysis.expr_group) == 1)

def test_group_nonrepeating_symbols():
    x,y = symbols('x y')
    expr = x + y
    equ = Eq(expr, 2)
    equ2 = Eq(x - y, 3)
    expr_group = [equ, equ2]
    group_analysis = SympyGroupAnalysis(expr_group)
    assert(group_analysis.symbols == set([x, y]))

def test_linear_system_detection():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    eanalysis = SympyGroupAnalysis(egroup)
    assert eanalysis.is_linear(), "Linearity of system not detected"

def test_nonlinear_system_detection():
    x,y = symbols('x, y')
    e1 = x*y - 1
    e2 = 4*x**2 + y**2 - 5
    egroup = [e1, e2]
    eanalysis = SympyGroupAnalysis(egroup)
    assert not eanalysis.is_linear(), "Nonlinearity of system not detected"

def test_basic_solvability_detection():
    from sympy import Add, Mul, Pow
    e1 = Add(2, 2, evaluate=False)
    e2 = Mul(2, 3, evaluate=False)
    e3 = Pow(2, 4, evaluate=False)
    egroup = [e1, e2, e3]
    eanalysis = SympyGroupAnalysis(egroup)
    assert eanalysis.num_expr == 3, "Wrong number of expressions"
    (solvable, sol_type_idx, unsolvable_idx) = eanalysis.is_solvable()
    assert solvable, "solvability not detected"
    assert sol_type_idx == {'evaluable': [0,1,2]}, "Solvability types not calculated correctly"
    assert unsolvable_idx == [], "Unsolvable indexes not filtered out"