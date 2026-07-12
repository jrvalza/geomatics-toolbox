library("udunits2")
library("units")
library(tmap)
library(leaflet)
library("sp")
library("sf")
library(RColorBrewer)

#========================================================
#=======================Load data========================
#========================================================
Ethnicity <- read.csv("camden/Camden/tables/KS201EW_oa11.csv")
Rooms <- read.csv("camden/Camden/tables/KS403EW_oa11.csv")
Qualifications <-read.csv("camden/Camden/tables/KS501EW_oa11.csv")
Employment <-read.csv("camden/Camden/tables/KS601EW_oa11.csv")

View(Employment)
names(Employment)

#========================================================
#=============selecting specific columns only============
#========================================================

#Elegimos las columnas 1 y 21 de Ethnicity
Ethnicity <- Ethnicity[, c(1, 21)]
names(Ethnicity)

Rooms <- Rooms[, c(1, 13)]
names(Rooms)

Employment <- Employment[, c(1, 20)]
names(Employment)

Qualifications <- Qualifications[, c(1, 20)]
names(Qualifications)

#========================================================
#===================change column names==================
#========================================================
names(Employment)[2] <- "Unemployed"

# OA = geographic code
names(Ethnicity)<- c("OA", "White_British")
names(Rooms)<- c("OA", "Low_Occupancy")
names(Employment)<- c("OA", "Unemployed")
names(Qualifications)<- c("OA", "Qualification")

names(Qualifications)
#========================================================
#=======================Merge Files======================
#========================================================
#1 Merge Ethnicity and Rooms
merged_data_1 <- merge(Ethnicity, Rooms, by="OA")

#2 Merge the "merged_data_1" object with Employment
merged_data_2 <- merge(merged_data_1, Employment, by="OA")

#3 Merge the "merged_data_2" object with Qualifications
Census.Data <- merge(merged_data_2, Qualifications, by="OA")

#4 Remove the "merged_data" objects as we won't need them anymore
rm(merged_data_1, merged_data_2)

names(Census.Data)

#=======================================================================
# Writes the data to a csv named "practical_data" in your file directory
#=======================================================================
write.csv(Census.Data, "practical_data.csv", row.names=F)

head(Census.Data)
tail(Census.Data)

#*****************************************************************************
#========================================================
#================Descriptive statistics==================
#========================================================

#mean, median, 25th and 75th quartiles, min, max 
summary(Census.Data)

# Creates a histogram
hist(Census.Data$Unemployed)

# Creates a histogram, enters more commands about the visualisation
hist(Census.Data$Unemployed, breaks=20, col= "blue", main="% Unemployed", xlab="Percentage")

# box and whisker plots
boxplot(Census.Data[,2:5])

#******************************************************************
#========================================================
#===================Making maps in R=====================
#========================================================

# Load the output area shapefiles. Move these files to your working directory.
Output.Areas <- st_read(".", layer = "Camden_oa11")

#========================================================
#====================plots the shapefile=================
#========================================================
plot(Output.Areas)

#========================================================
#==============joins data to the shapefile===============
#========================================================
names(Output.Areas)
names(Census.Data)
OA.Census <- merge(Output.Areas, Census.Data, by.x="OA11CD", by.y="OA")

names(OA.Census)

#========================================================
# sets the coordinate system to the British National Grid
#========================================================

#British National Grid (EPSG:27700) produced by the Ordenance Survey
# see https://www.r-spatial.org/r/2020/03/17/wkt.html
st_crs(OA.Census)
st_crs(OA.Census) <- 27700
st_crs(OA.Census)

#========================================================
# Creates a simple choropleth map of our qualification variable
#========================================================
qtm(OA.Census, fill = "Qualification")

#========================================================
#=========Creating more advanced maps with tmap==========
#========================================================
tm_shape(OA.Census) + tm_fill("Qualification")

#========================================================
#===============Setting the colour palette===============
#========================================================

display.brewer.all()

# setting a colour palette
tm_shape(OA.Census) + tm_fill("Qualification", palette = "-Greens")

#========================================================
#==============Setting the colour intervals==============
#========================================================
#equal - divides the range of the variable into n parts.
#pretty - chooses a number of breaks to fit a sequence of equally spaced 'round' values. So they keys for these intervals are always tidy and memorable.
#quantile - equal number of cases in each group
#jenks - looks for natural breaks in the data
#Cat - if the variable is categorical (i.e. not continuous data)

#========================================================
#================changing the intervals==================
#========================================================
tm_shape(OA.Census) + tm_fill("Qualification", style = "quantile", palette = "Reds")

#========================================================
#===================number of levels=====================
#========================================================
tm_shape(OA.Census) + tm_fill("Qualification", style= "quantile", n= 7, palette= "-Spectral")

#========================================================
#=========includes a histogram in the legend=============
#========================================================
tm_shape(OA.Census) + tm_fill("Qualification", 
                              style = "quantile", 
                              n = 5,
                              palette = "Reds", 
                              legend.hist = T)

# add borders
tm_shape(OA.Census) + tm_fill("Qualification", palette = "Reds") +
  tm_borders(alpha=.4)

# north arrow
tm_shape(OA.Census) + 
  tm_fill("Qualification", palette = "Reds") +
  tm_borders(alpha=.1) + 
  tm_compass(type= "4star", position = c("left", "top"), size= 4)

# adds in layout, gets rid of frame
tm_shape(OA.Census) + tm_fill(fill= "Qualification", 
                              fill.scale= tm_scale_intervals(style= "quantile", n=6, values = "Blues"),
                              fill.legend= tm_legend(title = "Camden, London",
                                                     title.size= 1.1,
                                                     text.size= 0.9,
                                                     position = c("left", "bottom"),
                                                     frame= F,
                                                     reverse= T)) +
  tm_borders(alpha=.4) +
  tm_compass(type= "4star", position = c("right", "top"), size= 4) +
  tm_layout(frame = FALSE)

#========================================================
#Using the Jenks optimization method (natural breaks)
#========================================================
tm_shape(OA.Census) + tm_fill(fill= "Qualification", 
                              fill.scale= tm_scale_intervals(style= "jenks", n=6, values = "Blues"),
                              fill.legend= tm_legend(title = "Camden, London",
                                                     title.size= 1.1,
                                                     text.size= 0.9,
                                                     position = c("left", "bottom"),
                                                     frame= F,
                                                     reverse= T)) +
  tm_borders(alpha=.4) +
  tm_compass(type= "4star", position = c("left", "top"), size= 4) +
  tm_layout(frame = FALSE)

#========================================================
#=================Saving the shapefile===================
#========================================================
st_write(OA.Census, dsn = "camden/", layer = "Census_OA_Shapefile", driver = "ESRI Shapefile")



#********************************************************************
#========================================================
#================interactive maps in tmap================
#========================================================
# turns view map on
tmap_mode("view")

tm_shape(OA.Census) + tm_fill(fill= "Qualification", 
                              fill.scale= tm_scale_intervals(style= "jenks", n=6, values = "-Spectral"),
                              fill.legend= tm_legend(title = "% with a Qualification",
                                                     title.size= 1.1,
                                                     text.size= 0.9,
                                                     position = c("right", "bottom"),
                                                     frame= F,
                                                     reverse= T)) +
  tm_borders(alpha=.4)

# turns plot map on
tmap_mode("plot")
