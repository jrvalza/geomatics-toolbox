
//Study area geometry selection
// Variable ZonaAprox

//Filter second-level FAO administrative boundaries according to the selected study area
//Center the map on the selected FAO region

var ZonaEstudio = FAO.filterBounds(ZonaAprox); 
Map.centerObject(ZonaEstudio,12);
Map.addLayer(ZonaEstudio,{color:'#000000'},"Zona de estudio");
print("Area zona de estudio: ", ee.Number(ZonaEstudio.geometry().area()).divide(1e6).round(),"km^2");

//=========================================================================================================
//pre-flood image
//=========================================================================================================

/*Get S1 image (pixel-level median calculation) before the flood date
The 'instrumentMode' property must equal 'IW'. Hint: filter(ee.Filter.eq(property_name, property_value))
The 'orbitProperties_pass' property must equal 'DESCENDING'*/
var imagen_pre =  Sentinel1.filterDate("2017-11-01","2017-12-05")
                 .filterBounds(ZonaEstudio)
                 .filter(ee.Filter.eq('instrumentMode','IW'))
                 .filter(ee.Filter.eq('orbitProperties_pass','DESCENDING'))
                 .select(['VV','VH'])
                 .median(); 

print("imagen pre inundación", imagen_pre)

//=========================================================================================================
//post-flood image               
//=========================================================================================================

//Get S1 image (pixel-level median calculation) after the flood date
var imagen_post =  Sentinel1.filterDate("2018-03-10","2018-03-20")
                 .filterBounds(ZonaEstudio)
                 .filter(ee.Filter.eq('instrumentMode','IW'))
                 .filter(ee.Filter.eq('orbitProperties_pass','DESCENDING'))
                 .select(['VV','VH'])
                 .median(); 
print("imagen post inundación", imagen_post); 

/*Visualize VH polarization before and after the flood
-clipped to the selected FAO region. Set minimum value -25 and maximum 0 and give it a descriptive names.
*/
var imagen_pre_clip = imagen_pre.clip(ZonaEstudio);
var VH_pre = imagen_pre_clip.select("VH");
Map.addLayer(VH_pre,{min:-25, max:0},"Polariación VH, Imagen pre inundación ");

var imagen_post_clip = imagen_post.clip(ZonaEstudio);
var VH_post = imagen_post_clip.select("VH");
Map.addLayer(VH_post,{min:-25, max:0},"Polariación VH, Imagen post inundación ")

//Apply a 50m or 150m circular median filter to the pre-flood and post-flood images
var imagen_pre_median = imagen_pre_clip.focalMedian(50,"circle","meters");
var imagen_pre_median = imagen_pre_median.focalMedian(150,"circle","meters");

var imagen_post_median = imagen_post_clip.focalMedian(50,"circle","meters");
var imagen_post_median = imagen_post_median.focalMedian(150,"circle","meters");

/*Visualize filtered VH polarization clipped to the selected region for the pre-flood and post-flood images.
-Set minimum value -25 and maximum 0 and give it a descriptive name.
*/
Map.addLayer(imagen_pre_median.select("VH"),{min:-25, max:0},"Polariación VH, Imagen filtrada pre inundación ");
Map.addLayer(imagen_post_median.select("VH"),{min:-25, max:0},"Polariación VH, Imagen filtrada post inundación ");

//Combine the pre-flood filtered image and the post-flood filtered image into a new image.
var combinacion = imagen_pre_median.addBands(imagen_post_median); 

//Rename the bands to more descriptive names. 
var nuevasBandas = combinacion.rename(['VV_pre','VH_pre','VV_post','VH_post']);
print("Imagen multitemporal de 4 bandas",nuevasBandas);

//Visualize the 4-band image with different RGB band combinations (min -25, max 0)
function addRGBVis(image, bands, name){
  Map.addLayer(image, {bands: bands, min: -25, max: 0}, name);
}

addRGBVis(nuevasBandas, ['VV_post','VV_pre','VH_pre'], 'Imagen multitemporal visualización 1');
addRGBVis(nuevasBandas, ['VV_pre','VV_post','VV_post'], 'Imagen multitemporal visualización 2');
addRGBVis(nuevasBandas, ['VH_pre','VH_post','VH_post'], 'Imagen multitemporal visualización 3');

//=========================================================================================================
//MANUAL THRESHOLD
//=========================================================================================================

//Calculate the difference between the filtered post-flood image (VH polarization) and the filtered pre-flood image (VH polarization)
var VH_pre  = nuevasBandas.select('VH_pre');
var VH_post = nuevasBandas.select('VH_post'); 
var diff_VH = VH_post.subtract(VH_pre);

//Diference image visualization
function addPaletteVis(image, palette, min, max, name){
  Map.addLayer(image, {palette: palette, min: min, max: max}, name);
}

addPaletteVis(diff_VH, ['blue','white'], -15, 10, "Imagen diferencia VH");

/*Manually, using the 'Inspector' tab, identify flooded and non-flooded values in the difference image.
-Set a threshold to separate both zones.
-Create a binary image: 1 below the threshold, 0 otherwise
*/
var umbral_manual = -1.82;
var mask_manual = diff_VH.lt(umbral_manual);

//Resulting binary image
addPaletteVis(mask_manual, ['white','blue'], 0, 1, "Imagen binaria umbral manual VH");

//=========================================================================================================
//HISTOGRAM THRESHOLD
//=========================================================================================================

//Selection of geometries (samples) in flooded and non-flooded areas
//From the difference image obtained in the previous section (VH polarization), clip according to the flooded area samples
//From the difference image obtained in the previous section (VH polarization), clip according to the non-flooded area samples
//Rename the bands with a more descriptive name. For example, 'VH_Flooded' and 'VH_NotFlooded'
var diff_inun_clip = diff_VH.clip(Inundado).rename(['VH_inundado']);
print(diff_inun_clip);
Map.addLayer(diff_inun_clip);

var diff_NO_inun_clip = diff_VH.clip(NO_inundado).rename(['VH_NoInundado']);
print(diff_NO_inun_clip);
Map.addLayer(diff_NO_inun_clip);

//Combine the two resulting images (flooded and non-flooded area clips) into a single image
var combi_inun_noInun = diff_inun_clip.addBands(diff_NO_inun_clip);
print(combi_inun_noInun);
Map.addLayer(combi_inun_noInun);

//=========================================================================================================
//SUPERVISED CLASSIFICATION
//=========================================================================================================

//Select training samples. In addition to the flooded class, select general but representative classes. For example: flooded, permanent water, agriculture, vegetation, urban
/*
Classes:
        Flooded
        Agricultural
        Urban
        Permanent water
        Forest
*/

/*
From the geometries selected for the training samples, convert each of them into a feature with a new property containing the class label.
For example, the new property can be called 'landCover' and have numeric values starting at 0 for the flooded class, 1 for the permanent water class, etc.
All these features must form a featurecollection that will make up the training samples
*/
var muestras_VT = ee.FeatureCollection ( [ee.Feature(Inundado, {'landcover':0}),
                                          ee.Feature(Clase_Agua_Permanente, {'landcover':1}),
                                          ee.Feature(Clase_Urbano, {'landcover':2}),
                                          ee.Feature(Clase_Agricola, {'landcover':3}),
                                          ee.Feature(Clase_Forestal, {'landcover':4})]);
print(muestras_VT);

/*
Extract the characteristics of the combined 4-band image using the training samples featurecollection.
Use scale = 10 and tileScale = 16
sampleRegions function, and remember to indicate the featurecollection property that contains the class identifier
*/
var entrenamiento = nuevasBandas.sampleRegions({collection: muestras_VT, 
                                                scale: 10,
                                                properties: ['landcover'],
                                                tileScale: 16
                                                }); 
//print(entrenamiento); //The print contains more than 5000 elements

//Train a RandomForest model with 100 trees.
var clasificador = ee.Classifier.smileRandomForest(100).train(entrenamiento, 'landcover'); 

//Apply the trained model to the combined 4-band image
var clasificacion = nuevasBandas.classify(clasificador); 
addPaletteVis(clasificacion, ['cyan','blue','gray','yellow','green'], 0, 4, "Imagen de la clasificación supervisada");
print("Imagen clasificacion", clasificacion)

//From the classified image, generate a binary image where value 1 corresponds to the class set as flooded, and 0 for the rest.
var imagen_Binaria_Supervisada = clasificacion.eq(0);

//Visualize the resulting binary image
addPaletteVis(imagen_Binaria_Supervisada, ['white','blue'], 0, 1, "Imagen binaria de la clasificación supervisada");


////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////EVALUATION///////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////

//Select evaluation samples. These must be samples of both the flooded and non-flooded classes.

/*
Following the same process used for the training samples, the evaluation samples (geometry) need to be converted to features, which then form a featurecollection.
The main difference is that there will only be two classes: flooded and non-flooded. The feature corresponding to flooded must have a class property value of 1, and non-flooded a value of 0.
This is because these evaluation samples will be compared against a binary image whose values are 1 for flooded areas and 0 for non-flooded areas.
*/
var muestras_EV = ee.FeatureCollection ( [ee.Feature(EV_Inundado, {'landcover':1}),
                                          ee.Feature(EV_No_Inundado, {'landcover':0})]);

//=========================================================================================================
//MANUAL THRESHOLD
//=========================================================================================================

/*
Extract the characteristics of the binary image obtained via manual threshold and of the evaluation samples featurecollection
Use scale = 10 and tileScale = 16
*/
var Evauacion_Umbral_Manual = mask_manual.sampleRegions({collection: muestras_EV, 
                                                scale: 10,
                                                properties: ['landcover'],
                                                tileScale: 16
                                                }); 
//Generate the confusion matrix
var matriz_Confus_Manual =  Evauacion_Umbral_Manual.errorMatrix('landcover','VH_post'); 
print("Matriz de consfusion Umbral Manual", matriz_Confus_Manual); 

//Show overall accuracy, user's and producer's accuracy, and the kappa index
 var fiabilidad_Global_M = matriz_Confus_Manual.accuracy(); 
 var fiablidad_Productor_M = matriz_Confus_Manual.producersAccuracy(); 
 var fiablidad_usuario_M = matriz_Confus_Manual.consumersAccuracy();
 var indice_kappa_M = matriz_Confus_Manual.kappa(); 

print("fiabilidad global", fiabilidad_Global_M); 
print("fiabilidad de productor", fiablidad_Productor_M);
print("fiabilidad usuario", fiablidad_usuario_M);
print("indice Kappa", indice_kappa_M);

// Matrix order
/// //     0  ///  1
//0 //  77182      53
//1//   595        6622 

//=========================================================================================================
//SUPERVISED CLASSIFICATION
//=========================================================================================================

//Extract the characteristics of the binary image obtained via supervised classification and of the evaluation samples featurecollection
var Evauacion_Umbral_Supervisado = imagen_Binaria_Supervisada.sampleRegions({collection: muestras_EV, 
                                                scale: 10,
                                                properties: ['landcover'],
                                                tileScale: 16
                                                }); 

//Generate the confusion matrix
var matriz_Confus_Suprevisado =  Evauacion_Umbral_Supervisado.errorMatrix('landcover','classification'); 
print("Matriz de confusion clasificacion supervisada", matriz_Confus_Suprevisado); 

//Show overall accuracy, user's and producer's accuracy, and the kappa index
var fiabilidad_Global_S = matriz_Confus_Suprevisado.accuracy(); 
 var fiablidad_Productor_S = matriz_Confus_Suprevisado.producersAccuracy(); 
 var fiablidad_usuario_S = matriz_Confus_Suprevisado.consumersAccuracy();
 var indice_kappa_S = matriz_Confus_Suprevisado.kappa(); 
 
print("fiabilidad global", fiabilidad_Global_S); 
print("fiabilidad de productor",fiablidad_Productor_S);
print("fiabilidad de usuario",fiablidad_usuario_S);
print("indice Kappa",indice_kappa_S);

///////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////FLOODED AREA CALCULATION///////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

/*
Calculate the area identified as flooded from the binary image obtained via manual threshold
Hint: generate an image whose pixel value is its area (ee.Image.pixelArea()) and apply a mask to filter only the flooded areas (updateMask).
This result can be divided by 10000 to work in hectare units.
Apply reduceRegion to this result, where only the pixels identified as flooded remain, each with a value equal to its own area in hectares,
to sum all these values (see Reducer sum) that fall within the selected FAO region.
Other values to use: scale = 30 and maxPixels = 1e13.

The result obtained is a dictionary, from which the area value can be extracted using .getNumber('area')
*/
var pixel_Area = ee.Image.pixelArea();
var pixel_Area_Inundada = pixel_Area.updateMask(mask_manual).divide(1e4);
var area_Inundada_Manual = pixel_Area_Inundada.reduceRegion({reducer: ee.Reducer.sum(), 
                                                geometry: ZonaEstudio,
                                                scale: 30,
                                                maxPixels: 1e13}).getNumber('area'); 
                                                
print("area inundada umbral manual", area_Inundada_Manual);

//Same process but to calculate the area identified as flooded from the binary image obtained via supervised classification
var pixel_Area_Inundada_supervisada = pixel_Area.updateMask(imagen_Binaria_Supervisada).divide(1e4);
var area_Inundada_supervisada = pixel_Area_Inundada_supervisada.reduceRegion({reducer: ee.Reducer.sum(), 
                                                geometry: ZonaEstudio,
                                                scale: 30,
                                                maxPixels: 1e13}).getNumber('area'); 
                                                
print("area inundada supervisada", area_Inundada_supervisada);


///////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////EXPORT/////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

Export.image.toDrive({
  image: VH_pre,
  description: 'Polarizacion VH pre inundación',
  region: ZonaEstudio,
  scale: 100
});

Export.image.toDrive({
  image: VH_post,
  description: 'Polarizacion VH post inundacion',
  region: ZonaEstudio,
  scale: 100
})

Export.image.toDrive({
  image: imagen_pre_median,
  description: 'Polarizacion VH pre inundación filtrada',
  region: ZonaEstudio,
  scale: 100
})

Export.image.toDrive({
  image: clasificacion,
  description: 'Imagen tematica - Clasificacion supervisada',
  region: ZonaEstudio,
  scale: 100
})

Export.image.toDrive({
  image: mask_manual,
  description: 'Mascara umbral manual',
  region: ZonaEstudio,
  scale: 100
});

Export.image.toDrive({
  image: nuevasBandas,
  description: 'imagen multitemporal',
  region: ZonaEstudio,
  scale: 100
});

Export.image.toDrive({
  image: imagen_Binaria_Supervisada,
  description: 'imagen binaria supervisada',
  region: ZonaEstudio,
  scale: 100
});

//MADAGASCAR - STUDY AREA
var madagascar = FAO.filterBounds(madagascar);
print("Regiones FAO: ", madagascar.getDownloadURL("kml"))

//Exporting the geometries
print("Zona de estudio: ", ZonaEstudio.getDownloadURL("kml"))
print("muestras_VT: ", muestras_VT.getDownloadURL("kml"))
print("muestras_EV: ", muestras_EV.getDownloadURL("kml"))
