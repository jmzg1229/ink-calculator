import pytest

import sympy
from sympy import symbols, Eq

from analysis_classes import SympyAnalysis

def test_init_no_errors():
    x = symbols('x')
    expr = x + 2
    expr_analysis = SympyAnalysis(expr)

def test_equation_identified():
    x,y = symbols('x y')
    expr = x + y
    equ = Eq(expr, 2)
    equ_analysis = SympyAnalysis(equ)
    expr_analysis= SympyAnalysis(expr)
    assert equ_analysis.is_equation(), "Equation object not recognized as an equation"
    assert (not expr_analysis.is_equation()), "Expression object misunderstood as equation"
