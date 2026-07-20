
#============================================================================
#==========================access to attributes==============================
#============================================================================

#project
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0] # returns a list with all layers or can be filtered by name
capa.removeSelection()

#fields names
campos = capa.fields() # QgsField object 
for campo in campos:
    print(campo.name())
print("*"*30) 

#values of the fields
registros = capa.getFeatures()

#data in FID, 'NOMBRE' and GEOMETRIA fields
field = 'NOMBRE'
print(f'Registros en el campo: {field}')
for reg in registros:
    nombre = reg.attribute(field) #access to attributes
    area = reg.geometry().area() #access to geometry
    print(f'Id: {reg.id()}, Nombre: {nombre}, Área: {area/1000000:.2f} km2')
