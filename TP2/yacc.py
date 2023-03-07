from ply import yacc
from lex import tokens

f = open("TP1/data/medicina.txt", "r")
texto = f.read()
f.close()


f = open("TP2/data/medicina.json", "w")
linhas = []
linhas.append("[")

def p_elementos(p):
    """elementos : elementos elemento
                 | elementos vids
                 | 
                 """
    global linhas
    
    if len(p) == 3:
        linhas.append("\t{")
        linhas.append(p[2])
        linhas.append("\t},")

def p_elemento(p):
    """elemento : ELEMENTO NUMERO texto tipo area"""
    p[0] = f"""\t\t"numero": {str(p[2])},
\t\t{str(p[4])}
\t\t{str(p[5])},
\t\t"ga": "{str(p[3])}\""""


def p_tipo(p):
    """tipo : TIPO texto
            |
    """
    if len(p) == 3:
        p[0] = f""""tipo": "{str(p[2])}","""
    else:
        p[0] = ""

def p_area(p):
    """area : AREA texto sin
            | AREA texto var
            | AREA texto lingua
    """
    p[0] = f""""área": "{str(p[2])}",
\t\t{str(p[3])}"""


def p_lingua(p):
    """lingua :  LINGUA texto lingua
                | LINGUA texto nota
                | LINGUA texto vids
                | LINGUA texto
    """
    if len(p) == 4:
        p[0] = f""""{str(p[1][2:])}": "{str(p[2])}",
\t\t{str(p[3])}"""
    else:
        p[0] = f""""{str(p[1][2:])}": "{str(p[2])}\""""

def p_sin(p):
    """sin : SIN texto lingua
           | SIN texto var
    """
    p[0] = f""""sin": "{str(p[2])}",
\t\t{str(p[3])}"""

def p_vids(p):
    """vids : vid
    """
    p[0] = f""""vids": [
\t\t\t{str(p[1])}
\t\t]"""

def p_vid(p):
    """vid : VID texto '»' texto
            | VID texto '»' texto vid
    """
    if len(p) == 5:
        p[0] = f""""{str(p[2])} --- {str(p[4])}\""""
    else:
        p[0] = f""""{str(p[2])} --- {str(p[4])}",
\t\t\t{str(p[5])}"""

def p_var(p):
    """var : VAR texto lingua"""
    p[0] = f""""var": "{str(p[2])}",
        {str(p[3])}"""


def p_nota(p):
    """nota : NOTA texto vids
            | NOTA texto
    """
    if len(p) == 4:
        p[0] = f""""mota": "{str(p[2])}",
\t\t{str(p[3])}"""
    else:
        p[0] = f""""mota": "{str(p[2])}\""""

def p_texto(p):
    """texto : TEXTO texto
            | NUMERO texto
            | TEXTO"""
    #global elemento, dicionario
    #p[0] = "TEXTO---\n")
    if len(p) == 3:
        p[0] = p[1] + " " + p[2]
    else:
        p[0] = p[1]


def p_error(p):
    print("Syntax error in input!" + str(p))
    quit()

parser = yacc.yacc()
parser.parse(texto)

linhas[-1] = linhas[-1][:-1]
linhas.append("]")

for linha in linhas:
    f.write(linha + "\n")