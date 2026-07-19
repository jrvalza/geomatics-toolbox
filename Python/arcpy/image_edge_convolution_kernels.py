
import numpy as np
from itertools import chain

#============================Prewitt============================
#3x3
prewittV3 =np.array([[1,1,1],
           [0,0,0],
           [-1,-1,-1]])

prewittH3 =prewittV3.T*-1


#5X5
prewittV5 = np.array([[2,2,2,2,2],
           [1,1,1,1,1],
           [0,0,0,0,0],
           [-1,-1,-1,-1,-1],
           [-2,-2,-2,-2,-2]])
prewittH5 = prewittV5.T*-1


#============================Sobel============================
#3x3
sobelV3 = np.array([[1,2,1],
         [0,0,0],
         [-1,-2,-1]])

sobelH3 =sobelV3.T*-1


#5x5
sobelV5 =np.array([[1,2,3,2,1],
         [2,3,5,3,2],
         [0,0,0,0,0],
         [-2,-3,-5,-3,-2],
         [-1,-2,-3,-2,-1]])

sobelH5=sobelV5.T*-1


#============================Roberts============================
#3x3
robertsV3 = np.array([[0,0,1],
                      [0,0,0],
                      [-1,0,0]])

robertsH3 = np.rot90(robertsV3,k=1)


#5x5
robertsV5 =np.array([[0,0,0,0,0],
         [0,0,0,1,0],
         [0,0,0,0,0],
         [0,-1,0,0,0],
         [0,0,0,0,0]])

robertsH5=np.rot90(robertsV5,k=1)



print(robertsV3, '\n\n', robertsH3, '\n\n', robertsV5, '\n\n', robertsH5)


def _get_kernel_coordinates (n):
    coordinates = []
    increment = int((n-1)/2)
    for fila in range(n):
        f = fila-increment
        for colum in range(n):
            c = colum-increment
            coordinates.append((c,f))
    return coordinates

coord = _get_kernel_coordinates(3)

print(coord)
print(robertsV3)
roberts = list(chain(*robertsV3))
for idx, coords in enumerate(coord):
    print(roberts[idx], coords)
    