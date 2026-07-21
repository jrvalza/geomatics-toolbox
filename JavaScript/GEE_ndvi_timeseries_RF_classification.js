
//Crop classification using biweekly NDVI time series and Random Forest in Google Earth Engine

//Training and evaluation samples
Map.addLayer(table, undefined, "PARCELAS");

//NDVI time series
//rice: peak between June and July
//bare soil: minimum NDVI values throughout the year
//citrus: sustained NDVI values throughout the year

//1. Calculate NDVI collection
function CalcularNDVI(imagen){
  var bandas_seleccionadas = imagen.select('B4','B8');
  var NDVI = bandas_seleccionadas.normalizedDifference(['B8','B4']).rename('NDVI');
  return NDVI;
}

// PERIOD 1________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-01-01','2023-01-16');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax1 = ColeccionNDVI.max().rename('A_NDVI_ENE1');
print(NDVImax1);
Map.addLayer(NDVImax1, undefined, 'NDVI_ENE_1');

// PERIOD 2________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-01-15','2023-02-01');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax2 = ColeccionNDVI.max().rename('B_NDVI_ENE2');
print(NDVImax2);
Map.addLayer(NDVImax2, undefined, 'NDVI_ENE_2');

// PERIOD 3________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-02-01','2023-02-16');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax3 = ColeccionNDVI.max().rename('C_NDVI_FEB1');
print(NDVImax3);
Map.addLayer(NDVImax3, undefined, 'NDVI_FEB_1');

// PERIOD 4________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-02-15','2023-03-01');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax4 = ColeccionNDVI.max().rename('D_NDVI_FEB2');
print(NDVImax4);
Map.addLayer(NDVImax4, undefined, 'NDVI_FEB_2');

// PERIOD 5________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-03-01','2023-03-16');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax5 = ColeccionNDVI.max().rename('E_NDVI_MAR1');
print(NDVImax5);
Map.addLayer(NDVImax5, undefined, 'NDVI_MAR_1');

// PERIOD 6________________________
//Images and NDVI
var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate('2023-03-15','2023-04-01');
var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);

//Maximum NDVI value
var NDVImax6 = ColeccionNDVI.max().rename('F_NDVI_MAR2');
print(NDVImax6);
Map.addLayer(NDVImax6, undefined, 'NDVI_MAR_2');

// PERIOD 7________________________
// PERIOD 8________________________
// PERIOD 9________________________
// PERIOD 10________________________

//Merge images into a single image
var NDVI2023 = ee.Image.cat(NDVImax1, NDVImax2, NDVImax3, NDVImax4, NDVImax5, NDVImax6);

//Calculate mean NDVI for each plot
function stats (feature){
  return feature.set(NDVI2023.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: feature.geometry(),
    maxPixels: 10000000000,
    scale: 10,
    bestEffort: true
  }))
}

var parcelasStats = table.map(stats);
Map.addLayer(parcelasStats, undefined, "Parcelas con estadisticas");

//Random Forest classification
var train = parcelasStats.filter(ee.Filter.lt('TRSAMPLE',99));
print(train);

//attributes (features) used for classification
var listacarac = ['A_NDVI_ENE1', 'B_NDVI_ENE2', 'C_NDVI_FEB1', 'D_NDVI_FEB2', 'E_NDVI_MAR1', 'F_NDVI_MAR2'];

//classifier
var clasificador = ee.Classifier.smileRandomForest(100).train(train, 'TRSAMPLE', listacarac);

//classification
var parcelasclasificadas= parcelasStats.classify(clasificador,'CLASE_ASIGNADA');
print('parcelasclasificadas', parcelasclasificadas);
Map.addLayer(parcelasclasificadas, undefined,'PARCELAS CLASIFICADAS');

//export results to Google Drive
Export.table.toDrive(parcelasclasificadas,'parcelasclas');

//Classification accuracy assessment
var test = parcelasclasificadas.filter(ee.Filter.lt('EVSAMPLE',99));
var matrizconfusion = test.errorMatrix('EVSAMPLE','CLASE_ASIGNADA');

var fiabilidadglobal=matrizconfusion.accuracy();
var indiceKappa= matrizconfusion.kappa();
var fiabilidadesproductor= matrizconfusion.producersAccuracy();
var fiabilidadesusuario= matrizconfusion.consumersAccuracy();

print('Matriz de confusión', matrizconfusion);
print ('Fiabilidad Global',fiabilidadglobal);
print ('Índice Kappa',indiceKappa);
print ('Fiabilidades de productor', fiabilidadesproductor);
print('Fiabilidades de ususario', fiabilidadesusuario);
