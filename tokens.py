import ply.lex as lex

reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'do' : 'DO',
    'while' : 'WHILE',
    'boolean' : 'BOOLEAN',
    'float' : 'FLOAT',
    'int' : 'INT',
    'string' : 'STRING',
    'true' : 'TRUE',
    'false' : 'FALSE'
}

tokens = list(reserved.values()) + [
    'NUMI',
    'NUMF',
    'ID',
    'STR',
    'EQUALS',
    'NOTEQUALS',
    'GTREQTHAN',
    'LSSEQTHAN'
]

literals = ['-', '+', '*', '/', '^', '=', '>', '<', '(', ')', '{', '}', ';']