# Triangular-Meshes
This repository contains a project which consists of three variations of algorithms to reduce triangular meshes
A triangular mesh is a very common way to represent 3-Dimensional Objects in computer graphics. In this simplification 3-dimensional surfaces are reduced to a set of adjacent triangles in the 3-D Space.
It is often useful to reduce the mesh i.e. to reduce the amount of triangles that are used to represent the object without losing its geometrical and topological atributes, so that algorithms and computation procedures on this object can be faster.

All three variations of the original algorithm follow the same Greedy-aproach. We follow greedely the order given by a priority queue wich tells us which triagle´s removal would have the smallest effect on the objects form. Then repeat iteratively until a given amount of triangles are removed or until the new mesh differs from the original one within a tolerance limit, which we meassure with the Hausdorff-Distance.

The first variation "TriangularMeshMaxd.py" sorts the priority queue by the maximal Diehedral angle that is formed by each triangle.
The second variation "TriangularMeshMinD.py" follows the same logic, but it takes the minimal Diehedral angle.
The third and most elaborated one "TriangularMeshQF" sorts the priority queue by the triangle´s Quality Functional, Which is a function that takes the triangle´s roundness (R), the curvature (H) and the local error caused by its removal (E). This function can be calibrated with three parameters fot R,H,E that depend on the type of object the mesh is representing, so that the reduction will keep its geometrical and topological atributes. 
