# Triangular-Meshes en español

Una malla triangular es una forma muy común de representar objetos 3d en computacion grafica. En esta simplificación, las superficies 3D se reducen a un conjunto de triángulos adyacentes en el espacio tridimensional.

A menudo es útil reducir la malla, es decir, reducir la cantidad de triángulos que se utilizan para representar el objeto sin perder sus atributos geométricos y topológicos, de modo que los algoritmos y procedimientos de cálculo sobre este objeto puedan ser más rápidos.

Las tres variaciones del algoritmo original siguen el mismo enfoque ["Greedy-aproach"](https://www.sciencedirect.com/topics/engineering/greedy-approach). Seguimos greedely el orden dado por una cola de prioridad que nos dice que la eliminación de triángulos tendría el menor efecto en la forma de los objetos. 

Luego se repite iterativamente hasta que se elimina una cantidad determinada de triángulos o hasta que la nueva malla difiere de la original dentro de un límite de tolerancia, que medimos con la distancia de Hausdorff.

### TriangularMeshMaxd.py

La primera variación "TriangularMeshMaxd.py" ordena la cola de prioridades por el [angulo diedro](https://www.sciencedirect.com/topics/chemistry/dihedral-angle) máximo que forma cada triángulo.

### TriangularMeshMinD.py

La segunda variación "TriangularMeshMinD.py" sigue la misma lógica, pero toma el mínimo ángulo diedro.

### TriangularMeshQF.py

La tercera y más elaborada "TriangularMeshQF" ordena la cola de prioridades por la Función de Calidad del triángulo, que es una función que toma la redondez del triángulo (R), la curvatura (H) y el error local causado por su eliminación (E). Esta función puede calibrarse con tres parámetros R,H,E que dependen del tipo de objeto que representa la malla, para que la reducción mantenga sus atributos geométricos y topológicos. 

## Ejecutar 

puede correr uno por uno, de la siguiente forma:

**TriangularMeshMaxd**

	python TriangularMeshMaxd.py

**TriangularMeshMinD**

	python TriangularMeshMinD.py

**TriangularMeshQF**

	python TriangularMeshQF.py

o use main.py

	python main.py
