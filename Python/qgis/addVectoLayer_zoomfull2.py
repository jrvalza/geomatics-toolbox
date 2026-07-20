
from glob import glob

path = r'O:\xxxxxxxxxxx'
paths = glob(path + '\*.shp')

#Add layer to the project
for path in paths:
    nombre = path.split('\\')[-1].split('.')[0]
    iface.addVectorLayer(path,
                        f'{nombre}',
                        'ogr'
                        )
    
#zoom extension to all layers
iface.zoomFull()
