# Objetivos:
Representação semântica do pdf para JSON, associado à vista chamado do galego para a informação
passar esta Representação para:
- Dicionário médico abstrato, onde o galego passa para as outras línguas
- Linguagem de dicionários - escrever a respetiva gramática e o parser associado  
  



# Feito:
Eis a gramática:
```
S -> elementos  
  
elementos -> elementos elemento          
           | elementos vids  
           | elementos  
  
elemento -> ELEMENTO NUMERO texto tipo area

tipo -> TIPO texto

area -> AREA texto sin  
      | AREA texto var  
      | AREA texto lingua  

lingua -> LINGUA texto lingua  
        | LINGUA texto nota  
        | LINGUA texto vids  
        | LINGUA texto  

sin -> SIN texto lingua sin  
     | SIN texto var sin  

vids -> vid vids  

vid -> VID texto » texto  
     | VID texto » texto vid  

var -> VAR texto lingua  

nota -> NOTA texto vids  
      | NOTA texto  

texto -> TEXTO texto  
       | NUMERO texto  
       | TEXTO  
```