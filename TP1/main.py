# ZEP -> E*
# E -> EC
#    | ER
# EC -> num pals po s CORPO
# CORPO -> area LINGUAS
# LINGUAS -> pt pals
#          | en pals
#          | es pals
# ER -> pals VID
# VID -> Vid.- pals

import re

texto = open('TP1/data/medicina.xml', 'r').read()

def remove_notImportant(texto):
    texto = re.sub(r'<\?xml.+\n.+\n', r'', texto)
    texto = re.sub(r'<\/?pdf2xml.+\n', r'', texto)
    texto = re.sub(r'\ *<fontspec.+\n', r'', texto)
    texto = re.sub(r'</pdf2xml\.*\n', r'', texto)
    texto = re.sub(r'<text.+>\n<text.*>ocabulario<\/text>\n<text.*<\/text>\n', r'', texto)
    texto = re.sub(r'</?page.*\n', r'', texto)
    
    #Remove Espaços
    texto = re.sub(r'\<text.+\>\<b\>\ +\<\/b\>\<\/text\>\n', r'', texto)
    texto = re.sub(r'\<text.+\>\<i\>\ +\<\/i\>\<\/text\>\n', r'', texto)
    texto = re.sub(r'\<text.+\>\s+\<\/text\>\n', r'', texto)

    #Tira linhas com fonte igual a 13 ou 15 (CO2)
    texto = re.sub(r'\n<text.+font="1(3|5)"><(\w)>.+</\2></text>', r'\1', texto)

    return texto
texto = remove_notImportant(texto)


def joinTEXT(texto):
    #Sempre que tem <i><b>, então é porque essa linha pertence à anterior que contém font="3"
    texto = re.sub('(<text.+font="3"><b>.+)(</b></text>)\n<text.+font="\d+"><i><b>(.+)</b></i></text>', r'\1 \3 \2', texto)
    texto = re.sub(r'(<text.+font=")(\d+)("><)(\w)(>.+)(</\4><\/text>)\n<text.+font="\2"><\4>(.+)<\/\4></text>', r'\1\2\3\4\5 \7\6', texto)
    texto = re.sub(r'(<text.+font=")(\d+)(">)(.+)(<\/text>)\n<text.+font="\2">(.+)</text>', r'\1\2\3\4\6\5', texto)
    return texto
texto = joinTEXT(texto)


def markSIN(texto):
    #Há frases que contêm o termo SIN.- e VAR.-, por isso alguns são captados
    texto = re.sub(r'<text.+>\s*SIN\.-(.*)</text>',r'SIN:: \1',texto)
    return texto
texto = markSIN(texto)


def marcaNota(texto):
    texto = re.sub(r'<text.+>\s*Nota\s*\.-(.+)</text>',r'NOTA:: \1',texto)
    return texto
texto = marcaNota(texto)


def marcaVAR(texto):
    texto = re.sub(r'<text.+>\s*VAR\s*\.-(.+)</text>',r'VAR:: \1',texto)
    return texto
texto = marcaVAR(texto)


def marcaVid(texto):
    texto = re.sub(r'.+<b>(.+)</b>.+\n<text.+>\s*Vid\.-(.+)</text>', r'VID:: \1 » \2', texto)
    texto = re.sub(r'.+<b>(.+)</b></text>\n<text.+font="5">\s*Vid\.-?\s+</text>\n.*font="6"><i>(.+)</i></text>', r'VID:: \1 » \2', texto)
    texto = re.sub(r'.+font="3"><b>(.+)</b></text>\n<text.+font="0">\s*Vid\.(.+)</text>', r'VID:: \1 » \2', texto)
    return texto
texto = marcaVid(texto)


def marcaLinguas(texto):
    texto = re.sub(r'<text.+>\s*en\s*</text>', r'@ en', texto)
    texto = re.sub(r'<text.+>\s*es\s*</text>', r'@ es', texto)
    texto = re.sub(r'<text.+>\s*pt\s*</text>', r'@ pt', texto)
    texto = re.sub(r'<text.+>\s*la\s*</text>', r'@ la', texto)
    return texto
texto = marcaLinguas(texto)


def marca_titulo(texto):
    texto = re.sub(r'<text.+"3"><b>\s*(\d+.+)</b></text>', r'ELEMENTO \1', texto)
    texto  = re.sub(r'<text.+"2">\s*(\d+)\s+</text>\n<text.+font="3"><b>(.+)</b></text>', r'ELEMENTO \1 \2', texto)
    texto  = re.sub(r'<text.+"12">\s*(\d+)\s+<\/text>\n<text.+font="11"><b>(.+)<\/b><\/text>', r'ELEMENTO \1 \2', texto)
    texto = re.sub(r'<text.+"2">\s*(\d+)\s+<\/text>\n<text.+font="3"><b>(.+)<\/b><\/text>\n', r'ELEMENTO \1 \2', texto)
    return texto
texto = marca_titulo(texto)


def someTexto(texto):
    texto = re.sub(r'\n<text.+>([^<]+)</text>',r'\1',texto)
    texto = re.sub(r'\n<text.+font="1\d+">(.+)</text>', r'\1', texto)
    texto = re.sub(r'\n<text.+font="10"><i><b>(.+)</b></i></text>\n<text.+font="3"><b>(.+)</b></text>', r'\1 \2', texto)
    texto = re.sub(r'(ELEMENTO \d.+)\n.+font="3"><b>\s+(\w)</b></text>', r'\1 \2', texto)
    return texto
texto = someTexto(texto)


def area(texto):
    texto = re.sub(r'(ELEMENTO \d.+)\n.+font="\d"><i>(.+)</i></text>', r'\1 \nAREA:: \2', texto)
    return texto
texto = area(texto)



def resto(texto):
    texto = re.sub(r'<text.+font="(3|6|7)"><(\w)>(.+)</\2></text>', r'\3', texto)
    texto = re.sub(r'(</\w><\w>|</b>)', r'', texto)
    return texto
texto = resto(texto)


def tipo(texto):
    texto = re.sub(r'(ELEMENTO.+)\s(m\s+pl)\s+\n', r'\1\nTIPO::\2\n', texto)
    texto = re.sub(r'(ELEMENTO.+)\s(f\s+pl)\s+\n', r'\1\nTIPO::\2\n', texto)
    texto = re.sub(r'(ELEMENTO.+)\s(m|f|s|a)\s+\n', r'\1\nTIPO::\2\n', texto)
    texto = re.sub(r'(ELEMENTO.+)\s(sg)\s+\n', r'\1\nTIPO::\2\n', texto)
    return texto
texto = tipo(texto)

file = open('TP1/data/medicina.txt', 'w')
file.write(texto)
file.close()