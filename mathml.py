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

class ExprNotReady(Exception):
    pass


class MathMLInterpreter:
    def __init__(self, Expr=None):
        self.Expr = None
        self.set_expr(Expr)
        pass

    def set_expr(self, Expr):
        if Expr == None:
            raise ValueError("Can't have NoneType as ExpressionWriter class")
        self.Expr = Expr

    def match_tag(self, elem):
        tag_fn_map = {
            'mn': self.mn,
            'mi': self.mi,
            'mo': self.mo,
            'mrow': self.mrow,
            'mfenced': self.mfenced,
            'mfrac': self.mfrac
            }
        if elem.tag not in tag_fn_map:
            raise ValueError("MathML tag '{}' not found in Interpreter database".format(tag))
        fn = tag_fn_map.get(elem.tag)
        return (elem.tag, fn)
    
    def get_expression(self, tree):
        # The big one. Gets an ExpressionWriter expression
        # from the lxml tree representation of the MathML
        pass
        
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

    def mo(self, elem):
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
        return self.Expr.operator(op_name)


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
