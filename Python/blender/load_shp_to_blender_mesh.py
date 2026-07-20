
import bpy
import shapefile

#capa previamente procesada. No multipoligono, No agujeros, ...
shp_path = r"O:\xxxxxxxx.shp"

#desplazamiento de coordenadas, porque blender centra en (0,0)
dx = -725600  #coord UTM
dy = -4372700 #coord UTM
fs = 0.01 #factor escala

#1-)lectura de shp
shp = shapefile.Reader(shp_path)

#2-)acceso a geometrías y atributos
registros = shp.shapeRecords()

#2.1-)Para cada registro
for reg in registros:
    #2.1.1-)Leer geometria
    poligono = reg.shape
    
    #Solo se procesan poligonos válidos
    if poligono:
        
        #2.1.2-)Obtener puntos del poligono
        puntos = poligono.points
        
        #2.1.2-)Generar lista de vertices
        vertices = []
        for p in puntos:
            vertices.append(((p[0]+dx)*fs, (p[1]+dy)*fs, 0))
        
        #2.1.3-)Generar índices de caras
        #orden de los vertices en las caras
        indices = range(len(vertices))
        
        #invertir índices solo si orientacion no es correcta
        indices_rev = reversed(indices)
        
        #índices de las caras
        caras = [tuple(indices_rev)]
        
        #2.1.4-)Acceso a atributos    
        atributos = reg.record.as_dict()  # Obtiene todos los atributos como diccionario
        CCAA_name = atributos["CCAA"]
        id_CCAA = atributos["id_ccaa"]
        
        #2.1.5-)Crear malla vacía
        malla = bpy.data.meshes.new(name="geom_" + CCAA_name + "_" + str(id_CCAA))
        
        #2.1.6-)Rellenar la malla con los vertices y las caras
        malla.from_pydata(vertices, [], caras)
        
        #2.1.7-)Crear el objeto
        objeto = bpy.data.objects.new("pol_" + CCAA_name + "_" + str(id_CCAA), malla)
        
        #2.1.8-)Incluir el objeto en una colección
        bpy.data.collections["CCAAs"].objects.link(objeto)
        
        #2.1.9-)Reasignar origen del objeto
        objeto.select_set(True)
        
        #origen en la geometría
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
        
        #limpiar selección
        bpy.ops.object.select_all(action="DESELECT")
             