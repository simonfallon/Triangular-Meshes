# from MetodosVisualizacion import *
import tools.Plot
from tools.Tools import readtxt2list
from tools.Triangular import frontera
import numpy as np
from itertools import combinations
from operator import itemgetter
import scipy.optimize as op

ARCHIVO1="ptsbunny.txt"
ARCHIVO2="tbunny.txt"

puntos_cent = []
vecindades = {}
puntos_irreg = []
noPosibles = []
puntos = []

triangulosquitados = set()
triangulos = set()

for punto in readtxt2list(ARCHIVO1):  # Puntos a tupla de valores p = (x,y,z)
    pto = tuple([float(i) for i in punto.split(',')])
    puntos.append(pto)

for tri in readtxt2list(ARCHIVO2):  # Triangulos a tupal de puntos t = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)
    triangulos.add(tuple([puntos[int(i) - 1] for i in tri.split(',')]))

# con pi = (xi,yi,zi)
# Dictionario de puntos p : ({p,p1,p2...},{(p,p2,p3),(p,p3,p4)...})
# Diccionario entra punto, sale tupla con primero, los puntos en el vecindario y en segundo indice triangulos en vecindario
def frontera(self,punto):
    return not len(self.vecindades[punto][0]) == len(self.vecindades[punto][1]) + 1


def irreg(punto):
    if len(vecindades[punto][0]) < len(vecindades[punto][1]) + 1:
        print(punto)
    return len(vecindades[punto][0]) < len(vecindades[punto][1]) + 1

def crearvecindades():
    vecindades.clear()
    for tri in triangulos:
        for punto in tri:
            if punto not in vecindades:
                vecindades[punto] = (set(tri), {tri})
            else:
                vecindades[punto][0].update(set(tri))
                vecindades[punto][1].add(tri)
    puntos_cent.clear()
    puntos_cent.extend(list(filter(lambda punto: frontera(punto) == False, puntos)))


crearvecindades()


def plotmallas():
    triangulos = set()
    list(map(lambda vec: triangulos.update(vec[1]), vecindades.values()))
    Plot.plotmalla(puntos, triangulos)


def puntos_list():
    return list(map(lambda punto: list(punto), puntos))


def toindexp(p):
    return puntos.index(p)


def toindextri(t):
    return tuple(map(lambda p: puntos.index(p), t))


def toindexvec(v):
    return (set(map(lambda p: toindexp(p), v[0])), set(map(lambda tri: toindextri(tri), v[1])))



def tritovec(tri):
    return list(map(lambda punto: np.asarray(punto),tri))


# Retorna minimo angulo dihedrales de vecindad.
def minanguloD(punto):
    vecindad = vecindades[punto]
    # Se crea una lista con tuplas de los triangulos adyacentes
    tri_adyacentes = list(
        filter(lambda par: len(set(par[0]).intersection(set(par[1]))) == 2, list(combinations(vecindad[1], 2))))
    minang = 4;
    for par in tri_adyacentes:
        inter = list(set(par[0]).intersection(set(par[1])))
        vecI = np.asarray(inter[1]) - np.asarray(inter[0])
        vec1 = np.asarray(list(set(par[0]).difference(set(inter)))[0]) - np.asarray(inter[0])
        vec2 = np.asarray(list(set(par[1]).difference(set(inter)))[0]) - np.asarray(inter[0])
        plano1 = np.cross(vecI, vec1)
        plano2 = np.cross(vecI, vec2)
        ang = np.math.acos(np.dot(plano1, plano2) / (np.linalg.norm(plano1) * np.linalg.norm(plano2)))
        minang = min(minang, ang)
    return minang

def objective(x,*args):
    puntos = args[0]
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    f = []
    for punto in puntos:
        x, y, z = punto
        f.append((a * x + b * y + c * z + d)**2 / (a ** 2 + b ** 2 + c ** 2) ** (0.5))
    return sum(f)

def planpromedio(puntos):
    R=[]
    pts=np.array(list(puntos))
    x,y,z=np.mean(np.transpose(pts),axis=1)
    for p in pts:
        x1 = p[0] - x
        x2 = p[1] - y
        x3 = p[2] - z
        R.append([x1, x2, x3])
    R = np.array(R)
    RtR = np.dot(R.T, R)
    W, v = np.linalg.eig(RtR)
    W = abs(W)
    minW = np.where(W == W.min())
    vn = v[minW]
    return vn 

first = True
def removepoint(punto):
    try:
        vec = vecindades[punto]
        paresady = list(map(lambda tri: list(set(tri)-{punto}), vec[1]))
        polygon = paresady.pop(1)
        while not polygon[0] == polygon[-1]:
            nextpar = list(filter(lambda par: polygon[-1] in par, paresady))[0]
            paresady.remove(nextpar)
            nextpar.remove(polygon[-1])
            polygon.append(nextpar[0])
        polygon.pop(0)
        polygon = list(map(lambda pt: np.asarray(pt),polygon))
        triaux = set()
        puntosaux = set()
        for pt in vec[0]:
                triaux.update(vecindades[pt][1])
                puntosaux.update(vecindades[pt][0])
        #Plot.plotmalla(list(puntosaux), triaux)
        triaux.difference_update(vec[1])
        triaux.update(triang(polygon))
        #Plot.plotmalla(list(puntosaux),triaux)
        triangulos.update(triang(polygon))
        triangulos.difference_update(vec[1])
        puntos.remove(punto)
        crearvecindades()
        listaquitar()
    except Exception as ex:
        #Plot.plotmalla(list(puntosaux), triaux)
        #Plot.plotmalla(list(vec[0]),vec[1])
        noPosibles.append(punto)
        listaquitar()
        print(ex.with_traceback())
        print('No fue posible quitar el punto : ',punto)

def triang(polygon):
    if len(polygon)==0:
        return []
    if len(polygon)<3:
        raise Exception('Menor que 3')
    if len(polygon) == 3:
        if np.linalg.norm(np.cross(polygon[0] - polygon[1], polygon[0] - polygon[2])) == 0:
            raise Exception('Area de Triangulo 0')
        return [(tuple(polygon[0]),tuple(polygon[1]),tuple(polygon[2]))]
    plano = planpromedio(polygon)
    for pt1 in polygon:
        for pt2 in polygon:
            i1 = [np.array_equal(pt1,x) for x in polygon].index(True)
            i2 = [np.array_equal(pt2,x) for x in polygon].index(True)
            if i1 == i2:
                continue
            indxs = sorted([i1,i2])
            pol1 = polygon[:indxs[0]]
            pol2 = [polygon[indxs[0]]]
            pol3 = polygon[indxs[0]:indxs[1]]
            pol4 = [polygon[indxs[1]]]
            pol5 = polygon[indxs[1]:]
            p1 = pol3+pol4
            p2 = pol5+pol1+pol2
            ilegalTriangle = False
            planoT = np.cross(plano, p1[0]-p1[-1])
            if len(p1)==len(polygon) or len(p2)==len(polygon):
                continue
            for i in p1:
                for j in p2:
                    if np.dot(planoT, i) * np.dot(planoT, j) < 0:
                        ilegalTriangle = True
            if ilegalTriangle:
                continue
            try:
                return triang(p1)+triang(p2)
            except Exception as ex:
                print(indxs)
                print(ex)
                continue
    raise Exception('No se Puede Triangular')



def savemesh(name):
    tri = list(map(lambda tri: str(puntos.index(tri[0])+1)+','+str(puntos.index(tri[1])+1)+','+str(puntos.index(tri[2])+1)+'\n', triangulos))
    pts = list(map(lambda pt: str(pt[0])+','+str(pt[1])+','+str(pt[2])+'\n', puntos))
    filepts = open("pts"+name+".txt", "w+")
    filet = open("t" + name + ".txt", "w+")
    filet.writelines(tri)
    filepts.writelines(pts)




def listaquitar():
    global angdict
    angdict = []
    for punto in puntos_cent:
        angdict.append((punto, minanguloD(punto)))
    angdict = sorted(angdict, key=itemgetter(1),reverse=True)
    for punto in noPosibles:
        for i in angdict:
            if i[0] == punto:
                angdict.remove(i)
listaquitar()


def quitar():
    numquitar = 200
    print("Se intentaran quitar", numquitar, "puntos", 'de', len(angdict))
    nquitados = 0;
    for i in range(0,numquitar):
        print(i-len(noPosibles))
        print(nquitados)
        if nquitados%500 == 0:
            Plot.plotmalla(puntos, triangulos)
            savemesh('bunny'+str(nquitados))
        try:
            removepoint(angdict[0][0])
            nquitados += 1;
        except:
            print('No fue posible quitar el punto : ',angdict[0][0])


def mirarpuntos(vec):
    puntos = list(vec[0])
    triangulos = vec[1]
    Plot.plotmalla(triangulos,puntos)

print(len(angdict))


quitar()


def hausdorff(pts1,pts2):
    maximo1 = -1
    for p1 in pts1:
        minimo =  np.linalg.norm(np.array(p1)-np.array(pts2[0]))
        for p2 in pts2:
            a=np.linalg.norm(np.array(p1)-np.array(p2))
            if(minimo>a):
                minimo =a
        if(maximo1<minimo):
            maximo1=minimo
    maximo2 = -1 
    for p1 in pts2:
        minimo =  np.linalg.norm(np.array(p1)-np.array(pts2[0]))
        for p2 in pts1:
            a=np.linalg.norm(np.array(p1)-np.array(p2))
            if(minimo>a):
                minimo =a
        if(maximo2<minimo):
            maximo2=minimo
    return max(maximo1,maximo2)

print("La distancia Hausdorff entre la malla original y la reducida es: ",hausdorff(puntos, puntosiniciales))


Plot.plotmalla(puntos, triangulos)
