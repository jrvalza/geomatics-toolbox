
//string and numeric variables
var str = ee.String("This is a string");
print(str);
var num = ee.Number(5);
print(num);

//adding numeric values as objects
var sum = num.add(num);
print(sum);

//creating arrays
var arr = ee.Array([[1,2,3],[4,5,6],[7,8,9]]);
print(arr);

//retrieving values from an array
print(arr.get([1,2]));
print(typeof(arr.get([1,2])));

//Creation of a confusion matrix
var confusion_matrix = ee.ConfusionMatrix(arr);
print(confusion_matrix);
var dict = ee.Dictionary({five:5, six:6});

//Creation of vector geometries
var point = ee.Geometry.Point(-0.38,39.48);
var poly = ee.Geometry.Polygon([[[-0.3803,39.4812],[-0.3746,39.4789],[-0.3842,39.4757],[-0.3803,39.4812]]]);

//Function to add geometries to the map
Map.setCenter(-0.38,39.48);
function map (geometria){
  Map.addLayer(geometria);
}
map(point)
map(poly)

/*Function map: for each input apply the function
                var result = input.map(function_name)
*/

//==========================================================================
//Feature y FeatureCollection
//==========================================================================

var feat1 = ee.Feature(poly1,{Propietario:"Mr",Referencia:"550"});
var feat2 = ee.Feature(poly2,{Propietario:"Sr",Referencia:"566"});

var ref_feat1 = feat1.get('Referencia');
print(ref_feat1);

var current_fc = ee.FeatureCollection([feat1,feat2]);

map(FAO_Frontier);

//==========================================================================
//Image and ImageCollections
//==========================================================================

//Images within a date range(AAAA-MM-DD)
var selectedIm = imCollection.filterData(startDate,stopDate);

//Images within a geometric boundary
var selectedIm = imCollection.filterBounds(geometry);

//Images based on a filter that meets a certain criterion
var selectedIm = imCollection.filter(created_filter);

//==========================================================================
//Image operations
//==========================================================================

//Pixel-level calculation for all images in a collection
var sumOfImages = imCollection.sum() //others methods product() max() min() mean() mode() median() count()

//Select the first n images from a collection
var selectedImages = imCollection.limit(n,propertyName,order)

//example of image collection operations
var S2_Bejis = S2_L2A.filterDate("2022-08-01","2022-08-10")
                  .filterBounds(Bejis)
                  .median();
print(S2_Bejis);

var vis = {"bands":["B4","B3","B2"],
           "max": 255,
           "min": 5,
           "opacity": 1};

//image visualization 
Map.addLayer(S2_Bejis, vis,"Mediana de Sentinel 2 de 1 al 10 de agosto de 2022");

//Selection of bands in image
var band = image.select(bandName)

//mask creation
var mask = image.eq(value) //others operators ( .neq, .gt, .gte, .lt, .lte)

//Apply masks to the images
var masked = image = image.updateMask(mask)

//Calculations using images (similar to Band Math)
var result = image.add(value) //others operators (.sqrt, .max, .min, .sin, .cos, ...)

/*Exercise: 
-calculating the NDVI index
-masking the image
-adding the NDVI band to the original image
-and applying a focal filter
*/

var B2 = S2_Bejis.select('B2');
var B3 = S2_Bejis.select('B3');
var B4 = S2_Bejis.select('B4');
var B8 = S2_Bejis.select('B8');

var diff_B8_B3 = B8.subtract(B3);
var suma_B4_B2 = B4.add(B2);
var rati_B8_B4 = B8.divide(B4);

var diff_B8_B4 = B8.subtract(B4);
var suma_B8_B4 = B8.add(B4);
var NDVI = diff_B8_B4.divide(suma_B8_B4);
map(NDVI);

//mask (NDVI > 0.5)
var mask_NDVI = NDVI.gt(0.5);
print(mask_NDVI);

var NDVI_masked = NDVI.updateMask(mask_NDVI);

Map.addLayer(NDVI_masked,{palette:['red','green']});

//band rename
var NDVI = NDVI.rename("NDVI");

//image crop
var clip_NDVI = NDVI.clip(Bejis);

//Add the NDVI image to the original image
var resultado = S2_Bejis.addBands(NDVI);
print(resultado);
map(clip_NDVI);
Map.setCenter(-0.70,39.91);

//Apply a 30 m radius circular focal median filter to smooth the NDVI image
var NDVI_filtered = NDVI.focalMedian(30,"circle");
map(NDVI_filtered)
