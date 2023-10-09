import matplotlib.pyplot as plt
import pandas

points = pandas.read_csv('fiber_surface.csv')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = points['X'].values
y = points['Y'].values
z = points['Z'].values


ax.scatter(x, y, z, c='r', marker='o')

plt.show()