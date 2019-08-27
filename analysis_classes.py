
import sympy
from sympy import symbols

class SympyAnalysis:
    def __init__(self, expr):
        self.set_expr(expr)
        self.symbols = self.expr.free_symbols
        pass

    def set_expr(self, expr):
        # Set the expression to be analyzed
        if not isinstance(expr, tuple(sympy.core.all_classes)):
            raise ValueError(f"Given expression is not Sympy type but '{type(expr)}' type")
        
        if isinstance(expr, sympy.relational.Relational):
            self.expr = expr.rewrite(sympy.Add)
        else:
            self.expr = expr

    def is_partially_linear(self, syms=None):
        # Checks partial linearity of expression for given symbols
        if syms is None:
            syms = self.symbols

        if len(syms) == 0:
            raise ValueError("No symbols to check linearity against")

        linearity = {}
        for s in syms:
            linearity[s] = (sympy.diff(self.expr,s,s) == 0)

        return linearity

    def is_linear(self, syms=None, detailed=False):
        # Checks if expressions are fully linear
        if syms is None:
            syms = self.symbols

        if len(syms) == 0:
            raise ValueError("No symbols to check linearity against")

        linearity_dict = {}
        for s in syms:
            linearity_dict[s] = {}
            for t in syms:
                linearity_dict[s][t] = (sympy.diff(self.expr, s, t) == 0)

        if detailed:
            return linearity_dict
        else:
            return all(all(d.values()) for d in linearity_dict.values())

    def is_constant(self):
        # Checks if value is constant over all variables
        for s in self.symbols:
            if (sympy.diff(self.expr, s) != 0):
                return False
        return True




           