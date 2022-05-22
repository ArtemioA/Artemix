import sympy as sy
import IPython

global DatosList, Orden
DatosList = []
Orden = 8

def Redondear(expr):
  if isinstance(expr, sy.Expr) or isinstance(expr, sy.Float):
    Aproximacion = expr.xreplace(sy.core.rules.Transform(lambda x: x.round(Orden), lambda x: isinstance(x, sy.Float)))
  elif isinstance(expr,float) or isinstance(expr,int):
    Aproximacion = round(expr,Orden)
  else:
    Aproximacion = expr
  return Aproximacion

def Evaluar(Ecuacion):
  DataRealSymbolList = []#Guarda en formato symbolo todos los Datos
  for element in DatosList:
    if (element[1] != None) :
      if isinstance(element[1],sy.Float) or isinstance(element[1],float) or isinstance(element[1],int):

        word = "" 
        for letra in sy.latex(Redondear(element[1])):
          if letra == " ":
            word = word+"~"
          else:
            word = word+letra
        DataRealSymbolList.append([element[0],sy.symbols("("+word+")")])
    else:
      #Es decir, si es un simbolo sin valor (None) o coleccion de simbolos. Entonces:
      DataRealSymbolList.append([element[0],word])
  #display(DataRealSymbolList)
  return Ecuacion.subs(DataRealSymbolList)

def D(elemento,color = "red"):#Display
  print("")
  Tipo = None
  if isinstance(elemento,sy.core.relational.Equality):
    Tipo = "Ecuacion"
  elif isinstance(elemento,list):
    Tipo = "Componente"
    c_componente = elemento
  
  if Tipo == "Ecuacion":
    texto = sy.latex(elemento.args[0]) + "=" + sy.latex(elemento.args[1])
    IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+texto+"}"))

  if Tipo == "Componente":
    if not isinstance(c_componente[0],str):#isinstance(c_componente[0],sy.core.symbol.Symbol) or isinstance(c_componente[0],sy.core.symbol.Symbol) :
      IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+sy.latex(c_componente[0])+" = "+sy.latex(Redondear(c_componente[1]))+"}"))
    elif isinstance(c_componente[0],str):
      IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+c_componente[0]+" = "+sy.latex(Redondear(c_componente[1]))+"}"))
  #Código para actualizar valores: if isinstance(element[1], sy.Expr):element = [element[0],element[1].subs(c_componente[0],c_componente[1])]

def G(c_componente):#Guardar
  color = "gray"
  dentro = False
  for element in DatosList:
    if element[0] == c_componente[0]:
      element[1] = c_componente[1]
      dentro = True
  
  if dentro == False:
    DatosList.append(c_componente)
  D(c_componente,color)

def A(c_componente):#Actualizar
  color = "red"
  for element in DatosList:
    if element[0] == c_componente[0]:
      #Identificamos el componente en la lista de datos guardados
      #Ahora actualizamos los valores
      D([c_componente[0],Evaluar(c_componente[1])],color)
      D([c_componente[0],element[1].subs(DatosList)],color)
      element[1] = element[1].subs(DatosList)
      return element#Sistema por Artemio Araya :)