def readtxt2list(name):
    content=[]
    with open(name, 'r') as file:
        for i in file.readlines():
            content.append(str(i))#.replace("\n",""))
    return content
def readtxt2points(name):
    contentenido=[]
    with open(name, 'r') as file:
        for i in file.readlines():
            linea2puntos(contentenido,str(i).replace("\n",""))
    return contentenido

def linea2puntos(todosPuntos,texto,separador="\t"):
	num=""
	for i in texto:
		if not i==separador:
			num+=i
		else:
			todosPuntos.append(float(num))
			num=""

