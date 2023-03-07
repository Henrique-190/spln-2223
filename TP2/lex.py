f = open("TP1/data/medicina.txt", "r")
texto = f.read()
f.close()

from ply import lex

tokens = (
    'ELEMENTO',
    'AREA',
    'LINGUA',
    'SIN',
    'VID',
    'VAR',
    'NOTA',
    'NUMERO',
    'TIPO',
    'TEXTO'
)

literals = (
    '»'
)

t_ignore = ' \t\n'

def t_ELEMENTO(t):
    r'ELEMENTO'
    return t

def t_AREA(t):
    r'AREA::'
    return t

def t_LINGUA(t):
    r'\@\ (pt|en|es|la)'
    return t

def t_SIN(t):
    r'SIN::'
    return t

def t_VID(t):
    r'VID::'
    return t

def t_VAR(t):
    r'VAR::'
    return t

def t_NOTA(t):
    r'NOTA::'
    return t

def t_NUMERO(t):
    r'\d+'
    return t

def t_TIPO(t):
    r'TIPO::'
    return t

def t_TEXTO(t):
    r'[\wáéíóú\,\d\:\(\)\[\]\{\}\.\;\-\!\?\*\“\”\‘\’\—\–\%\/\+]+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    quit()

lexer = lex.lex()

"""
lexer.input(texto)

while True:
    tok = lexer.token()
    if not tok: 
        quit()
    print(tok)
"""