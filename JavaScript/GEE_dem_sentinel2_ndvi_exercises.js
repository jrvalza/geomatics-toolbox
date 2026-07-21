
//DEM visualization
print(srtm);
//(data, visualization parameters, name of the layer)
Map.addLayer(srtm,
            {min: 0, max: 300, palette: ['blue', 'yellow', 'red']},
            "MDE nasa"); 

//Hillshade calculation and visualization
var sombreado = ee.Terrain.hillshade(srtm);
Map.addLayer(sombreado, {min: 150, max:255}, 'Sombreado');

//============================================================================
//Image collection
//============================================================================

//Images from November, only in time zone 30
var coleccionSentinelFil=sentinelColl.filterBounds(zonaestudio).filterDate('2024-11-01','2024-11-20').filterMetadata('MGRS_TILE','equals','30SXJ');
print(coleccionSentinelFil);
Map.addLayer(coleccionSentinelFil, undefined, 'Colección sentinel');

//Image with less cloudiness
var coleccionSentinelFilOrd = coleccionSentinelFil.sort ('CLOUDY_PIXEL_PERCENTAGE');
var imagenS2= coleccionSentinelFilOrd.first();
print(imagenS2);
Map.addLayer(imagenS2, undefined, 'imagenS2');

//============================================================================
//Image operations
//============================================================================

//Exercise - NDVI index calculation (b8-b4)/(b8+b4)
var NDVI1 = imagenS2.normalizedDifference(['B8','B4']).rename("NDVI1");
print(NDVI1);
Map.addLayer(NDVI1, undefined,'NDVI1');

//other method to calculate NDVI using the expression function
var NDVI2 = imagenS2.expression('float(nir-red)/float(nir+red)',{'nir':imagenS2.select('B8'), 'red':imagenS2.select('B4')});
print(NDVI2);
Map.addLayer(NDVI2,undefined,'NDVI2');

//Exercise - NDVI calculation for a collection of images
function CalcularNDVI(imagen){
  var bandas_seleccionadas = imagen.select('B4','B8');
  var NDVI = bandas_seleccionadas.normalizedDifference(['B8','B4']).rename('NDVI');
  return NDVI;
}
// applying the function to the entire image collection
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);
print(ColeccionNDVI);
Map.addLayer(NDVI2,undefined,'Colección NDVI');

//Exercise - reduction/summary of images (mean, median, ...)
//in NDVI it is common to work with the maximum, due to the presence of clouds
var NDVImax = ColeccionNDVI.max();
print(NDVImax);
