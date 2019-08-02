### TODO: Look out for logger variable overriding when using logging across mutliple files/modules
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log_{}.txt'.format(__name__))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info('\nOpening mathml.py...')

def print_str(*args, sep=' '):
    return sep.join(str(a) for a in args)

#@doctest_depends_on(modules=('lxml','StringIO','os',))
def openmath2cmml(omstring,simple=False):
    """
    Transforms a string in Openmath to Content MathML (simple or not)
    XSL Templates from https://svn.omdoc.org/repos/omdoc/projects/emacsmode/nomdoc-mode/xsl/ although they are
    """
    
    from lxml import etree
    from lxml import objectify
    #from io.StringIO import * # will comment out until figure out what it imports
    import os
    
    if simple:
        xslt_tree = etree.XML(open(os.path.join(request.folder,'mathml/data/omtosimcmml.xsl')).read())
    else:
        xslt_tree = etree.XML(open(os.path.join(request.folder,'mathml/data/omtocmml.xsl')).read())
    
    transform = etree.XSLT(xslt_tree)
    omstring= omstring.replace(' xmlns="', ' xmlnamespace="')
    parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
    tree   = etree.parse(StringIO(omstring), parser)
    objectify.deannotate(tree,cleanup_namespaces=True,xsi=True,xsi_nil=True)
    cmmlstring_tree=transform(tree)
    cmmlstring=etree.tostring(cmmlstring_tree.getroot())
    return(cmmlstring)


class ExpressionWriter:
    # Generates an expression. Call methods in order of operations
    # and the expression will be generated as the calls go along.

    def set_expr(self, expr, *args, **kwargs):
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
        else:
            raise NotImplementedError("Operation '{}' not implemented yet in ExpressionWriter".format(op_name))

    def number(self, *args, **kwargs):
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

class PythonExpression(ExpressionWriter):
    def __init__(self, *args, **kwargs):
        self.expr = ""

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
        self.expr += str(num)

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

    def parenthesize(self, *args, **kwargs):
        self.expr = '({})'.format(self.expr)
        return self.expr


# TODO: Figure out how to communicate to ExpressionWriter what
#       is a 'symbol', operation, and number without stepping over Sympy
#       (specifically with the definition of a symbol)

class MathMLInterpreter:
    def __init__(self):
        pass

    def match_tag(self, elem):
        # Function mapping is probably defunct because we can't
        # process whole operations on a tag-by-tag basis.
        # Will consider removing this function soon
        # Might need it back at some point, but will write big
        # if statement before that happens
        tag_fn_map = {
            'mn': self.mn,
            'mi': self.mi,
            'mo': self.get_op_name,
            'mrow': self.mrow,
            'mfenced': self.mfenced,
            'mfrac': self.mfrac
            }
        if elem.tag not in tag_fn_map:
            raise ValueError("MathML tag '{}' not found in Interpreter database".format(tag))
        fn = tag_fn_map.get(elem.tag)
        return (elem.tag, fn)
    
    def get_tree(self, s):
        # Get MathML tree from string
        from lxml import etree
        from io import StringIO, BytesIO # Will add necessary functions individually
        from lxml import objectify
        if 'xmlns=' in s:
            s = s.replace("xmlns=", "xmlnamespace=")
        parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
        tree   = etree.parse(StringIO(s), parser)
        return tree

    def get_elem_tree_string(self, elem):
        from lxml import etree
        tree_string = etree.tostring(elem).decode("utf-8")
        return tree_string
        
    def get_expression(self, s, Expr):
        # The big one. Gets an ExpressionWriter expression
        # from the string representation of the MathML
        from lxml import etree
        tree = self.get_tree(s)
        head_tag = tree.getroot().tag
        logger.debug(print_str("Head tag:", head_tag))

        # Check for a valid given ExpressionWriter instance
        if not issubclass(Expr, ExpressionWriter):
            raise TypeError("Passed expression instance is not an 'ExpressionWriter' class")
        Expr_instance = Expr()

        tags = []
        fns = []
        elems = []
        texts = []
        for elem in tree.getroot():
            elem.text = elem.text.strip().rstrip()
            t,f = self.match_tag(elem)
            tags.append(t)
            fns.append(f)
            elems.append(elem)
            texts.append(elem.text)
            #print(t)
        logger.debug(print_str(tags))


        ### Check if valid expression or just character typing
        # Check no trailing operators
        if (tags[0] == 'mo') or (tags[-1] == 'mo'):
            raise NotImplementedError("Raw character writing that's an unvalid expression")

        # Skip invalid expressions
        ## Assuming only valid expressions below

        # Index 'mo' operator tags
        mo_idx = [i for (i,x) in enumerate(tags) if x == 'mo']
        mo_text = [texts[i] for i in mo_idx]
        num_ops = len(mo_idx)

        # Stop if any equality operands. Not implemented yet
        # how to process multiple expressions at once
        num_equalities = len([i for (i,x) in enumerate(mo_text) if x == '='])
        if num_equalities > 1:
            raise NotImplementedError("Multiple equalities/equations in one line statement")
        elif num_equalities == 1:
            raise NotImplementedError("Equality and separation of expressions")


        # Check if zero operators found (e.g. only an mrow inside an mfenced)
        if num_ops == 0:
            if (head_tag == 'mfenced') or (head_tag == 'mrow'):
                logger.debug("Zero ops - {} tag".format(head_tag))
                if not len(elems) == 1:
                    raise ValueError("Need only 1 element but got {} instead".format(len(elems)))
                elem = elems[0]
                elem_tree_string = self.get_elem_tree_string(elem)
                nest_exp = self.get_expression(elem_tree_string, Expr=Expr)
                return nest_exp                
            else:
                raise ValueError("No operators found inside '{}' element".format(head_tag))


        # TODO: Check for overlapping operands and decide how to manage
        # those expression mergers.
        logger.debug(print_str("mo_text:", mo_text))
        # Check if operators have operands
        for midx in range(len(mo_idx)):
            # Get operator text
            i = mo_idx[midx]
            op_elem = elems[i]
            op_text = op_elem.text
            op_name = self.get_op_name(op_elem)
            logger.debug(print_str("Operation:", op_name))

            # Get operand tags and texts
            (right_tag,right_text) = (tags[i+1], elems[i+1].text)

            # Something other than a number as operand
            if (right_tag == 'mrow') or (right_tag == 'mfenced'):
                right_tree_string = self.get_elem_tree_string(elems[i+1])
                right_value = self.get_expression(right_tree_string, Expr=Expr)                
            elif (right_tag == 'mn'):
                # Check if number is int or float
                right_dtype = float if '.' in right_text else int
                # Cast value to number
                right_value = right_dtype(right_text)
            else:
                raise NotImplementedError("'{}' tag as right operand".format(right_tag))

            logger.debug(print_str("midx =", midx))
            if midx == 0:
                # Disable expression append
                append = False

                # Get left operand tags and texts too
                (left_tag, left_text) = (tags[i-1], elems[i-1].text)

                # Something other than a number as operand
                if (left_tag == 'mrow') or (left_tag == 'mfenced'):
                    left_tree_string = self.get_elem_tree_string(elems[i-1])
                    logger.info("Calling left tree expression recursion...")
                    left_value = self.get_expression(left_tree_string, Expr=Expr)
                    logger.info("Finished left tree recursion.")
                    logger.debug(print_str('left_value:', left_value))
                    #raise NotImplementedError("Paranthesizing for left operand expression")
                elif (left_tag != 'mn'):
                    raise NotImplementedError("Non-number ('{}' tag) as left operand".format(left_tag))
                elif (left_tag == 'mn'):
                    # Check if number is int or float
                    left_dtype = float if '.' in left_text else int

                    # Cast value to number
                    left_value = left_dtype(left_text)
                    logger.debug(print_str((left_value, op_text, right_value)))

                # Set operation arguments
                op_kwargs = {'append':append, 'left_value': left_value, 'right_value': right_value}
            else:
                # Enable expression append
                append = True

                # Set operation arguments
                op_kwargs = {'append':append, 'right_value': right_value}

            # Run operation
            logger.debug(print_str(op_name, op_kwargs))
            Expr_instance.run_operation(op_name, **op_kwargs)

            # Print current calculated expression
            logger.debug(print_str("Current expression:", Expr_instance.expr))

        if (head_tag == 'mrow') or (head_tag == 'mfenced'):
            Expr_instance.parenthesize()

        print("Final expression: '{}'".format(Expr_instance.expr))
        logger.debug("Final expression: '{}'".format(Expr_instance.expr))
        return Expr_instance
        



    def mn(self, elem):
        # TODO: Check with symbols such as PI
        return self.Expr.number(elem.text)

    def mi(self, elem):
        return self.Expr.variable(elem.text)

    def mrow(self, elem):
        # Recursion required
        return self.Expr.group()

    def mfenced(self, elem):
        # Recursion required
        return self.Expr.parenthesis()
        pass

    def mfrac(self, elem):
        # Recursion required
        children = elem.getchildren()
        assert len(children) == 2
        pass

    def get_op_name(self, elem):
        op_map = {
            '=': 'equality',
            '+': 'addition',
            '-': 'subtraction',
            '*': 'multiplication',
            '/': 'division'
        }
        op_symbol = elem.text
        if op_symbol not in op_map:
            raise ValueError("Operator '{}' not found in Interpreter database.".format(op_symbol))
        op_name = op_map.get(op_symbol)
        return op_name


#@doctest_depends_on(modules=('lxml','StringIO',))    
def parseCMML(mmlinput):
    """
    This parses Content MathML into a Python expression and a set of variables which can be sympified afterwards. At the moment, only basic operators are taking into account.
    It returns the expression and the set of variables inside it
    """
    from lxml import etree
    from io import StringIO, BytesIO # Will add necessary functions individually
    from lxml import objectify
    if 'xmlns=' in mmlinput:
        mmlinput= mmlinput.replace("xmlns=", "xmlnamespace=")
    parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
    tree   = etree.parse(StringIO(mmlinput), parser)
    tree_string = etree.tostring(tree, pretty_print=True).decode("utf-8")
    #print(tree)
    print("Tree:", tree_string, sep='\n')
    objectify.deannotate(tree,cleanup_namespaces=True,xsi=True,xsi_nil=True)
    #print([(t.tag,t.text) for t in tree.getroot()])
    mmlinput=etree.tostring(tree.getroot())
    #print(mmlinput.decode("utf-8"))
    exppy="" #this is the python expression
    symvars=[]  #these are symbolic variables which can eventually take part in the expression
    #events = ("start", "end")
    #level = 0
    #context = etree.iterparse(BytesIO(mmlinput),events=events)
    #print(context)
    #print("Starting tree loop:")
    for elem in tree.getroot():

        # Clean-up input element text
        if elem.text is not None:
            elem.text = elem.text.strip().rstrip()
        print(elem.tag)

        # If has children, get expressions from children
        children = elem.getchildren()
        child_exps = []
        for c in children:
            cexp = parseCMML(etree.tostring(c).decode("utf-8"))
            child_exps.append(cexp)
        #print("Child expressions:")
        #print(child_exps)

        # Synthesize expression from this element, and
        # Add to running expression tally
        if elem.tag == 'mn':
            exppy += elem.text
        elif elem.tag == 'mfrac':
            assert len(child_exps) == 2
            (num, den) = child_exps
            print("num,dem", num, den)
            exppy += "({num})/({den})".format(num=num,den=den)
        elif (elem.tag == 'mfenced'):
            exppy += "(" + ''.join(child_exps) + ")"
        elif (elem.tag == 'mrow'):
            # Not quite being detected yet. Look at how it processes children vs root of new tree
            exppy += "(" + ''.join(child_exps) + ")"
        elif elem.tag == 'mo':
            if elem.text == '=':
                exppy += '='
            elif elem.text == '+':
                exppy += '+'
            elif elem.text == '-':
                exppy += '-'
            elif elem.text == '*':
                exppy += '*'

        
    return exppy
