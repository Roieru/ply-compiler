import ply.yacc as yacc
from plylexer import tokens, literals
import plylexer

def p_block(p):
    '''
    block : stmt block
        | stmt
    '''
    pass

def p_stmt(p):
    '''
    stmt : simpstmt ';'
        | flowctrl
    '''
    pass

def p_simpstmt_assdec(p):
    '''
    simpstmt : type ID '=' expr
    '''
    pass

def p_simpstmt_dec(p):
    '''
    simpstmt : type ID
    '''
    pass

def p_simpstmt_ass(p):
    '''
    simpstmt : ID '=' expr
    '''
    pass

def p_type(p):
    '''
    type : BOOLEAN
        | FLOAT
        | INT
        | STRING
    '''
    pass

def p_expr(p):
    '''
    expr : numexpr
        | strexpr
        | boolexpr
    '''
    pass

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

def p_numexpr(p):
    '''
    numexpr : num
        | num arit numexpr
        | '(' numexpr ')'
    '''
    pass

def p_num(p):
    '''
    num : NUMI
        | NUMF
        | ID
    '''
    pass

def p_arit(p):
    '''
    arit : '+'
        | '-'
        | '*'
        | '/'
        | '^'
    '''
    pass

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

print(parserer.parse(lexer=plylexer.lx, input=open("input.txt").read()))