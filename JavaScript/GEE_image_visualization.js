
//Image: Landsat 5 TM RAW

//Select image from Landsat 5 TM RAW collection
var L5 = ee.ImageCollection("LANDSAT/LT05/C01/T1").
filterMetadata("CLOUD_COVER", "less_than", 20).
filterMetadata("WRS_PATH","equals",3).
filterMetadata("WRS_ROW","equals",69).
filterDate("2005-01-01","2010-01-01")
print(L5)

//Select one image
var img = ee.Image("LANDSAT/LT05/C01/T1/LT05_003069_20050716")
print(img)

//Landsat Symbology
var viz = {"bands":["B5","B4","B3"],
           "gamma": 1,
           "max": 100,
           "min": 5,
           "opacity": 1}

//Visualize image
Map.addLayer(img, viz,"Landsat 5")
