
//Loading plots
Map.addLayer(parcelas, undefined, "PARCELAS");

//Two-week periods for year 2020
var quincenas = [
  { inicio: '2020-01-01', fin: '2020-01-16', etiqueta: 'A_ENE1' },
  { inicio: '2020-01-15', fin: '2020-02-01', etiqueta: 'B_ENE2' },
  
  { inicio: '2020-02-01', fin: '2020-02-16', etiqueta: 'C_FEB1' },
  { inicio: '2020-02-15', fin: '2020-03-01', etiqueta: 'D_FEB2' },
  
  { inicio: '2020-03-01', fin: '2020-03-16', etiqueta: 'E_MAR1' },
  { inicio: '2020-03-15', fin: '2020-04-01', etiqueta: 'F_MAR2' },
  
  { inicio: '2020-04-01', fin: '2020-04-16', etiqueta: 'G_ABR1' },
  { inicio: '2020-04-15', fin: '2020-05-01', etiqueta: 'H_ABR2' },
  
  { inicio: '2020-05-01', fin: '2020-05-16', etiqueta: 'I_MAY1' },
  { inicio: '2020-05-15', fin: '2020-06-01', etiqueta: 'J_MAY2' },
  
  { inicio: '2020-06-01', fin: '2020-06-16', etiqueta: 'K_JUN1' },
  { inicio: '2020-06-15', fin: '2020-07-01', etiqueta: 'L_JUN2' },
  
  { inicio: '2020-07-01', fin: '2020-07-16', etiqueta: 'M_JUL1' },
  { inicio: '2020-07-15', fin: '2020-08-01', etiqueta: 'N_JUL2' },
  
  { inicio: '2020-08-01', fin: '2020-08-16', etiqueta: 'O_AGO1' },
  { inicio: '2020-08-15', fin: '2020-09-01', etiqueta: 'P_AGO2' },
  
  { inicio: '2020-09-01', fin: '2020-09-16', etiqueta: 'Q_SEP1' },
  { inicio: '2020-09-15', fin: '2020-10-01', etiqueta: 'R_SEP2' },
  
  { inicio: '2020-10-01', fin: '2020-10-16', etiqueta: 'S_OCT1' },
  { inicio: '2020-10-15', fin: '2020-11-01', etiqueta: 'T_OCT2' },
  
  { inicio: '2020-11-01', fin: '2020-11-16', etiqueta: 'U_NOV1' },
  { inicio: '2020-11-15', fin: '2020-12-01', etiqueta: 'V_NOV2' },
  
  { inicio: '2020-12-01', fin: '2020-12-16', etiqueta: 'W_DIC1' },
  { inicio: '2020-12-15', fin: '2021-01-01', etiqueta: 'X_DIC2' }
];

//Function for calculating the NDVI index
function CalcularNDVI(imagen){
  var bandas_seleccionadas = imagen.select('B4','B8');
  var NDVI = bandas_seleccionadas.normalizedDifference(['B8','B4']).rename('NDVI');
  return NDVI;
}

//NDVI colection
var NDVI2020 = []

for (var i = 0; i < quincenas.length; i++) {
  //start date, end date, and label
  var inicio = quincenas[i].inicio;
  var fin = quincenas[i].fin;
  var etiqueta = quincenas[i].etiqueta;

  //NDVI index calculation for the two-week period i
  var coleccionSentinelFil = sentinelCol.filterBounds(zonaestudio).filterDate(inicio, fin);
  var ColeccionNDVI= coleccionSentinelFil.map(CalcularNDVI);
  var NDVImax = ColeccionNDVI.max().rename(etiqueta + '_NDVI');
  NDVI2020.push(NDVImax);
}

//data series
var NDVISerie = ee.Image.cat(NDVI2020);
Map.addLayer(NDVISerie, undefined, "serie temporal NDVI_2020");

//Calculation of the average NDVI for each plot
function stats (feature){
  var NDVIStats = NDVISerie.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: feature.geometry(),
    maxPixels: 10000000000,
    scale: 10,
    bestEffort: true
  });
  return feature.set(NDVIStats);
}

var parcelasStats = parcelas.map(stats);
Map.addLayer(parcelasStats, undefined, "Parcelas-con-estadisticas");

//export results to Google Drive
Export.table.toDrive(parcelasStats,'parcelasStats');
