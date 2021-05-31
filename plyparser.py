import ply.yacc as yacc
from plylexer import tokens, literals
import plylexer
import sys

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf


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
                a1 = stack.pop()
                stack.append(Node(e,children=[a1, a2]))
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
    else:
        p[0] = p[1]
    treeFromInfix(['a'])

def p_stmt(p):
    '''
    stmt : simpstmt ';'
        | flowctrl
    '''
    p[0] = p[1]

def p_simpstmt_assdec(p):
    '''
    simpstmt : type ID '=' expr
    '''
    d = Node('declaration', [p[2], p[1]])
    p[0] = Node('assignment', [d, p[4]])

def p_simpstmt_dec(p):
    '''
    simpstmt : type ID
    '''
    p[0] = Node('declaration', [p[2], p[1]])

def p_simpstmt_ass(p):
    '''
    simpstmt : ID '=' expr
    '''
    p[0] = Node('assignment', [p[1], p[3]])

def p_type(p):
    '''
    type : BOOLEAN
        | FLOAT
        | INT
        | STRING
    '''
    p[0] = Node(p[1])

def p_expr_num(p):
    '''
    expr : numexpr
    '''
    p[0] = treeFromInfix(p[1])

def p_expr_other(p):
    '''
    expr : strexpr
        | boolexpr
    '''
    p[0] = p[1]

def p_flowctrl(p):
    '''
    flowctrl : FOR '(' simpstmt ';' boolexpr ';' simpstmt ')' '{' block '}'
        | DO '{' block '}' WHILE '(' boolexpr ')' ';'
        | WHILE '(' boolexpr ')' '{' block '}'
        | IF '(' boolexpr ')' '{' block '}' elif else
    '''
    pass

def p_elif(p):
    '''
    elif : ELIF '(' boolexpr ')' '{' block '}' elif
        | empty
    '''
    pass

def p_else(p):
    '''
    else : ELSE '{' block '}'
    '''
    pass

def p_numexpr_num(p):
    '''
    numexpr : num
    '''
    p[0] = p[1]

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

def p_strexpr(p):
    '''
    strexpr : concat
        | concat '+' concat
        | '(' concat ')'
    '''
    pass

def p_concat(p):
    '''
    concat : STR
        | ID
        | STRING '(' numexpr ')'
    '''
    pass

def p_boolexpr(p):
    '''
    boolexpr : boolop AND boolexpr
        | boolop OR boolexpr
        | boolop EQUALS boolexpr
        | boolop NOTEQUALS boolexpr
        | boolop
        | '(' boolexpr ')'
    '''
    pass

def p_boolop(p):
    '''
    boolop : strcomp
        | numcomp
        | bool
    '''
    pass

def p_bool(p):
    '''
    bool : TRUE
        | FALSE
        | ID
    '''
    pass

def p_strcomp(p):
    '''
    strcomp : strexpr NOTEQUALS strexpr
        | strexpr EQUALS strexpr
    '''
    pass

def p_numcomp(p):
    '''
    numcomp : numexpr comp numexpr
    '''
    pass

def p_comp(p):
    '''
    comp : EQUALS
        | NOTEQUALS
        | GTREQTHAN
        | LSSEQTHAN
        | '<'
        | '>'
    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    pass

parserer = yacc.yacc()

root = parserer.parse(lexer=plylexer.lx, input=open("input.txt").read())

def printChildren(node):
    if hasattr(node, "type"):
        print(node.type)
    else:
        print(node)
    if hasattr(node, "children") and node.children:
        for i in node.children:
            printChildren(i)

#root = treeFromInfix(['4', '-', '5'])

printChildren(root)