import pytest

import sympy
from sympy import symbols, Eq, Number, FiniteSet

from analysis_classes import SympyAnalysis
from solver_classes import SympySolver

def test_init_runs():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)

def test_symbols_found():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)
    assert esolver.symbols() == set((x,y,z)), "Symbols not found."

def test_subs():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)
    egroup_subs = esolver.subs(x, 2)
    assert egroup_subs == [4, y+z, z-2], "Distributed substitution didn't work"

def test_subs_inplace():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)
    esolver.subs(x, 2, inplace=True)
    assert esolver.expr_group == [4, y+z, z-2], "Distributed inplace substitution didn't work"

def test_linear_system_detection():
    x,y,z = symbols('x, y, z')
    e1 = x + 2
    e2 = y + z
    e3 = z - x
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)
    assert esolver.is_linear(), "Linearity of system not detected"

def test_nonlinear_system_detection():
    x,y = symbols('x, y')
    e1 = x*y - 1
    e2 = 4*x**2 + y**2 - 5
    egroup = [e1, e2]
    esolver = SympySolver(egroup)
    assert not esolver.is_linear(), "Nonlinearity of system not detected"

def test_linear_solver():
    x,y,z = symbols('x, y, z')
    e1 = x + 2 - 3
    e2 = y + z - 5
    e3 = z - x - 2
    egroup = [e1, e2, e3]
    esolver = SympySolver(egroup)
    sol = esolver.solve()
    sol_correct_dict = {x: 1, y: 2, z: 3}
    sol_correct = FiniteSet(tuple(sol_correct_dict[s] for s in esolver.symbols()))
    assert sol == sol_correct , "Linear solver failed"

def test_nonlinear_solver():
    x,y = symbols('x, y')
    e1 = x*y - 1
    e2 = 4*x**2 + y**2 - 5
    egroup = [e1, e2]
    esolver = SympySolver(egroup)
    sol = esolver.solve()
    sol_correct_dict = {x: (-1,-1/2,1/2,1), y: (-1,-2,2,1)}
    sol_correct_tuple= tuple(sol_correct_dict[s] for s in esolver.symbols())
    sol_correct = FiniteSet(tuple(t for t in zip(*sol_correct_tuple)))
    assert sol == sol_correct , "Nonlinear solver failed"