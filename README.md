# Triangular-Meshes
This repository contains a project which consists of three variations of algorithms to reduce triangular meshes
A triangular mesh is a very common way to represent 3-Dimensional Objects in computer graphics. In this simplification 3-dimensional surfaces are reduced to a set of adjacent triangles in the 3-D Space.
It is often useful to reduce the mesh i.e. to reduce the amount of triangles that are used to represent the object without losing its geometrical and topological atributes, so that algorithms and computation procedures on this object can be faster.

All three variations of the original algorithm follow the same [Greedy-aproach](https://www.sciencedirect.com/topics/engineering/greedy-approach). We follow greedely the order given by a priority queue wich tells us which triagle´s removal would have the smallest effect on the objects form. Then repeat iteratively until a given amount of triangles are removed or until the new mesh differs from the original one within a tolerance limit, which we meassure with the Hausdorff-Distance.

### TriangularMeshMaxd.py

The first variation "TriangularMeshMaxd.py" sorts the priority queue by the maximal [Diehedral angle](https://www.sciencedirect.com/topics/chemistry/dihedral-angle) that is formed by each triangle.

### TriangularMeshMinD.py

The second variation "TriangularMeshMinD.py" follows the same logic, but it takes the minimal Diehedral angle.

### TriangularMeshQF.py

The third and most elaborated one "TriangularMeshQF" sorts the priority queue by the triangle´s Quality Functional, Which is a function that takes the triangle´s roundness (R), the curvature (H) and the local error caused by its removal (E). This function can be calibrated with three parameters fot R,H,E that depend on the type of object the mesh is representing, so that the reduction will keep its geometrical and topological atributes. 

## Run 

you can run one by one ,like:

**TriangularMeshMaxd**

	python TriangularMeshMaxd.py

**TriangularMeshMinD**

	python TriangularMeshMinD.py

**TriangularMeshQF**

	python TriangularMeshQF.py

or use main.py

	python main.py

### Screenshots
![sphere](https://github.com/jero98772/Triangular-Meshes/blob/master/docs/screenshots/1.png?raw=true)
![plane](https://github.com/jero98772/Triangular-Meshes/blob/master/docs/screenshots/2.png?raw=true)
