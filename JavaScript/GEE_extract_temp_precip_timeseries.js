
//Loading plots
Map.addLayer(parcelas, undefined, "PARCELAS");

//Two-week periods for year 2023
var quincenas = [
  { inicio: '2023-01-01', fin: '2023-01-16', etiqueta: 'A_ENE1' },
  { inicio: '2023-01-15', fin: '2023-02-01', etiqueta: 'B_ENE2' },
  
  { inicio: '2023-02-01', fin: '2023-02-16', etiqueta: 'C_FEB1' },
  { inicio: '2023-02-15', fin: '2023-03-01', etiqueta: 'D_FEB2' },
  
  { inicio: '2023-03-01', fin: '2023-03-16', etiqueta: 'E_MAR1' },
  { inicio: '2023-03-15', fin: '2023-04-01', etiqueta: 'F_MAR2' },
  
  { inicio: '2023-04-01', fin: '2023-04-16', etiqueta: 'G_ABR1' },
  { inicio: '2023-04-15', fin: '2023-05-01', etiqueta: 'H_ABR2' },
  
  { inicio: '2023-05-01', fin: '2023-05-16', etiqueta: 'I_MAY1' },
  { inicio: '2023-05-15', fin: '2023-06-01', etiqueta: 'J_MAY2' },
  
  { inicio: '2023-06-01', fin: '2023-06-16', etiqueta: 'K_JUN1' },
  { inicio: '2023-06-15', fin: '2023-07-01', etiqueta: 'L_JUN2' },
  
  { inicio: '2023-07-01', fin: '2023-07-16', etiqueta: 'M_JUL1' },
  { inicio: '2023-07-15', fin: '2023-08-01', etiqueta: 'N_JUL2' },
  
  { inicio: '2023-08-01', fin: '2023-08-16', etiqueta: 'O_AGO1' },
  { inicio: '2023-08-15', fin: '2023-09-01', etiqueta: 'P_AGO2' },
  
  { inicio: '2023-09-01', fin: '2023-09-16', etiqueta: 'Q_SEP1' },
  { inicio: '2023-09-15', fin: '2023-10-01', etiqueta: 'R_SEP2' },
  
  { inicio: '2023-10-01', fin: '2023-10-16', etiqueta: 'S_OCT1' },
  { inicio: '2023-10-15', fin: '2023-11-01', etiqueta: 'T_OCT2' },
  
  { inicio: '2023-11-01', fin: '2023-11-16', etiqueta: 'U_NOV1' },
  { inicio: '2023-11-15', fin: '2023-12-01', etiqueta: 'V_NOV2' },
  
  { inicio: '2023-12-01', fin: '2023-12-16', etiqueta: 'W_DIC1' },
  { inicio: '2023-12-15', fin: '2024-01-01', etiqueta: 'X_DIC2' }
];

//Precipitation collection
var precipitacion2023 = []

//Temperature collection
var temperatura2023 = []

for (var i = 0; i < quincenas.length; i++) {
  //start date, end date, and label
  var inicio = quincenas[i].inicio;
  var fin = quincenas[i].fin;
  var etiqueta = quincenas[i].etiqueta;

  //Calculation of average precipitation for the two-week period i
  var precipitacion = precipitacionCol.filterDate(inicio, fin).select('precipitation');
  var precipitacionMedia = precipitacion.mean().rename(etiqueta + '_pre');
  precipitacion2023.push(precipitacionMedia);
  
  //Maximum temperature (in the layer 0–7 cm deep) for the two-week period i
  var temperatura = temperaturaCol.filterDate(inicio, fin).select('soil_temperature_level_1');
  var temperaturaMaxima = temperatura.max().rename(etiqueta + '_temp');
  temperatura2023.push(temperaturaMaxima);
}

//data series
var precipitacionSerie = ee.Image.cat(precipitacion2023);
print(precipitacionSerie);
Map.addLayer(precipitacionSerie, undefined, "serie temporal precipitacion");

var temperaturaSerieCelsius = ee.Image.cat(temperatura2023).subtract(273.15);
print(temperaturaSerieCelsius);
Map.addLayer(temperaturaSerieCelsius, undefined, "serie temporal temperatura ºC");

//Calculation of precipitation and average temperature for each plot
function stats (feature){
  var precipitacionStats = precipitacionSerie.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: feature.geometry(),
    maxPixels: 10000000000,
    scale: 10,
    bestEffort: true
  });
  
  var temperaturaStats = temperaturaSerieCelsius.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: feature.geometry(),
    maxPixels: 10000000000,
    scale: 10,
    bestEffort: true
  });
  
  return feature.set(precipitacionStats).set(temperaturaStats);
}

var parcelasStats = parcelas.map(stats);
Map.addLayer(parcelasStats, undefined, "Parcelas-con-estadisticas");

//export results to Google Drive
Export.table.toDrive(parcelasStats,'parcelasStats');
