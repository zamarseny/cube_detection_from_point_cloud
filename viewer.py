import sys

import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # registers 3D projection, not used directly
import matplotlib.pyplot as plt


def show_scatter_3d(xs, ys, zs):
    fig = plt.figure(figsize=plt.figaspect(1)*1.5)
    ax = fig.gca(projection='3d')
    ax.scatter(xs, ys, zs)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} path/to/sample.csv')
        exit()
    filename = sys.argv[1]
    data = np.genfromtxt(filename, dtype=float, delimiter=' ', skip_header=1, usecols=(0, 1, 2))
    xs, ys, zs = data.T
    show_scatter_3d(xs, ys, zs)
