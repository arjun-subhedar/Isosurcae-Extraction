import sympy
from shapely.geometry import Point, Polygon, LineString
import math  
import ast
import csv
import pandas as pd

def decimal_range(start, stop, increment):
    while start <= stop: 
        yield start
        start += increment

def equidistant_points (start, end, length):
    test_list = [start + x * (end - start)/length for x in range(length)]
    return test_list
 

def sort_counterclockwise(points):
  centre_x, centre_y = sum([x for x,_ in points])/len(points), sum([y for _,y in points])/len(points)
  angles = [math.atan2(y - centre_y, x - centre_x) for x,y in points]
  counterclockwise_indices = sorted(range(len(points)), key=lambda i: angles[i])
  counterclockwise_points = [points[i] for i in counterclockwise_indices]
  return counterclockwise_points

lookup_table = pd.read_csv("lookup_table.csv")


x_range = eval(input("Enter the range of x coordinate in the mesh : "))
y_range = eval(input("Enter the range of y coordinate in the mesh : "))
z_range = eval(input("Enter the range of z coordinate in the mesh : "))

resolution = float(input("Enter the length of cell in the mesh : "))

count_vertex = 0
with open('grid.csv', 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['X', 'Y', 'Z', 'visited', 'colour'])
    for i in decimal_range(x_range[0], x_range[1], resolution):
      for j in decimal_range(y_range[0], y_range[1], resolution):
          for k in decimal_range(z_range[0], z_range[1], resolution):
            count_vertex += 1
            vertex = [round(i, 1), round(j, 1), round(k, 1), False, -1]
            csvwriter.writerow(vertex)

grid = pd.read_csv('grid.csv')

with open('function.csv', 'w') as csvfile:
  csvwriter = csv.writer(csvfile) 
  csvwriter.writerow(['X', 'Y', 'Z', 'H1', 'H2'])
  for index, row in grid.iterrows():
    h1 = row['X']
    h2 = row['Y']
    csvwriter.writerow([row['X'], row['Y'], row['Z'], h1, h2])

function = pd.read_csv('function.csv')

pointsarray = []
n_polygon = int(input("Enter number of points of FSCP: "))
if n_polygon == 1:
    x = int(input("Enter x coordinate of the point : "))
    y = int(input("Enter y coordinate of the point : "))
    polygon = Point(x, y)
    sympy_polygon = sympy.Point2D(x, y)
elif n_polygon == 2:
    x = eval(input("Enter coordinates for the first point : "))
    y = eval(input("Enter coordinates for the second point : "))
    polygon = LineString([Point(x[0], x[1]), Point(y[0], y[1])])
    sympy_polygon = sympy.Line(x, y)
elif n_polygon > 2:
    for i in range (n_polygon):
        x = int(input("Enter x coordinate of the point : "))
        y = int(input("Enter y coordinate of the point : "))
        pointsarray.append([x, y])
    coords = sort_counterclockwise(pointsarray)
    polygon = Polygon(coords)
    sympy_polygon = sympy.Polygon(*coords)

resolution = round(resolution, 1)

with open('mesh.csv', 'w') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(['Cell Number', 'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7'])
  count_cell = 0
  c_i = -1
  c_j = -1
  c_k = -1
  for i in decimal_range(x_range[0], x_range[1]-resolution, resolution):
      c_i += 1
      for j in decimal_range(y_range[0], y_range[1]-resolution, resolution):
          c_j += 1
          for k in decimal_range(z_range[0], z_range[1]-resolution, resolution):
              c_k += 1
              count_cell = count_cell + 1
              i = round(i, 1)
              j = round(j, 1)
              k = round(k, 1)
              csvwriter.writerow([count_cell, [i, j, k, c_i, c_j, c_k], [round(i+resolution,1), j, k, c_i+1, c_j, c_k], [round(i+resolution,1), j, round(k+resolution, 1), c_i+1, c_j, c_k+1], [i, j, round(k+resolution,1), c_i, c_j, c_k+1], [i, round(j+resolution, 1), k, c_i, c_j+1, c_k], [round(i+resolution, 1), round(j+resolution, 1), k, c_i+1, c_j+1, c_k], [round(i+resolution, 1), round(j+resolution, 1), round(k+resolution, 1), c_i+1, c_j+1, c_k+1], [i, round(j+resolution, 1), round(k+resolution, 1), c_i, c_j+1, c_k+1]])
          c_k = -1
      c_j = -1


mesh = pd.read_csv('mesh.csv')

cube_map = {
    "0" : [0,1],
    "1" : [1,2],
    "2" : [2,3],
    "3" : [3,0],
    "4" : [4,5],
    "5" : [5,6],
    "6" : [6,7],
    "7" : [7,4],
    "8" : [4,0],
    "9" : [5,1],
    "10" : [6,2],
    "11" : [7,3]
}

f_fibersurface = open('fiber_surface.csv', 'w')
csvwriter = csv.writer(f_fibersurface) 
csvwriter.writerow(['X', 'Y', 'Z'])

n = (x_range[1] - x_range[0])/resolution
n = int(n)

for index, row in mesh.iterrows():
  cell = row
  binary_string = ""
  for i in range (1, len(cell)):
    vertex = ast.literal_eval(cell[i])
    index = vertex[3]*((n+1)**2) + vertex[4]*(n+1) + vertex[5]
    grid_entry = grid.iloc[index]
    if grid_entry[3] == False:
      function_entry = function.iloc[index]
      h1 = function_entry[3]
      h2 = function_entry[4]
      if polygon.contains(Point(h1, h2)) is True:
        binary_string += "1"
        grid.loc[index, 'colour'] = 1
        grid.loc[index, 'visited'] = True
      else:
        binary_string += "0"
        grid.loc[index, 'colour'] = 0
        grid.loc[index, 'visited'] = True
    else:
      if grid_entry[4] == 1:
        binary_string += "1"
      else:
        binary_string += "0"
    grid.to_csv("grid.csv", index=False)
  number = int(binary_string, 2)
  m = lookup_table.iloc[number]
  mc_case = [m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15]]
  triangles = []
  if mc_case != [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]:
    i = 0
    while i < len(mc_case):
        if mc_case[i] != -1:
            triangles.append([mc_case[i], mc_case[i+1], mc_case[i+2]])
            if i+3 < len(mc_case):
                i = i + 3
        else:
            i = i + 1
  count = 0   
  for t in triangles:
    count += 1
    for edge in t:
      endpoints_indices = cube_map.get(str(edge))
      u = ast.literal_eval(cell[endpoints_indices[0]+1])
      v = ast.literal_eval(cell[endpoints_indices[1]+1])
      index_u = ((n+1)**2)*u[3] + (n+1)*u[4] + u[5]
      index_v = ((n+1)**2)*v[3] + (n+1)*v[4] + v[5]
      
      segment_uv = sympy.Segment([function.iloc[index_u][3], function.iloc[index_u][4]], [function.iloc[index_v][3], function.iloc[index_v][4]])
      isIntersection = sympy_polygon.intersection(segment_uv)
      for i in isIntersection: 
        if isinstance(i, sympy.Segment2D) is False:
          r = math.dist([function.iloc[index_u][3], function.iloc[index_u][4]], i)/math.dist([function.iloc[index_u][3], function.iloc[index_u][4]], [function.iloc[index_v][3], function.iloc[index_v][4]])
          e = []
          for i in range (3):
            e.append(r*v[i] + (1-r)*u[i])
          csvwriter.writerow(e)
f_fibersurface.close()