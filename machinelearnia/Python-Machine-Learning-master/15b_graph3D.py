import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Nécessite pip install tk

iris = load_iris()
print(iris.keys())

# exit()
x = iris.data
y = iris.target
names = list(iris.target_names)

print(f"x contient {x.shape[0]} exemples et {x.shape[1]} variables")
print(f"il y a {np.unique(y).size} classes")
y.shape, [str(n) for n in names], int(y.max())

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=y)
plt.show()
