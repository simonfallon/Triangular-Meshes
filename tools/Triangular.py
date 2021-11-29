class Triangular():
    puntos_cent = []
    vecindades = {}
    puntos_irreg = []
    noPosibles = []
    puntos = []
    triangulosquitados = set()
    triangulos = set()

    def __init__(self,file1:str,file2:str):
        for punto in readtxt2list(file1):  # Puntos a tupla de valores p = (x,y,z)
            #pto = tuple([float(i) for i in punto.split(',')])
            self.puntos.append([float(i) for i in punto])
            #considerar     puntos.append(punto)
        for tri in readtxt2list(file2):  # Triangulos a tupal de puntos t = ((x1,y1,z1),(x2,y2,z2),(x3,y3,z3)
            self.triangulos.add(tuple([self.puntos[int(i) - 1] for i in tri.split(',')]))
        self.puntosiniciales = puntos.copy()

    def frontera(self,punto):
        return not len(self.vecindades[punto][0]) == len(self.vecindades[punto][1]) + 1

    def irreg(punto):
        if len(self.vecindades[punto][0]) < len(self.vecindades[punto][1]) + 1:
            print(punto)
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
        self.puntos_cent.extend(list(filter(lambda punto: frontera(punto) == False, puntos)))
    
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

class TriangularMeshMaxD(Triangular):
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2,self)       
        # Retorna minimo angulo dihedrales de vecindad.
    def maxAnguloD(self,punto):
        vecindad = supervecindades[punto]
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

class TriangularMeshMinD(Triangular):
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2,self)
    def minanguloD(self,punto):
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
class TriangularMeshesQF(Triangular):
    def __init__(self,file1:str,file2:str):
        super().__init__(file1,file2,self)

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
"""
#testing
class testing():
    def __init__(self, arg):
        filepath="../data"
        file1=filepath+"triangulos/Tgs_conejo.txt"
        file2=filepath+"puntos/Pts_conejo.txt"
    def TriangularMeshMinD(self):
        t=Triangular(file1,file2)
        t
    def TriangularMeshMinD(self):
        pass
test=testing()
test.
"""
def testing():
    filepath="../data"
    file1=filepath+"triangulos/Tgs_conejo.txt"
    file2=filepath+"puntos/Pts_conejo.txt"
    t=Triangular(file1,file2)
    tmax=TriangularMeshMaxD(file1,file2)
    tmin=TriangularMeshMinD(file1,file2)
    tqf=TriangularMeshesQF(file1,file2)