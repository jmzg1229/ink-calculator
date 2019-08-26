### TODO: Look out for logger_mathml variable overriding when using logging across mutliple files/modules
import logging
logger_mathml = logging.getLogger(__name__)
logger_mathml.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log_{}.txt'.format(__name__))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger_mathml.addHandler(file_handler)

logger_mathml.info('\n\nOpening mathml.py...')

import copy

from utils import print_str
from expression_classes import ExpressionWriter

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
            'mfrac': self.mfrac,
            'msup': self.msup,
            'msub': self.msub
            }
        if elem.tag not in tag_fn_map:
            raise ValueError("MathML tag '{}' not found in Interpreter database".format(elem.tag))
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
        """ The big one. Gets an ExpressionWriter expression
        # from the string representation of the MathML """
        from lxml import etree
        logger_mathml.info("Calling get_expression()")

        # Read input string or element
        if isinstance(s, etree._Element):
            logger_mathml.debug("Passed in an element")
            s = self.get_elem_tree_string(s)
        elif type(s) != str:
            raise TypeError("Expected in str or etree._Element for s, but got {} instead.".format(type(s)))
        else:
            logger_mathml.debug("Passed in a string")

        # TOFIX: Converting element to tree to reconvert back into elements
        # Get lxml tree
        tree = self.get_tree(s)
        root_elem = tree.getroot()
        head_tag = root_elem.tag

        logger_mathml.debug(print_str("Head tag:", head_tag))
            

        # Check for a valid given ExpressionWriter instance
        if not issubclass(Expr, ExpressionWriter):
            raise TypeError("Passed expression instance is not an 'ExpressionWriter' class")
        Expr_instance = Expr()

        # Setup/data loop
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
        logger_mathml.debug(print_str("tags:", tags))


        # No co-level tags (e.g. a singular 'mn' element)
        ## TOFIX: Outsource 'mn' number identification into a different method
        if (len(tags) == 0):
            logger_mathml.debug("No tags co-level - {} head".format(head_tag))
            if (head_tag == 'mn'):
                return self.mn(tree.getroot(), Expr=Expr)
                raise NotImplementedError("No co-level tags for 'mn' head")
            elif (head_tag == 'mi'):
                return self.mi(tree.getroot(), Expr=Expr)
            else:
                raise NotImplementedError("No co-level tags for '{}' head".format(head_tag))

        ### Check if valid expression or just character typing
        # Check no trailing operators
        if (tags[0] == 'mo') or (tags[-1] == 'mo'):
            raise NotImplementedError("Raw character writing that's an unvalid expression")
        ######################################################
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
            left_tree = copy.deepcopy(root_elem)
            right_tree= copy.deepcopy(root_elem)
            before_equal = True
            for (cl,cr) in zip(left_tree,right_tree):
                if cl.text == '=':
                    before_equal = False
                    left_tree.remove(cl)
                    right_tree.remove(cr)
                elif before_equal:
                    right_tree.remove(cr)
                elif not before_equal:
                    left_tree.remove(cl)
            left_expr = self.get_expression(left_tree, Expr)
            right_expr= self.get_expression(right_tree,Expr)
            Expr_instance.equation(append=False, left_value=left_expr, right_value=right_expr)
            return Expr_instance
            raise NotImplementedError("Equality and separation of expressions")


        # Check if zero operators found (e.g. only an mrow inside an mfenced)
        if num_ops == 0:
            logger_mathml.debug("Zero ops - {} tag".format(head_tag))
            
            # Container heads
            if (head_tag == 'mfenced') or (head_tag == 'mrow') or (head_tag == 'math'):                
                if not len(elems) == 1:
                    raise ValueError("Need only 1 element but got {} instead".format(len(elems)))
                elem = elems[0]
                elem_tree_string = self.get_elem_tree_string(elem)
                return self.get_expression(elem, Expr=Expr)  
            
            # Fraction head
            elif (head_tag == 'mfrac'):
                ### TODO: Work on fraction element
                if not len(elems) == 2:
                    raise ValueError("Need only 2 elements for fraction but got {}".format(len(elems)))
                
                # Get fraction numerator and denominators
                (top_elem, bot_elem) = elems
                top_expr = self.get_expression(top_elem, Expr=Expr)
                bot_expr = self.get_expression(bot_elem, Expr=Expr)
                logger_mathml.debug(print_str("top_expr:", top_expr))
                logger_mathml.debug(print_str("bot_expr:", bot_expr))

                # Run fraction (division) operation
                frac_kwargs = {'append': False, 'left_value': top_expr, 'right_value': bot_expr}
                Expr_instance.run_operation('division', **frac_kwargs)
                return Expr_instance
                raise NotImplementedError("'mfrac' operator")
            
            # Power/Exponent head
            elif (head_tag == 'msup'):
                if not len(elems) == 2:
                    raise ValueError("Need only 2 elements for power but got {}".format(len(elems)))
                
                # Get base and power (e.g. exponent)
                (base_elem, power_elem) = elems
                base_expr = self.get_expression(base_elem, Expr=Expr)
                power_expr = self.get_expression(power_elem, Expr=Expr)
                logger_mathml.debug(print_str("base_expr:", base_expr))
                logger_mathml.debug(print_str("power_expr:", power_expr))

                # Run power operation
                power_kwargs = {'append': False, 'left_value': base_expr, 'right_value': power_expr}
                Expr_instance.run_operation('power', **power_kwargs)

            # Subscript head
            elif (head_tag == 'msub'):
                if not len(elems) == 2:
                    raise ValueError("Need only 2 elements for subscript but got {}".format(len(elems)))

                # Get base and subscript expressions
                (base_elem, sub_elem) = elems
                base_expr = self.get_expression(base_elem, Expr=Expr)
                sub_expr = self.get_expression(sub_elem, Expr=Expr)
                logger_mathml.debug(print_str("base_expr:", base_expr))
                logger_mathml.debug(print_str("sub_expr:", sub_expr))

                base_text = str(base_expr.expr)
                sub_text  = str(sub_expr.expr)

                sym_name = '{0}_{{{1}}}'.format(base_text, sub_text)

                # Run symbol creation
                Expr_instance.symbol(sym=sym_name)
                return Expr_instance

                raise NotImplementedError("'msub' operator")
            
            # Any other heads
            else:
                raise ValueError("No operators found inside '{}' element".format(head_tag))

        logger_mathml.debug(print_str("mo_text:", mo_text))

        # Iterate through expression's operations         
        for midx in range(len(mo_idx)):
            # Get operator text
            i = mo_idx[midx]
            op_elem = elems[i]
            op_name = self.get_op_name(op_elem)
            logger_mathml.debug(print_str("Operation:", op_name))

            # Get right operand expression
            right_elem = elems[i+1]
            right_value = self.get_expression(right_elem, Expr)            

            logger_mathml.debug(print_str("midx =", midx))

            # Start of expression
            if midx == 0:
                # Disable expression append
                append = False

                # Get left operand expression
                left_elem = elems[i-1]
                left_value = self.get_expression(left_elem, Expr)
                logger_mathml.debug(print_str('left_value:', left_value))

            # Ongoing expression                                   
            else:
                # Enable expression append
                append = True
                left_value = None
                

            # Set operation arguments
            op_kwargs = {'append':append, 'left_value': left_value, 'right_value': right_value}

            # Run operation
            logger_mathml.debug(print_str("Pre-op expression:", Expr_instance.expr))
            logger_mathml.debug(print_str(op_name, op_kwargs))
            logger_mathml.debug(print_str('left_value:', left_value))
            logger_mathml.debug(print_str('right_value:', right_value))
            Expr_instance.run_operation(op_name, **op_kwargs)

            # Print/log current calculated expression
            logger_mathml.debug(print_str("Current expression:", Expr_instance.expr))

        # Parenthesize expression to preserve order of operations. Done at end to prevent extra parenthesis.
        if (head_tag == 'mrow') or (head_tag == 'mfenced'):
            Expr_instance.parenthesize()

        # Return expression
        logger_mathml.debug("Final expression: '{}'".format(Expr_instance.expr))
        return Expr_instance
        



    def mn(self, elem, Expr):
        # TODO: Check with symbols such as PI
        # TOFIX: Add a robust check to see if string actually matches a number

        # Check if number is int or float
        operand_dtype = float if '.' in elem.text else int

        # Cast value to number
        operand_value = operand_dtype(elem.text)
        operand_expr = Expr()

        # Cast value to expression
        operand_expr.number(num=operand_value)

        return operand_expr

    def mi(self, elem, Expr):
        symbol_expr = Expr()
        symbol_expr.symbol(sym=elem.text)
        return symbol_expr

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


    def msup(self, elem):
        raise NotImplementedError

    def msub(self, elem):
        raise NotImplementedError

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
