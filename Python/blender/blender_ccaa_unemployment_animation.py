
import bpy
import shapefile

# Deseleccionar todos los objetos
bpy.ops.object.select_all(action='DESELECT')

#1-)lectura de shp
#capa previamente procesada. No multipoligono, no agujeros, ...
shp_path = r"O:\xxxxxxxx.shp"

shp = shapefile.Reader(shp_path)

#2-)acceso a geometrías y atributos
registros = shp.shapeRecords()

#3-)construcción de base de datos de la forma: {año: {comunidad: tasaParo}}
data = {}

for count, reg in enumerate(registros):
    #3.1-) lectura de registros en forma de diccionario
    reg_dict = reg.record.as_dict()
    
    #3.2-) captura de pares clave:valor primera comunidad autónoma
    if count==0:
        for key, value in reg_dict.items():
            #saltar campos que no son años
            try:
                #datos del primer registro
                año = int(key[1:])#porque en el shp cada año aparece como F1976, F1977, etc
                tasa = value
                ccaa = reg_dict["CCAA"]    
            except:
                continue
            #almacenando la información    
            if key not in data.keys():
                data[año] = {ccaa: tasa}
                
    #3.3-) almacenando los datos del resto de comunidades por año
    else:
        for key, value in reg_dict.items():
            try:
                año = int(key[1:])
                tasa = value
                ccaa = reg_dict["CCAA"]    
            except:
                continue
            data[año][ccaa]= tasa
        

#4-)Animaciones

#Init
objetos = bpy.data.objects
frame = 0

#4.1-) Configuración inicial del TimeLine
tl= bpy.data.objects["TimeLine"]
tl.location = (-321, 5000, 870)
tl.select_set(True)

#4.1.1-) animación TimeLine
def animacionTimeLine(i, frame):
    #primer año
    if i ==0:
        
    ##Inicio frame 0
        bpy.context.scene.frame_current=frame
        bpy.ops.anim.keyframe_insert_by_name(type="Location")
    ##primer año
        bpy.context.scene.frame_current=frame+5
        bpy.ops.transform.translate(value=(-3350,0,0))
        bpy.ops.anim.keyframe_insert_by_name(type="Location")
        
    #resto de años
    else:
        bpy.context.scene.frame_current=frame+5
        bpy.ops.transform.translate(value=(-2860,0,0))
        bpy.ops.anim.keyframe_insert_by_name(type="Location")
 
#4.1.2-) Para cada año
años = list(data.keys())
for i in range(0, len(años), 1):
    animacionTimeLine(i, frame) 
    frame += 5
    
#devolver al inicio el timeLine
bpy.ops.transform.translate(value=(-321, 5000, 870))
tl.select_set(False)
frame=0



#4.2-) animación Comunidades autónomas
#añadir materiales a las CCAA
materials = bpy.data.materials
materials_names = [material.name for material in materials]
for ob in objetos:
    name = ob.name
    if name.startswith("pol"):
        ob.data.materials.clear()
        for material_name in materials_names:
            if material_name.startswith("Intervalo") or material_name == "Material_inicial":
                material = bpy.data.materials.get(material_name)
                ob.data.materials.append(material)
    
def animacionCCAA(iter, frame, año, scale):
    for ob in objetos:
        name = ob.name
        if name.startswith("pol"):
            ccaaName = name.split("_")[1]
            
            #Tasa de paro
            tasaParo = float(data[año][ccaaName])
            
            #seleccion de material
            if tasaParo <= 8:
                material = 0
            if (tasaParo > 8) and (tasaParo <= 16):
                material = 1 
            if (tasaParo > 16) and (tasaParo <= 24):
                material = 2
            if (tasaParo > 24) and (tasaParo <= 32):
                material = 3
            if (tasaParo >32):
                material = 4


            if iter == 0: 
            ## Inicio frame 0
                #material y extrusion
                ob.modifiers["GeometryNodes"]["Input_2"] = 0.0
                ob.modifiers["GeometryNodes"]["Input_3"] = 0
                ob.data.update()
                #keyframe
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_2"]', frame=frame)
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_3"]', frame=frame)

                
            ##primer año 
                #material y extrusion
                ob.modifiers["GeometryNodes"]["Input_3"] = material
                ob.modifiers["GeometryNodes"]["Input_2"] = tasaParo*scale 
                ob.data.update()
                #keyframe
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_2"]', frame=frame+5)
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_3"]', frame=frame+5)
                
                
                
                print(f"iteracion:{iter}, frame: {frame}, ccaa: {name}")
            
            # resto de años
            else: 
                #material y extrusion
                ob.modifiers["GeometryNodes"]["Input_3"] = material
                ob.modifiers["GeometryNodes"]["Input_2"] = tasaParo*scale
                ob.data.update()
                #keyframe
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_2"]', frame=frame+5)
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_3"]', frame=frame+5)
                print(f"iteracion:{iter}, frame: {frame}, ccaa: {name}")
            
            #último año
            if año == 2024:
                #material y extrusion
                ob.modifiers["GeometryNodes"]["Input_3"] = material
                ob.modifiers["GeometryNodes"]["Input_2"] = tasaParo*scale
                ob.data.update()
                #keyframe
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_2"]', frame=frame+5) 
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_3"]', frame=frame+5)  
                
            ## último frame
                #material y extrusion
                ob.modifiers["GeometryNodes"]["Input_3"] = 0
                ob.modifiers["GeometryNodes"]["Input_2"] = 0.0
                ob.data.update()
                #keyframe
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_2"]', frame=frame+10)
                ob.modifiers["GeometryNodes"].keyframe_insert(data_path='["Input_3"]', frame=frame+10)  
        
  
#4.2.1-) Para cada año
años = list(data.keys())
for i in range(0, len(años), 1):
    año = años[i]
    animacionCCAA(i, frame, año, scale=50)
    #siguiente frame
    frame += 5

#resetear extrusion y material de CCAA
for ob in objetos:
    name = ob.name
    if name.startswith("pol"):
        ob.modifiers["GeometryNodes"]["Input_2"] = 0.0
        ob.modifiers["GeometryNodes"]["Input_3"] = 0
        ob.data.update()
