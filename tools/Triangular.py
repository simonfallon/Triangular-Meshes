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
            pto = tuple([float(i) for i in punto.split(',')])
            self.puntos.append(pto)

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
        super().__init__(file1,file2)       
        # Retorna minimo angulo dihedrales de vecindad.
    def maxAnguloD(punto):
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
       