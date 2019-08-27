import pytest

import sympy
from sympy import symbols, Eq, Number

from analysis_classes import SympyAnalysis

def test_init_no_errors():
    x = symbols('x')
    expr = x + 2
    expr_analysis = SympyAnalysis(expr)

def test_equation_rewritten():
    x,y = symbols('x y')
    expr = x + y
    equ = Eq(expr, 2)
    equ_analysis = SympyAnalysis(equ)
    assert str(equ_analysis.expr) == 'x + y - 2', "Equation not rewritten into expression"

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
