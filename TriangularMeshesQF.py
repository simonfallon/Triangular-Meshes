# from MetodosVisualizacion import *
import tools.Plot
from tools.Tools import readtxt2list
from tools.Triangular import frontera
import numpy as np
from itertools import combinations
from operator import itemgetter
import scipy.optimize as op

NOMBRE1="Pts_esfera.txt"
NOMBRE2="Tgs_esfera.txt"

ARCHIVO1="data/puntos/"+NOMBRE1
ARCHIVO2="data/triangulos/"+NOMBRE2

CARACTER_SEPARACION = '\t'#se podria automatisar , cogiendo el primer caracter que no sea un numero ni un punto

puntos_cent = []
vecindades = {}
puntos_irreg = []
noPosibles = []
puntos = []

triangulosquitados = set()
triangulos = set()


for punto in readtxt2list(ARCHIVO1): #Points to tuple of p values = (x,y,z)
    pto = tuple([float(i) for i in punto.split(CARACTER_SEPARACION)])
    puntos.append(pto)
puntosiniciales = puntos.copy()

for tri in readtxt2list(ARCHIVO2): #Triangles to tuple of points t = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)
    triangulos.add(tuple([puntos[int(i) - 1] for i in tri.split(CARACTER_SEPARACION)]))


# with pi = (xi,yi,zi)
# Dictionary of points p: ({p,p1,p2...},{(p,p2,p3),(p,p3,p4)...})
# Dictionary with point as input, output is a tuple with the first one, the points in the neighborhood and in the second index the triangles in the neighborhood.

def areaHeron(tri):
    A = np.array(tri[0])
    B = np.array(tri[1])
    C = np.array(tri[2])
    a = np.linalg.norm(B-C)
    b = np.linalg.norm(A-C)
    c = np.linalg.norm(A-B)
    s = (a+b+c)/2
    return np.sqrt(s*(s-a)*(s-b)*(s-c))

def perimeter(tri):
    A = np.array(tri[0])
    B = np.array(tri[1])
    C = np.array(tri[2])
    a = np.linalg.norm(B-C)
    b = np.linalg.norm(A-C)
    c = np.linalg.norm(A-B)
    return(a+b+c)
 
def rInCircle(tri):
    return areaHeron(tri)/(0.5*perimeter(tri))    

def redondez(tri):
    A = np.array(tri[0])
    B = np.array(tri[1])
    C = np.array(tri[2])
    a = np.linalg.norm(B-C)
    b = np.linalg.norm(A-C)
    c = np.linalg.norm(A-B)
    ladoMax = max(a,b,c)
    return rInCircle(tri)/ladoMax

def R(punto):
    ans =0
    vecindad = vecindades [punto][1]
    tam = len(vecindad)
    for t in vecindad:
        ans += redondez(t)
    return ans/tam

def anguloD(t1, t2):
    A = np.array(t1[0])
    B = np.array(t1[1])
    C = np.array(t1[2])
    v1 = B-A
    v2 = C-A
    n1 = np.cross(v1, v2)
    
    D = np.array(t2[0])
    E = np.array(t2[1])
    F = np.array(t2[2])
    v3 = E-D
    v4 = F-D
    n2 = np.cross(v3, v4)
    ang = np.arccos(abs(np.dot(n1, n2))/(np.linalg.norm(n1)*np.linalg.norm(n2)))/100
    return ang
    
def H(punto):
    ans =0
    vecindad = vecindades [punto][1]
    for t1 in vecindad:
        for t2 in vecindad:
            a1 = set(t1)
            a2 = set(t2)
            if len(a1.intersection(a2))==2:
                ans += anguloD(t1, t2)
    return ans
    
def planpromedio(puntos):
    return op.minimize(objective, np.array([1, 1, 1, 1]), list(puntos)).x[:3]

def planpromedio2(puntos):
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

def planopromedio(puntos):
    puntoprom=np.mean(np.transpose(np.array(list(puntos))),axis=1)
    vecnorm = planpromedio2(puntos)
    ecuacion = [vecnorm[0][0],vecnorm[0][1],vecnorm[0][2], -vecnorm[0][0]*puntoprom[0]-vecnorm[0][1]*puntoprom[1]-vecnorm[0][2]*puntoprom[2]]
    return ecuacion
 

def distanciapp(ecuacion,punto):
    return abs(ecuacion[0]*punto[0]+ecuacion[1]*punto[1]+ecuacion[2]*punto[2]+ecuacion[3])/(ecuacion[0]*ecuacion[0]+ecuacion[1]*ecuacion[1]+ecuacion[2]*ecuacion[2])**0.5

def E(punto):
    vecindadAntes = vecindades[punto][0]
    vecindadDespues = vecindadAntes.copy()
    vecindadDespues.remove(punto)
    return abs(distanciapp(planopromedio(vecindadAntes),punto)-distanciapp(planopromedio(vecindadDespues),punto))

def funcionalDeCal(punto, alpha, beta, gamma):
    return alpha*E(punto)+beta*R(punto)+gamma*H(punto)
    

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



# Returns the minimal dihedral angle of the neighborhood
def minanguloD(punto):
    vecindad = vecindades[punto]
    # A list with the tuple of the adyacent triangles.
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
        tpolygon = triang(polygon)
        triaux.update(tpolygon)
        #Plot.plotmalla(list(puntosaux),triaux)
        triangulos.update(tpolygon)
        triangulos.difference_update(vec[1])
       # print("E = ", E(punto))
        #print("R = ", R(punto))
        #print("H = ", H(punto))
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
    plano = planpromedio2(polygon)
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
            planoT = np.cross(plano, p1[0]-p1[-1])      #p1[0]=i1   p1[-1]=i2
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
    global funcionalDC
    funcionalDC = []
    for punto in puntos_cent:
        funcionalDC.append((punto, funcionalDeCal(punto, 20, 5, 2)))
    funcionalDC = sorted(funcionalDC, key=itemgetter(1),reverse=True)
    for punto in noPosibles:
        for i in funcionalDC:
            if i[0] == punto:
                funcionalDC.remove(i)
listaquitar()


def quitar():
    numquitar = 100
    print("Se intentaran quitar", numquitar, "puntos", 'de', len(funcionalDC))
    nquitados = 0;
    for i in range(0,numquitar):
        print(i-len(noPosibles))
        print(nquitados)
        if nquitados%500 == 0:
            Plot.plotmalla(puntos, triangulos)
            savemesh('bunny'+str(nquitados))
        try:
            removepoint(funcionalDC[0][0])
            nquitados += 1;
        except:
            print('No fue posible quitar el punto : ',funcionalDC[0][0])


def mirarpuntos(vec):
    puntos = list(vec[0])
    triangulos = vec[1]
    Plot.plotmalla(triangulos,puntos)

#mirarpuntos(vecindades[funcionalDC[0][0]])
print(len(funcionalDC))
#mirarpuntos(vecindades[funcionalDC[0][0]])

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
