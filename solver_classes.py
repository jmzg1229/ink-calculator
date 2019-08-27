
import copy
import sympy
from sympy import symbols, Eq, solveset, solve, linsolve, nonlinsolve

from analysis_classes import SympyAnalysis

class SympySolver:
    # Seeks to solve the system of equations towards zero
    def __init__(self, expr_group):
        # expr_group being a container for the expressions to be solved
        self.set_expression_group(expr_group)
        pass

    def set_expression_group(self, expr_group):
        if len(expr_group) == 0:
            raise ValueError("No expressions were given.")

        self.analysis_group = []
        for i in range(len(expr_group)):
            expr = expr_group[i]
            self.analysis_group.append(SympyAnalysis(expr))

        self.expr_group = expr_group

    def symbols(self):
        syms = set()
        for expr in self.expr_group:
            syms.update(expr.free_symbols)
        return syms

    def set_domain(self, domain):
        pass

    def set_bounds(self, bounds):
        pass

    def subs(self, sym, val, *args, **kwargs):
        inplace = kwargs.get('inplace', False)

        expr_subs_group = []
        for i in range(len(self.expr_group)):
            expr = self.expr_group[i]
            expr_subs = expr.subs(sym, val, *args, **kwargs)
            expr_subs_group.append(expr_subs)
        if inplace:
            self.set_expression_group(expr_subs_group)
        return expr_subs_group

    def is_linear(self, syms=None):
        # Returns whether system is linear for ALL of the given symbols
        if syms is None:
            syms = self.symbols()
        return all(a.is_linear(syms) for a in self.analysis_group)

    def solve(self, syms=None, *args, **kwargs):
        if syms is None:
            syms = self.symbols()

        num_expr = len(self.expr_group)
        if num_expr == 1:
            return solveset(self.expr_group[0], syms, *args, **kwargs)

        linear = self.is_linear(syms)
        if linear:
            sol = linsolve(self.expr_group, syms)
            return sol
        else:
            raise NotImplementedError("Nonlinear solvers")
            sol = nonlinsolve(self.expr_group, syms)
            return sol
            

