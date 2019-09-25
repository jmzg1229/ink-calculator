import logging
logger_solverclasses = logging.getLogger(__name__)
logger_solverclasses.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log_{}.txt'.format(__name__))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger_solverclasses.addHandler(file_handler)

import copy
import sympy
from sympy import symbols, Eq, solveset, solve, linsolve, nonlinsolve

from utils import print_str
from analysis_classes import SympyAnalysis, SympyGroupAnalysis

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

    def figure_out(self):

        # Symbols
        syms = self.symbols()
        num_syms = len(syms)
        has_syms = (num_syms > 0)

        # Expression group
        expr_group = self.expr_group
        num_expr = len(expr_group)
        has_expr = (num_expr > 0)

        # Check if has symbols
        expr_has_syms = tuple(len(e.free_symbols) > 0 for e in expr_group)
        num_expr_w_symbols = sum(expr_has_syms)
        num_expr_wo_symbols = num_expr - num_expr_w_symbols

        # Some analysis
        if not has_expr:
            raise ValueError("No expressions given. What am I supposed to 'figure out'???")
        only_evals = (not has_syms)


        # Iterate through expressions individually
        for i in range(num_expr):
            expr = expr_group[i]
            expr_analysis = self.analysis_group[i]

            # Evaluate if has no symbols
            if not expr_has_syms[i]:
                expr = expr.doit()

            # Evaluate if it's just an unrelational expression to be evaluated
            if expr_analysis.rel_type is None:
                expr = expr.doit()

            # Overwrite expression
            expr_group[i] = expr

        # Not done figuring this one out yet
        raise NotImplementedError("Will figure out later")

    def subs(self, sym, val, inplace=False, *args, **kwargs):

        expr_subs_group = []
        for i in range(len(self.expr_group)):
            expr = self.expr_group[i]
            expr_subs = expr.subs(sym, val, *args, **kwargs)
            expr_subs_group.append(expr_subs)
        if inplace:
            self.set_expression_group(expr_subs_group)
        return expr_subs_group

    def evalf(self, inplace=False, *args, **kwargs):

        expr_evalf_group = []
        for i in range(len(self.expr_group)):
            expr = self.expr_group[i]
            expr_evalf = expr.evalf(*args, **kwargs)
            expr_evalf_group.append(expr_evalf)
        if inplace:
            self.set_expression_group(expr_evalf_group)
        return expr_evalf_group

    def solve(self, syms=None, *args, **kwargs):
        # TODO: What happens if an irrelevant expression is given?
        if syms is None:
            syms = self.symbols()

        if len(syms) == 0:
            logger_solverclasses.debug("Symbolless expression")
            raise ValueError("No symbols to solve for")

        num_expr = len(self.expr_group)
        if num_expr == 1:
            logger_solverclasses.debug("Only 1 expression given")
            return solveset(self.expr_group[0], syms, *args, **kwargs)

        linear = self.is_linear(syms)
        if linear:
            logger_solverclasses.debug("Linear Expressions")
            sol = linsolve(self.expr_group, syms)
            return sol
        else:
            logger_solverclasses.debug("Nonlinear Expressions")
            logger_solverclasses.debug(print_str('Symbols:', syms))
            logger_solverclasses.debug(print_str('Expressions:', self.expr_group))
            sol = nonlinsolve(self.expr_group, list(syms))
            logger_solverclasses.debug(print_str('Solution:', sol))
            return sol
            

