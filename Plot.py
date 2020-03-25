from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np


def plotmalla(puntos, triangulos):
    x = np.asarray(list(map(lambda punto: punto[0], puntos)))
    y = np.asarray(list(map(lambda punto: punto[1], puntos)))
    z = np.asarray(list(map(lambda punto: punto[2], puntos)))
    tri = np.asarray(list(map(lambda tri: list(list(map(lambda point: puntos.index(point), tri))), triangulos)))
    fig = plt.figure(figsize=(12.8, 9.6))
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(-x, -z, y, triangles=tri)
    plt.show()


