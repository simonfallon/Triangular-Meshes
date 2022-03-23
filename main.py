import time
def main():
    print("""
                          @@@@
                         @@@@
                      #@@@@@@
              #######    @@@@
          ######      ###  #   
    ########        ####   #  
@@@@##            ###      #   
@@@@#            ##       #   
@@  ####    @@@@@@        #   
 #      ####@@@@          #    
# #         @@@@          #    
# #        @@@@          #    
#  #       #   #        #     
#  ##      #    ##      #     
#   #     #       #    #      
#    #   #        ## #        
#    #  #           @@@       
#     @@           @@@@       
#     @@@    #######@@@@       
 #    @@@@####     @@@@       
 #    @@          ## #        
 #   #         ##             
 #   #       ##               
 #  #     ###                 
 #      ###                   
 # #   ##                     
 #    #                       
 @@ @@                        
 @@@@                          
 @@   
  _____     _                         _            
|_   _| __(_) __ _ _ __   __ _ _   _| | __ _ _ __ 
  | || '__| |/ _` | '_ \ / _` | | | | |/ _` | '__|
  | || |  | | (_| | | | | (_| | |_| | | (_| | |   
  |_||_|  |_|\__,_|_| |_|\__, |\__,_|_|\__,_|_|   
                         |___/                    
                     _               
 _ __ ___   ___  ___| |__   ___  ___ 
| '_ ` _ \ / _ \/ __| '_ \ / _ \/ __|
| | | | | |  __/\__ \ | | |  __/\__ \
|_| |_| |_|\___||___/_| |_|\___||___/

        """)
    print("""run TriangularMesh:
[1]TriangularMeshMaxd of file
[2]TriangularMeshMinD of file
[3]TriangularMeshQF of file
[4]TriangularMeshMaxd of class triangular
[5]TriangularMeshMinD of class triangular
[6]TriangularMeshQF of class triangular
        """)
    option=int(input())
    s=time.time()
    if option==1:import TriangularMeshMaxD;
    elif option==2:import TriangularMeshMinD;
    elif option==3:import TriangularMeshesQF;
    elif option==4:
        from tools.Triangular import TriangularMeshMaxD
        file1=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert file1[len(file1)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            file2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert file2[len(file2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
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
        file1=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert file1[len(file1)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            file2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert file2[len(file2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
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
        file1=input('Entre archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
        try:
            assert file1[len(file1)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
            file2=input('Entre el segundo archivo a triangular (archivo por defecto="data/puntos/Pts_esfera.txt" y "data/puntos/Tgs_esfera.txt")')
            assert file2[len(file2)-4:],"el archivo a ingresar debe ser de texto, termina en .txt"
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
    end=time.time()
    print("  "*50,"\n",end-s,"\n","  "*50)
def tests():
    filepath="data/"
    """

    file1=filepath+"puntos/Pts_plano.txt"
    file2=filepath+"triangulos/Tgs_plano.txt"
    
    file1=filepath+"puntos/Pts_esfera.txt"
    file2=filepath+"triangulos/Tgs_esfera.txt"
    """
    file1=filepath+"puntos/Pts_conejo.txt"
    file2=filepath+"triangulos/Tgs_conejo.txt"

    s1=time.time()
    from tools.Triangular import TriangularMeshMaxD
    tmax=TriangularMeshMaxD(file1,file2)
    tmax.crearvecindades()
    tmax.listaquitar()
    #print(len(tmax.angdict))
    tmax.quitar()
    tmax.resultado()
    end1=time.time()

    s2=time.time()
    from tools.Triangular import TriangularMeshMinD
    tmin=TriangularMeshMinD(file1,file2)
    tmin.crearvecindades()
    tmin.listaquitar()
    #print(len(tmin.angdict))
    tmin.quitar()
    tmin.resultado()
    end2=time.time()

    s3=time.time()
    from tools.Triangular import TriangularMeshesQF
    tmQF=TriangularMeshesQF(file1,file2)
    tmQF.crearvecindades()
    tmQF.listaquitar()
    #print(len(tmQF.funcionalDC))
    #print(len(tmQF.angdict))
    tmQF.quitar()
    tmQF.resultado()
    end3=time.time()

    print("  "*50,"\n",end1-s1,"\n","  "*50)
    print("  "*50,"\n",end2-s2,"\n","  "*50)
    print("  "*50,"\n",end3-s3,"\n","  "*50)
    print(end1-s1,",",end2-s2,",",end3-s3)

#tests()
main()