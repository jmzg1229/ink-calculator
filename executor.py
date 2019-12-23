
import argparse

from mathml import MathMLInterpreter
from expression_classes import SympyExpression
from analysis_classes import SympyAnalysis, SympyGroupAnalysis
from solver_classes import SympySolver

## TODO: Implement instructions parsing
## TODO: Make sure expressions and groups are processed the same way

## Parse command line input
parser = argparse.ArgumentParser()

parser.add_argument('mathml', help="MathML string containing written-down math")

args = parser.parse_args()

## Decide what tasks must be done

## Do the tasks
s = args.mathml

# Interpret and express in Sympy terms
intp = MathMLInterpreter()
expr_inst = intp.get_expression(s, Expr=SympyExpression)
sympy_expr = expr_inst.expr

# Analyze expression
expr_analysis = SympyAnalysis(sympy_expr)

# Evaluate
solver = SympySolver([sympy_expr])
expr_eval = solver.evalf()

print(expr_eval)