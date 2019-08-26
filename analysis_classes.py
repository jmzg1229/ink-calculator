
import sympy
from sympy import symbols

class SympyAnalysis:
    def __init__(self, expr):
        self.set_expr(expr)
        pass

    def set_expr(self, expr):
        if not isinstance(expr, tuple(sympy.core.all_classes)):
            raise ValueError(f"Given expression is not Sympy type but '{type(expr)}' type")
        self.expr = expr

    def symbols(self):
        return self.expr.free_symbols

    def is_equation(self):
        return type(self.expr) == sympy.Eq

    def is_separately_linear(self, syms=None):
        if syms is None:
            syms = self.symbols()

        linearity = {}
        for s in syms:
            linearity[s] = sympy.Eq(sympy.diff(self.expr,s,s), 0)
        raise NotImplementedError



           