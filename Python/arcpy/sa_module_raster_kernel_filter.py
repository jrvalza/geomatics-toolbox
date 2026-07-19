
import arcpy
from arcpy.sa import *
from matplotlib import pyplot as plt

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Rasters
mde = arcpy.Raster('mde1.asc')
mde_info = mde.getRasterInfo()
mde_filtered = arcpy.Raster(mde_info)

#Draw Image
def draw_images(img):
    fig, aux = plt.subplots(1, 2)
    aux[0].imshow(img[0][0], cmap='gray')
    aux[0].set_title(img[0][1])

    aux[1].imshow(img[1][0], cmap='gray')
    aux[1].set_title(img[1][1])

    plt.show()

#Kernel
def get_kernel (n):
    if n%2 == 0:
        return 'El tamaño del kernel debe ser impar'
    else:
        kernel = []
        increment = int((n-1)/2)
        for fila in range(n):
            f = fila-increment
            for colum in range(n):
                c = colum-increment
                kernel.append((c,f))
        #return kernel
        return kernel

n= 3
kernel = get_kernel(n)

#Apply kernel to raster
with RasterCellIterator({'rasters':[mde, mde_filtered]}) as rci:
    for fila, columna in rci:
        suma = 0
        for x, y in kernel:
            suma += mde[fila+x, columna+y] 
        media = suma / (n*n)
        mde_filtered[fila, columna] = media
    
    #output
    mde_array = arcpy.RasterToNumPyArray(mde)
    mde_filter_array = arcpy.RasterToNumPyArray(mde_filtered)
    
    #Matplotlib
    draw_image = [[mde_array, 'MDE'], [mde_filter_array, f'MDE Filtered - kernel: {n}x{n}']]
    draw_images(draw_image)

print('Proceso terminado.')
