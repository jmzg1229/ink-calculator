
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
        self.num_expr = 0
        self.analysis_group = []
        self.symbols = set()
        self.set_expr_group(expr_group)

    def set_expr_group(self, expr_group):
        num_expr = len(expr_group)
        if num_expr == 0:
            raise ValueError("No expressions given!")

        self.num_expr = 0
        self.expr_group = []
        self.analysis_group = []
        self.symbols = set()
        for i in range(num_expr):
            expr = expr_group[i]
            self.add_expr(expr)
        pass

    def update_symbols(self):
        self.symbols = set()
        for i in range(self.num_expr):
            expr_syms = self.analysis_group[i].symbols
            self.symbols.update(expr_syms)

    def add_expr(self, expr):
        self.expr_group.append(expr)
        self.set_expr(self.num_expr, expr)

    def set_expr(self, idx, expr):
        if (idx > self.num_expr) or (idx < -self.num_expr):
            raise ValueError("Index out of bounds")

        expr_analysis = SympyAnalysis(expr)
        expr_syms = expr_analysis.symbols

        if (idx == self.num_expr):
            # Add a new expression
            self.num_expr += 1
            self.analysis_group.append(expr_analysis)
            self.symbols.update(expr_syms)
        else:
            self.analysis_group[idx] = expr_analysis
            self.update_symbols()

    def is_linear(self, syms=None):
        # Returns whether system is linear for ALL of the given symbols
        if syms is None:
            syms = self.symbols
        return all(a.is_linear(syms) for a in self.analysis_group)

    def is_solvable(self):
        # Checks if system can be figured out
        expr_idx = list(range(self.num_expr))

        # Evaluable parts
        eval_idx = []
        for i in expr_idx:
            if self.analysis_group[i].is_evaluable():
                eval_idx.append(i)
        expr_idx = [e for e in expr_idx if e not in eval_idx]

        # Rest of unknowns
        solvable = (len(expr_idx) == 0)
        return (solvable, {'evaluable': eval_idx}, expr_idx)




           