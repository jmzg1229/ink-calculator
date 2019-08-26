import logging
logger_exprclasses = logging.getLogger(__name__)
logger_exprclasses.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log_{}.txt'.format(__name__))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger_exprclasses.addHandler(file_handler)

logger_exprclasses.info('\n\nOpening expression_classes.py...')

from sympy import Number, Symbol, Add, Mul, Pow, Eq

class ExpressionWriter:
    # Generates an expression. Call methods in order of operations
    # and the expression will be generated as the calls go along.

    def __str__(self):
        raise NotImplementedError("String representation for placeholder ExpressionWriter template class")

    def set_expr(self, expr, *args, **kwargs):
        raise NotImplementedError

    def argcheck(self, *args, **kwargs):
        raise NotImplementedError

    def run_operation(self, op_name, *args, **kwargs):
        if op_name == 'addition':
            self.addition(*args, **kwargs)
        elif op_name == 'subtraction':
            self.subtraction(*args, **kwargs)
        elif op_name == 'multiplication':
            self.multiplication(*args, **kwargs)
        elif op_name == 'division':
            self.division(*args, **kwargs)
        elif op_name == 'power':
        	self.power(*args, **kwargs)
        else:
            raise NotImplementedError("Operation '{}' not implemented yet in ExpressionWriter".format(op_name))

    def number(self, *args, **kwargs):
        raise NotImplementedError

    def symbol(self, *args, **kwargs):
        raise NotImplementedError

    def constant(self, *args, **kwargs):
        raise NotImplementedError

    def variable(self, *args, **kwargs):
        raise NotImplementedError

    def equality(self, *args, **kwargs):
        raise NotImplementedError

    def addition(self, *args, **kwargs):
        raise NotImplementedError

    def subtraction(self, *args, **kwargs):
        raise NotImplementedError

    def multiplication(self, *args, **kwargs):
        raise NotImplementedError

    def division(self, *args, **kwargs):
        raise NotImplementedError

    def parenthesize(self, *args, **kwargs):
        raise NotImplementedError

    def equation(self, *args, **kwargs):
        raise NotImplementedError

class PythonExpression(ExpressionWriter):
    def __init__(self, *args, **kwargs):
        self.expr = ""

    def __str__(self):
        return 'PythonExpression("{}")'.format(self.expr)

    def set_expr(self, expr, *args, **kwargs):
        if not isinstance(expr, str):
            raise ValueError("Python expressions must be written in strings")

        self.expr = '({})'.format(expr)
        return self.expr

    # TODO: Once SympyExpression begins implementation, determine what part of this method
    #       can be moved up to a general ExpressionWriter method.
    def create_expression(self, op_symbol, *args, **kwargs):
        left_value = kwargs.get('left_value',  None)
        right_value= kwargs.get('right_value', None)
        append =     kwargs.get('append',      True)

        # Check sufficient operands are given
        if (right_value == None):
            raise ValueError("Right operand was not given.")
        elif (append == False) and (left_value == None):
            raise ValueError("Left operand not given for non-appending operation")
        elif (append == True) and (left_value != None):
            raise ValueError("Requested an append operation but gave a left operand anyway.")

        # Check if either operand is an expression in of itself
        if isinstance(left_value, PythonExpression):
            left_value = left_value.expr
        if isinstance(right_value, PythonExpression):
            right_value = right_value.expr

        # Overwrite expression
        if append:
            left_value = self.expr
        self.expr = str(left_value) + ' {} '.format(op_symbol) + str(right_value)
        return self.expr
            

    def number(self, *args, **kwargs):
        num = kwargs.get('num', None)
        if num is None:
            raise ValueError("'num' argument not given")
        elif type(num) not in (int, float):
            raise NotImplementedError("num of type '{}'".format(type(num)))
        elif self.expr != '':
            raise ValueError("Current expression not empty for inserting number")
        self.expr = str(num)

    def symbol(self, *args, **kwargs):
        sym = kwargs.get('sym', None)
        if sym is None:
            raise ValueError("'sym' argument not given.")
        self.expr = sym

    def addition(self, *args, **kwargs):
        return self.create_expression('+', *args, **kwargs)
        #self.expr += '+'

    def subtraction(self, *args, **kwargs):
        return self.create_expression('-', *args, **kwargs)
        #self.expr += '-'

    def multiplication(self, *args, **kwargs):
        return self.create_expression('*', *args, **kwargs)
        #self.expr += '*'

    def division(self, *args, **kwargs):
        return self.create_expression('/', *args, **kwargs)
        #self.expr += '/'

    def power(self, *args, **kwargs):
        return self.create_expression('**', *args, **kwargs)

    def parenthesize(self, *args, **kwargs):
        self.expr = '({})'.format(self.expr)
        return self.expr

    def equation(self, *args, **kwargs):
        # Single equals sign - Assignment/Equation
        return self.create_expression('=', *args, **kwargs)

class SympyExpression(ExpressionWriter):
    def __init__(self, *args, **kwargs):
        self.expr = None
        self.evaluate = kwargs.get('evaluate', False)

    def __str__(self):
        return 'SympyExpression("{}")'.format(self.expr)

    # TODO: Once SympyExpression begins implementation, determine what part of this method
    #       can be moved up to a general ExpressionWriter method.
    def argcheck(self, *args, **kwargs):
        left_value = kwargs.get('left_value',  None)
        right_value= kwargs.get('right_value', None)
        append =     kwargs.get('append',      True)

        # Check sufficient operands are given
        if (right_value == None):
            raise ValueError("Right operand was not given.")
        elif (append == False) and (left_value == None):
            raise ValueError("Left operand not given for non-appending operation")
        elif (append == True) and (left_value != None):
            raise ValueError("Requested an append operation but gave a left operand anyway.")

        # Check if either operand is an expression in of itself
        if isinstance(left_value, SympyExpression):
            left_value = left_value.expr
        if isinstance(right_value, SympyExpression):
            right_value = right_value.expr

        # Overwrite expression
        if append:
            left_value = self.expr
        
        kwargs.update(left_value=left_value, right_value=right_value, append=append)
        
        return (args, kwargs)
            

    def number(self, *args, **kwargs):
        num = kwargs.get('num', None)
        if num is None:
            raise ValueError("'num' argument not given")
        self.expr = Number(num)

    def symbol(self, *args, **kwargs):
        sym = kwargs.get('sym', None)
        if sym is None:
            raise ValueError("'sym' argument not given.")
        self.expr = Symbol(sym)

    def addition(self, *args, **kwargs):
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Add(left_value, right_value, evaluate=self.evaluate)
        return self.expr

    def subtraction(self, *args, **kwargs):
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Add(left_value, Mul(-1, right_value), evaluate=self.evaluate)
        return self.expr

    def multiplication(self, *args, **kwargs):
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Mul(left_value, right_value, evaluate=self.evaluate)
        return self.expr

    def division(self, *args, **kwargs):
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Mul(left_value, Pow(right_value, -1), evaluate=self.evaluate)
        return self.expr

    def power(self, *args, **kwargs):
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Pow(left_value, right_value, evaluate=self.evaluate)
        return self.expr

    def equation(self, *args, **kwargs):
        # Single equals sign - Assignment/Equation
        (args, kwargs) = self.argcheck(*args, **kwargs)
        left_value = kwargs.get('left_value')
        right_value = kwargs.get('right_value')
        self.expr = Eq(left_value, right_value)
        return self.expr