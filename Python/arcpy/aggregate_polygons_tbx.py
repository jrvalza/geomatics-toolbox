
import os
import arcpy
import arcpy.mp as mp

arcpy.env.overwriteOutput = True

#project
aprx = mp.ArcGISProject('CURRENT')

#map
map = aprx.listMaps('Detalle')[0]

#parameters
capa_entrada = arcpy.GetParameterAsText(index=0) #first item in the toolbox script
capa_salida = arcpy.GetParameterAsText(index=1) 
distancia_buffer = arcpy.GetParameter(index=2) 
tolerancia = arcpy.GetParameter(index=3) 


#Geoprocessing
#1-)buffer
capa_intermedia = os.path.join(os.path.dirname(capa_entrada), 'remove.shp')
arcpy.Buffer_analysis(in_features = capa_entrada,
                      out_feature_class = capa_intermedia,
                      buffer_distance_or_field = distancia_buffer,
                      dissolve_option = 'ALL')

#2-)inverse buffer
arcpy.Buffer_analysis(in_features = capa_intermedia,
                      out_feature_class = capa_salida,
                      buffer_distance_or_field = distancia_buffer * -1,
                      )

#3-)generalize
arcpy.Generalize_edit(in_features = capa_salida,
                      tolerance = tolerancia
                      )

#delete temporal data
arcpy.Delete_management(in_data = capa_intermedia)

#mensaje en la toolbox
arcpy.AddMessage(f'Prcoeso terminado')
