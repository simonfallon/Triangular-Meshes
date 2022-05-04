import numpy as np
try:#si se corre desde el main
    from tools import Plot
    from tools.Tools import readtxt2list,writetxt
except:#si se corre desde triangular.py
    import Plot
    from Tools import readtxt2list,writetxt
from itertools import combinations
from operator import itemgetter
from collections import deque
import scipy.optimize as op
class Triangular():
    """
    puntos_cent = []
    puntos_irreg = []
    noPosibles = []
    puntos = []
    angdict = []
    """
    puntos_cent = deque()
    puntos_irreg = deque()
    noPosibles = deque()
    puntos = deque()
    angdict = deque()
    vecindades = {}
    triangulosquitados = set()
    triangulos = set()
    CARACTER_SEPARACION = '\t'
    def __init__(self,file1:str,file2:str):
        for punto in readtxt2list(file1):  # Puntos a tupla de valores p = (x,y,z)
            pto = tuple([float(i) for i in punto.split(self.CARACTER_SEPARACION)])
            self.puntos.append(pto)
        for tri in readtxt2list(file2):  # Triangulos a tupal de puntos t = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)
            self.triangulos.add(tuple([self.puntos[int(i) - 1] for i in tri.split(self.CARACTER_SEPARACION)]))
        self.puntosiniciales = self.puntos.copy()

    def frontera(self,punto):
        return not len(self.vecindades[punto][0]) == len(self.vecindades[punto][1]) + 1
    # no se usa irreg
    def irreg(punto):
        if len(self.vecindades[punto][0]) < len(self.vecindades[punto][1]) + 1:
            pass
            #print(punto)
        return len(self.vecindades[punto][0]) < len(self.vecindades[punto][1]) + 1
    
    def crearvecindades(self):
        self.vecindades.clear()
        for tri in self.triangulos:
            for punto in tri:
                if punto not in self.vecindades:
                    self.vecindades[punto] = (set(tri), {tri})
                else:
                    self.vecindades[punto][0].update(set(tri))
                    self.vecindades[punto][1].add(tri)
        self.puntos_cent.clear()
        self.puntos_cent.extend(list(filter(lambda punto: self.frontera(punto) == False, self.puntos)))
    
    def plotmallas(self):
        import Plot
        triangulos = set()
        list(map(lambda vec: triangulos.update(vec[1]), self.vecindades.values()))
        Plot.plotmalla(self.puntos, triangulos)

    def puntos_list():
        return list(map(lambda punto: list(self.punto), self.puntos))

    def toindexp(p):
        return self.puntos.index(p)

    def toindextri(t):
        return tuple(map(lambda p: self.puntos.index(p), t))

    def toindexvec(v):
        return (set(map(lambda p: toindexp(p), v[0])), set(map(lambda tri: toindextri(tri), v[1])))

    def tritovec(tri):
        return list(map(lambda punto: np.asarray(punto),tri))
    
    def removepoint(self,punto):
        try:
            vec = self.vecindades[punto]
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
            Plot.plotmalla(list(puntosaux), triaux)
            triaux.difference_update(vec[1])
            triaux.update(triang(polygon))
            Plot.plotmalla(list(puntosaux),triaux)
            triangulos.update(triang(polygon))
            triangulos.difference_update(vec[1])
            puntos.remove(punto)
            crearvecindades()
            listaquitar()
        except Exception as ex:
            Plot.plotmalla(list(puntosaux), triaux)
            Plot.plotmalla(list(vec[0]),vec[1])
            self.noPosibles.append(punto)
            self.listaquitar()
            #print(ex.with_traceback())
            #print('No fue posible quitar el punto : ',punto)

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
                    #print(indxs)
                    #print(ex)
                    continue
        raise Exception('No se Puede Triangular')

    def savemesh(self,folder="data/generaciones",name="copia"):
        #print(file1)
        tri = list(map(lambda tri: str(self.puntos.index(tri[0])+1)+','+str(self.puntos.index(tri[1])+1)+','+str(self.puntos.index(tri[2])+1)+'\n', self.triangulos))
        pts = list(map(lambda pt: str(pt[0])+','+str(pt[1])+','+str(pt[2])+'\n', self.puntos))
        writetxt(folder+"/Pts_"+name+".txt",pts)
        writetxt(folder+"/Tgs_"+name+".txt",tri)
        """
        se penso en tomar los nombres mediante slicing de strings, pero daba un error por self.file
        pos1=self.file1.index("/",len(self.file1)-self.file1[::-1].index("/")-1)
        pos2=self.file2.index("/",len(self.file2)-self.file2[::-1].index("/")-1) 
        """

    def quitar(self):
        numquitar = 200
        #print("Se intentaran quitar", numquitar, "puntos", 'de', len(self.angdict))
        nquitados = 0;
        for i in range(0,numquitar):
            #print(i-len(self.noPosibles))
            #print(nquitados)
            if nquitados%500 == 0:
                try:#desde el main
                    self.savemesh()
                except:#desde este archivos
                    self.savemesh(folder="../data/generaciones")
            try:
                removepoint(self.angdict[0][0])
                nquitados += 1;
            except:
                pass
                #print('No fue posible quitar el punto : ',self.angdict[0][0])
        Plot.plotmalla(self.puntos, self.triangulos)

    def mirarpuntos(vec):
        puntos = list(vec[0])
        triangulos = vec[1]
        Plot.plotmalla(triangulos,puntos)

    def hausdorff(self,pts1,pts2):
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
    def resultado(self):
        pass
        #print("La distancia Hausdorff entre la malla original y la reducida es: ",self.hausdorff(self.puntos, self.puntosiniciales))
        Plot.plotmalla(self.puntos,self.triangulos)
    def maxAnguloD(self,punto):
        vecindad = self.vecindades[punto]
        # Se crea una lista con tuplas de los triangulos adyacentes
        tri_adyacentes = list(
            filter(lambda par: len(set(par[0]).intersection(set(par[1]))) == 2, list(combinations(vecindad[1], 2))))
        maxang = 4;
        for par in tri_adyacentes:
            inter = list(set(par[0]).intersection(set(par[1])))
            vecI = np.asarray(inter[1]) - np.asarray(inter[0])
            vec1 = np.asarray(list(set(par[0]).difference(set(inter)))[0]) - np.asarray(inter[0])
            vec2 = np.asarray(list(set(par[1]).difference(set(inter)))[0]) - np.asarray(inter[0])
            plano1 = np.cross(vecI, vec1)
            plano2 = np.cross(vecI, vec2)
            ang = np.math.acos(np.dot(plano1, plano2) / (np.linalg.norm(plano1) * np.linalg.norm(plano2)))
            maxang = min(maxang, ang)
        return maxang
    def listaquitar(self):
        for punto in self.puntos_cent:
            self.angdict.append((punto, self.maxAnguloD(punto)))
        self.angdict = sorted(self.angdict, key=itemgetter(1),reverse=True)
        for punto in self.noPosibles:
            for i in self.angdict:
                if i[0] == punto:
                    self.angdict.remove(i)

class TriangularMeshMaxD(Triangular):
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2)       
    

class TriangularMeshMinD(Triangular):
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2)

class TriangularMeshesQF(Triangular):
    funcionalDC=[]
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2)

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
    def minanguloD(self,punto):
        vecindad = self.vecindades[punto]
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
    def listaquitar(self):
        for punto in self.puntos_cent:
            self.angdict.append((punto, self.minanguloD(punto)))
        self.angdict = sorted(self.angdict, key=itemgetter(1),reverse=True)
        for punto in self.noPosibles:
            for i in self.angdict:
                if i[0] == punto:
                    self.angdict.remove(i)
"""
def testingTmax():
    filepath="../data/"
    file1=filepath+"puntos/Pts_esfera.txt"
    file2=filepath+"triangulos/Tgs_esfera.txt"
    tmax=TriangularMeshMaxD(file1,file2)
    tmax.crearvecindades()
    tmax.listaquitar()
    print(len(tmax.angdict))
    tmax.quitar()
    tmax.resultado()

def testingTmin():
    filepath="../data/"
    file1=filepath+"puntos/Pts_plano.txt"
    file2=filepath+"triangulos/Tgs_plano.txt"
    tmin=TriangularMeshMinD(file1,file2)
    tmin.crearvecindades()
    tmin.listaquitar()
    print(len(tmin.angdict))
    tmin.quitar()
    tmin.resultado()

def testingTqf():
    filepath="../data/"
    file1=filepath+"puntos/Pts_plano.txt"
    file2=filepath+"triangulos/Tgs_plano.txt"
    tmQF=TriangularMeshesQF(file1,file2)
    tmQF.crearvecindades()
    tmQF.listaquitar()
    print(len(tmQF.funcionalDC))
    print(len(tmQF.angdict))
    tmQF.quitar()
    tmQF.resultado()
"""
"""
    file1=filepath+"puntos/Pts_plano.txt"
    file2=filepath+"triangulos/Tgs_plano.txt"
    
    file1=filepath+"puntos/Pts_esfera.txt"
    file2=filepath+"triangulos/Tgs_esfera.txt"

    file1=filepath+"puntos/Pts_conejo.txt"
    file2=filepath+"triangulos/Tgs_conejo.txt"
"""

#testingTmax()
#testingTmin()
#testingTqf()