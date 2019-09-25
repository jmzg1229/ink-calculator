
import sympy
from sympy import symbols

class SympyAnalysis:
    expr_rel_classes = {sympy.Eq: 'equality',
                        sympy.Ne: 'unequality',
                        sympy.Lt: 'less than',
                        sympy.Le: 'less equal',
                        sympy.Gt: 'greater than',
                        sympy.Ge: 'greater equal'}

    def __init__(self, expr):
        self.set_expr(expr)

    def set_expr(self, expr):
        # Set the expression to be analyzed
        if not isinstance(expr, tuple(sympy.core.all_classes)):
            raise ValueError(f"Given expression is not Sympy type but '{type(expr)}' type")
        
        self.rel_name = self.expr_rel_classes.get(type(expr), None)
        self.rel_type = type(expr) if self.rel_name != None else None

        if isinstance(expr, sympy.relational.Relational):
            if self.rel_type == None:
                raise NotImplementedError(f"Type '{type(expr)}' relational class")
            self.expr = expr.lhs - expr.rhs
        else:
            self.expr = expr

        self.symbols = self.expr.free_symbols


    def get_rel_expr(self):
        if self.rel_name is None:
            raise ValueError("No relation present in expression")
        else:
            return self.rel_type(self.expr, 0)

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

    def has_symbols(self):
        # Checks if expression has any unevaluated symbols
        return (len(self.symbols) > 0)

    def is_evaluable(self):
        return self.is_constant()

    def is_relational(self):
        return (self.rel_name is not None)

    property_funs = { 'has_symbols': has_symbols,
                      'is_constant': is_constant,
                      'is_evaluable':is_evaluable,
                      'is_linear':   is_linear,
                      'is_linear_detailed': lambda: is_linear(detailed=True),
                      'is_partially_linear': is_partially_linear,
                      'is_relational': is_relational}

    def get_properties(self, property_names):
        properties = {n: self.property_funs[n](self) for n in property_names}
        return properties


class SympyGroupAnalysis:
    def __init__(self, expr_group):
        self.set_expr_group(expr_group)

    def set_expr_group(self, expr_group):
        self.expr_group = expr_group
        self.num_expr = len(self.expr_group)
        if self.num_expr > 1:
            pass
        elif self.num_expr == 0:
            raise ValueError("No expressions given!")

        self.analysis_group = []
        self.symbols = set()
        for expr in expr_group:
            expr_analysis = SympyAnalysis(expr)
            expr_syms = expr_analysis.symbols

            self.analysis_group.append(expr_analysis)
            self.symbols.update(expr_syms)
        pass



           