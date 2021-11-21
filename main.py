def main():
    print("""run TriangularMesh:
[1]TriangularMeshMaxd
[2]TriangularMeshMinD
[3]TriangularMeshQF
        """)
    option=int(input())
    if option==1:import TriangularMeshMaxD;
    elif option==2:import TriangularMeshMinD;
    elif option==3:import TriangularMeshesQF;
main()