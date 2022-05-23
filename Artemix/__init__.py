import sympy as sy
import IPython

DatosList = []
Orden = 0

#Funciones de Redondeo
def Redondear(expr):#Redondeamos la expresión.
  if isinstance(expr, sy.Expr) or isinstance(expr, sy.Float):
    Aproximacion = expr.xreplace(sy.core.rules.Transform(lambda x: x.round(Orden), lambda x: isinstance(x, sy.Float)))
  elif isinstance(expr,float) or isinstance(expr,int):
    Aproximacion = round(expr,Orden)
  else:
    Aproximacion = expr
  return Aproximacion


def D(elemento,color = "red"):#Por default se imprime en rojo, para indicar que es un derivado.
  print("")
  Tipo = None
  if isinstance(elemento,sy.core.relational.Equality):#Si el elemento ingresado es una ecuación, entonces la identificamos
    Tipo = "Ecuacion"
  elif isinstance(elemento,list):#Si el elemento ingresado es un componente, entonces lo identificamos.
    Tipo = "Componente"
    c_componente = elemento
  
  if Tipo == "Ecuacion":#Si hemos identificado el elemento ingresado como una ecuación, entonces la imprimimos en rojo
    texto = sy.latex(elemento.args[0]) + "=" + sy.latex(elemento.args[1])
    IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+texto+"}"))

  if Tipo == "Componente":#Si hemos identificado el elemento ingresado como un componente, entonces lo imprimimos en rojo
    if not isinstance(c_componente[0],str):#isinstance(c_componente[0],sy.core.symbol.Symbol) or isinstance(c_componente[0],sy.core.symbol.Symbol) :
      IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+sy.latex(c_componente[0])+" = "+sy.latex(Redondear(c_componente[1]))+"}"))
    elif isinstance(c_componente[0],str):
      IPython.display.display(IPython.display.Latex(r"\textcolor{"+str(color)+"}{"+c_componente[0]+" = "+sy.latex(Redondear(c_componente[1]))+"}"))
  #Código para actualizar valores: if isinstance(element[1], sy.Expr):element = [element[0],element[1].subs(c_componente[0],c_componente[1])]


def E(expr,color):
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
  D(expr)
  D([expr[0],expr[1].subs(DataRealSymbolList)])
  D([expr[0],expr[1].subs(DatosList)])



def G(c_componente):#Guardar
  dentro = False
  for element in DatosList:
    if element[0] == c_componente[0]:
      element[1] = c_componente[1]
      dentro = True#Si el elemento ha sido guardado antes, entonces no lo volvemos a ingresar. Sino que sobre escribimos lo que dicho
      #componente significaba con el valor actual que se desea guardar.
  
  if dentro == False:
    DatosList.append(c_componente)#Si el emento no estaba adentro, simplemente lo agregamos.
  
  #Renderizado Gris
  D(c_componente,"gray")#Hacemos un print renderizado en color gris para indicar que el elemento ha sido definido/guardado


#Arreglar
def A(c_componente):#Actualizar
  color = "red"
  for element in DatosList:
    if element[0] == c_componente[0]:
      #Identificamos el componente en la lista de datos guardados
      #Ahora actualizamos los valores
      E([c_componente[0],c_componente[1]],color)
      #D([c_componente[0],E(c_componente[1])],color)
      #D([c_componente[0],element[1].subs(DatosList)],color)
      element[1] = element[1].subs(DatosList)
      return element#Sistema por Artemio Araya :)
