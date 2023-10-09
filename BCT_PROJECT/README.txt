INSTRUCTIONS TO RUN THE CODE:

1. To install libraries required to compile the code, execute the following commands on the terminal
    a. ast, csv and math are standard Python libraries, you don't need to install them separately.
    b. for matplotlib, shapely, pandas, and sympy, execute "python3 -m pip install LIBRARY_NAME".
    
2. Now run the main source code file, fiber_surface.py using "python3 finer_surface.py".

3. You will first be asked to input the range of the three coordinates (x, y, z) which will basically be the dimensions for the mesh. Enter in the following format, [start, end].

4. Next you will be asked to input the length of a cubic cell in the mesh (with this the mesh will be divided into smaller cubes).

5. Then you need to input the number of points in the fiber surface control polygon (FSCP). (If FSCP is a line enter 2, if it is a polygon, enter number of sides of the polygon).
    a. If you choose the FSCP to be a line, input the two endpoints of the line in the format, [x, y] (where x and y correspond to the x-coordinate and the y-coordinate)
    b. If you choose the FSCP to be a polygon, one by one enter the x and y coordinate as asked by the program.
    
6. Hereafter, the calculation of points of the biber surface takes place.

7. Once the execution is complete, run the file plot_3d.py using the command "python3 plot_3d.py".

8. You can now see the points on the fiber surfaces plotted in a 3-dimensional domain. 

************************************************************************************************************************************************************************************************************

NOTE: We have implemented a simple function in the source code, f(x, y, z) = (x, y). In order to change the function, follow the steps given below,
    1. In the file fiber_surface.py, line number 51 and 52 correspond to the bivariate function values which can be changed.
    
    2. row['X'], row['Y'], row['Z'] correspond to the x-coordinate, y-coordinate and z-coordinate respectively. Using these variables custom values for the two values in range (h1, h2) can be made.


To verify the results of the code, following can be done:
1. A separating line in the range of the function, forms a separating surface in the domain of the function.

2. So for a grid, [0,10]x[0,10]x[0,10] a separating line (FSCP) should have endpoints [0,0] and [10,10] (given the function is f(x, y, z) = (x, y))

3. In the resulting plot of fiber surface we can see a surfaces separating the domain into two parts can be seen.


The test case for the above mentioned case will be,
	Enter the range of x coordinate in the mesh : [0,10]
	Enter the range of y coordinate in the mesh : [0,10]
	Enter the range of z coordinate in the mesh : [0,10]
	Enter the length of cell in the mesh : 1
	Enter number of points of FSCP: 2
	Enter coordinates for the first point : [0,0]
	Enter coordinates for the second point : [10,10]
	
*Since the computation of points of the fiver surface is heavy, choose the input that you give for the mesh and length of cell wisely. (For computation of a mesh with 1000 cubes it takes apporximately 2 minutes)
