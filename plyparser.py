import ply.yacc as yacc
from plylexer import tokens, literals
import plylexer
import sys

class Node:
    def __init__(self,type,children=None,parent=None,ptype=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        if parent:
            self.parent = parent
        else:
            self.parent = None
        if ptype:
            self.ptype = ptype
        else:
            self.ptype = None

def setParentOfChildren(node):
    for child in node.children:
        child.parent = node

def boolToTree(input):

    stack = []
    output = []
    while(len(input) > 0):
        e = input.pop(0)
        if(e == "("):
            stack.append(e)
        elif(e == ")"):
            while(len(stack) > 0 and stack[len(stack)-1] != "("):
                output.append(stack.pop())
            if(stack[len(stack)-1] == "("):
                stack.pop()
            else:
                sys.exit("Error 2")
        elif(e in ["and", "or"]):
            if(len(stack) > 0 and stack[len(stack)-1] in ["and", "or"]):
                output.append(stack.pop())
            stack.append(e)
        else:
            output.append(e)
    while(len(stack) > 0):
        output.append(stack.pop())

    stack = []
    input = output

    while(len(input) > 0):
        e = input.pop(0)
        if(isinstance(e, Node)):
            stack.append(e)
        elif(e == '('):
            sys.exit("Error 2")
        elif(e in ["and", "or"]):
            if(len(stack) < 2):
                sys.exit("Error 3")
            else:
                a2 = stack.pop()
                if(not(isinstance(a2, Node))):
                    a2 = Node(a2)
                a1 = stack.pop()
                if(not(isinstance(a1, Node))):
                    a1 = Node(a1)
                newNode = Node(e,children=[a1, a2])
                setParentOfChildren(newNode)
                stack.append(newNode)
        else:
            stack.append(e)
    if(len(stack) != 1):
        sys.exit("Error 3")
    else:
        e = stack.pop()
        if(not(isinstance(e, Node))):
            e = Node(e)
        return e

def hasGreaterPrecedence(a, b):
    if(a in "^"):
        return True
    elif(a in "*/" and b in "*/+-"):
        return True
    elif(a in "+-" and b in "+-"):
        return True
    else:
        return False

def treeFromInfix(input):

    #Infix to Postfix

    stack = []
    output = []
    while(len(input) > 0):
        e = input.pop(0)
        if(e == "("):
            stack.append(e)
        elif(e == ")"):
            while(len(stack) > 0 and stack[len(stack)-1] != "("):
                output.append(stack.pop())
            if(stack[len(stack)-1] == "("):
                stack.pop()
            else:
                sys.exit("Error 2")
        elif(e in "+-/*^"):
            while(len(stack) > 0 and hasGreaterPrecedence(stack[len(stack)-1],e)):
                output.append(stack.pop())
            stack.append(e)
        else:
            output.append(e)
    while(len(stack) > 0):
        output.append(stack.pop())

    #Postfix to Tree

    stack = []
    input = output

    while(len(input) > 0):
        e = input.pop(0)
        if(isinstance(e, Node)):
            stack.append(e)
        elif(e == '('):
            sys.exit("Error 2")
        elif(e in "+-*/^"):
            if(len(stack) < 2):
                sys.exit("Error 3")
            else:
                a2 = stack.pop()
                if(not(isinstance(a2, Node))):
                    a2 = Node(a2)
                a1 = stack.pop()
                if(not(isinstance(a1, Node))):
                    a1 = Node(a1)
                newNode = Node(e,children=[a1, a2])
                setParentOfChildren(newNode)
                stack.append(newNode)
        else:
            stack.append(e)
    if(len(stack) != 1):
        sys.exit("Error 3")
    else:
        e = stack.pop()
        if(not(isinstance(e, Node))):
            e = Node(e)
        return e

def p_block(p):
    '''
    block : stmt block
        | stmt
    '''
    if(len(p) > 2):
        p[0] = Node('block', children=[p[1], p[2]])
        setParentOfChildren(p[0])
    else:
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : simpstmt ';'
        | flowctrl
    '''
    p[0] = p[1]

def p_simpstmt_assdec_other(p):
    '''
    simpstmt : BOOLEAN ID '=' boolexpr
        | STRING ID '=' strexpr
    '''
    d = Node('declaration', [Node(p[2]), Node(p[1])])
    setParentOfChildren(d)
    p[0] = Node('assignment', [d, p[4]])
    setParentOfChildren(p[0])

def p_simpstmt_assdec_num(p):
    '''
    simpstmt : INT ID '=' numexpr
        | FLOAT ID '=' numexpr
    '''
    d = Node('declaration', [Node(p[2]), Node(p[1])])
    setParentOfChildren(d)
    p[0] = Node('assignment', [d, treeFromInfix(p[4])])
    setParentOfChildren(p[0])

def p_simpstmt_dec(p):
    '''
    simpstmt : INT ID
        | FLOAT ID
        | BOOLEAN ID
        | STRING ID
    '''
    p[0] = Node('declaration', [Node(p[2]), Node(p[1])])
    setParentOfChildren(p[0])

def p_simpstmt_ass(p):
    '''
    simpstmt : ID '=' expr
    '''
    p[0] = Node('assignment', [Node(p[1]), p[3]])
    setParentOfChildren(p[0])

def p_expr_num(p):
    '''
    expr : numexpr
    '''
    p[0] = treeFromInfix(p[1])

def p_expr_str(p):
    '''
    expr : strexpr
    '''
    p[0] = p[1]

def p_expr_bool(p):
    '''
    expr : boolexpr
    '''
    p[0] = p[1]

def p_flowctrl_for(p):
    '''
    flowctrl : FOR '(' simpstmt ';' boolexpr ';' simpstmt ')' '{' block '}'
    '''
    p[0] = Node('for', [p[3], p[5], p[7], p[10]])
    setParentOfChildren(p[0])

def p_flowctrl_dowhile(p):
    '''
    flowctrl : DO '{' block '}' WHILE '(' boolexpr ')' ';'
    '''
    p[0] = Node('dowh', [p[3], p[7]])
    setParentOfChildren(p[0])

def p_flowctrl_while(p):
    '''
    flowctrl : WHILE '(' boolexpr ')' '{' block '}'
    '''
    p[0] = Node('while', [p[3], p[6]])
    setParentOfChildren(p[0])

def p_flowctrl_if(p):
    '''
    flowctrl : IF '(' boolexpr ')' '{' block '}' elif else
    '''
    if(len(p) > 2):
        ch = [p[3], p[6]]
        if(p[8]):
            ch.append(p[8])
        if(p[9]):
            ch.append(p[9])
        p[0] = Node('if', children=ch)
        setParentOfChildren(p[0])

def p_elif(p):
    '''
    elif : ELIF '(' boolexpr ')' '{' block '}' elif
        | empty
    '''
    if(len(p) > 2):
        ch = [p[3], p[6]]
        if(p[8]):
            ch.append(p[8])
        p[0] = Node('elif', children=ch)
        setParentOfChildren(p[0])

def p_else(p):
    '''
    else : ELSE '{' block '}'
        | empty
    '''
    if(len(p) > 2):
        elseNode = Node('else', [p[3]])
        setParentOfChildren(elseNode)
        p[0] = elseNode
        setParentOfChildren(p[0])

def p_numexpr_num(p):
    '''
    numexpr : num
    '''
    p[0] = [p[1]]

def p_numexpr_arit(p):
    '''
    numexpr : numexpr arit numexpr
    '''
    p[0] = []
    for i in p[1]:
        p[0].append(i)
    p[0].append(p[2])
    for i in p[3]:
        p[0].append(i)

def p_numexpr_par(p):
    '''
    numexpr : '(' numexpr ')'
    '''
    p[0] = []
    p[0].append(p[1])
    for i in p[2]:
        p[0].append(i)
    p[0].append(p[3])

def p_num(p):
    '''
    num : NUMI
        | NUMF
        | ID
    '''
    p[0] = p[1]

def p_arit(p):
    '''
    arit : '+'
        | '-'
        | '*'
        | '/'
        | '^'
    '''
    p[0] = p[1]

def p_strexpr_one(p):
    '''
    strexpr : concat
    '''
    p[0] = p[1]

def p_strexpr_concat(p):
    '''
    strexpr : concat '+' strexpr
    '''
    p[0] = Node('concat', [p[1], p[3]])
    setParentOfChildren(p[0])

def p_strexpr_par(p):
    '''
    strexpr : '(' strexpr ')'
    '''
    p[0] = Node(p[2])

def p_concat_one(p):
    '''
    concat : STR
        | ID
    '''
    p[0] = Node(p[1])

def p_concat_par(p):
    '''
    concat : STRING '(' numexpr ')'
    '''
    numNode = treeFromInfix(p[3])
    setParentOfChildren(numNode)
    p[0] = Node('num2string', [numNode])
    setParentOfChildren(p[0])

def p_boolexpr_bin(p):
    '''
    boolexpr : boolexpr AND boolexpr
        | boolexpr OR boolexpr
        | boolexpr EQUALS boolexpr
        | boolexpr NOTEQUALS boolexpr
    '''
    p[0] = Node(p[2], [p[1], p[3]])
    setParentOfChildren(p[0])

def p_boolexpr_idstr(p):
    '''
    boolexpr : ID EQUALS strexpr
        | ID NOTEQUALS strexpr
    '''
    p[0] = Node(p[2], [Node(p[1]), p[3]])
    setParentOfChildren(p[0])

def p_boolexpr_idnum(p):
    '''
    boolexpr : ID EQUALS numexpr
        | ID NOTEQUALS numexpr
        | ID GTREQTHAN numexpr
        | ID LSSEQTHAN numexpr
        | ID '<' numexpr
        | ID '>' numexpr
    '''
    p[0] = Node(p[2], [Node(p[1]), treeFromInfix(p[3])])
    setParentOfChildren(p[0])

def p_boolexpr_idbool(p):
    '''
    boolexpr : ID EQUALS boolexpr
        | ID NOTEQUALS boolexpr
    '''
    p[0] = Node(p[2], [Node(p[1]), p[3]])
    setParentOfChildren(p[0])

def p_boolexpr_one(p):
    '''
    boolexpr : boolop
    '''
    p[0] = p[1]

def p_boolexpr_par(p):
    '''
    boolexpr : '(' boolexpr ')'
    '''
    p[0] = p[2]

def p_boolop(p):
    '''
    boolop : strcomp
        | numcomp
        | bool
    '''
    p[0] = p[1]

def p_bool(p):
    '''
    bool : TRUE
        | FALSE
        | ID
    '''
    p[0] = Node(p[1])

def p_strcomp(p):
    '''
    strcomp : strexpr NOTEQUALS strexpr
        | strexpr EQUALS strexpr
    '''
    p[0] = Node(p[2], [p[1], p[3]])
    setParentOfChildren(p[0])

def p_numcomp(p):
    '''
    numcomp : numexpr comp numexpr
    '''
    p[0] = Node(p[2], [treeFromInfix(p[1]), treeFromInfix(p[3])])
    setParentOfChildren(p[0])
        
def p_comp(p):
    '''
    comp : EQUALS
        | NOTEQUALS
        | GTREQTHAN
        | LSSEQTHAN
        | '<'
        | '>'
    '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    pass

parserer = yacc.yacc()

root = parserer.parse(lexer=plylexer.lx, input=open("input.txt").read())
if root == None:
    sys.exit("[ ! ] Syntax error.")

def printChildren(node):
    print(node.type)
    if node.children:
        for i in node.children:
            printChildren(i)

#printChildren(boolToTree(['true', 'and', '(','false', 'or', 'false', ')']))

#root = treeFromInfix(['4', '-', '5'])

#printChildren(root)