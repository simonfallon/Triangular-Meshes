def main():
    print("(ascii art banner)")
    print("""run TriangularMesh:
[1]TriangularMeshMaxd of file
[2]TriangularMeshMinD of file
[3]TriangularMeshQF of file
[4]TriangularMeshMaxd of class triangular
[5]TriangularMeshMinD of class triangular
[6]TriangularMeshQF of class triangular
        """)
    option=int(input())
    if option==1:import TriangularMeshMaxD;
    elif option==2:import TriangularMeshMinD;
    elif option==3:import TriangularMeshesQF;
    elif option==4:
        from tools.Triangular import TriangularMeshMaxD
        name1=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert name1[len(name1)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            name2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert name2[len(name2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
        except AssertionError:
            filepath="data/"
            file1=filepath+"puntos/Pts_esfera.txt"
            file2=filepath+"triangulos/Tgs_esfera.txt"
            print("Se asigno los archivos por defecto")
        tmax=TriangularMeshMaxD(file1,file2)
        tmax.crearvecindades()
        tmax.listaquitar()
        print(len(tmax.angdict))
        tmax.quitar()
        tmax.resultado()
    elif option==5:
        from tools.Triangular import TriangularMeshMinD
        name=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert name[len(name)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            name2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert name2[len(name2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
        except AssertionError:
            filepath="data/"
            file1=filepath+"puntos/Pts_esfera.txt"
            file2=filepath+"triangulos/Tgs_esfera.txt"
            print("Se asigno los archivos por defecto")
        tmin=TriangularMeshMinD(file1,file2)
        tmin.crearvecindades()
        tmin.listaquitar()
        print(len(tmin.angdict))
        tmin.quitar()
        tmin.resultado()
    elif option==6:
        from tools.Triangular import TriangularMeshesQF
        name=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert name[len(name)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            name2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert name2[len(name2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
        except AssertionError:
            filepath="data/"
            file1=filepath+"puntos/Pts_esfera.txt"
            file2=filepath+"triangulos/Tgs_esfera.txt"
            print("Se asigno los archivos por defecto")
        tmQF=TriangularMeshesQF(file1,file2)
        tmQF.crearvecindades()
        tmQF.listaquitar()
        print(len(tmQF.funcionalDC))
        print(len(tmQF.angdict))
        tmQF.quitar()
        tmQF.resultado()
main()