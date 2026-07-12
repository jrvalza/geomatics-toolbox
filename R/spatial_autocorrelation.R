
#Measuring Spatial Autocorrelation in R

install.packages("spdep")
install.packages("leafem")
install.packages("tmaptools")
install.packages("sf")
install.packages("stars")
install.packages("udunits2")
install.packages("units")
install.packages("tmap",type = "source")
install.packages("leaflet")
install.packages("dismo")

#****************************************
library("sp")
library("udunits2")
library("units")
library(tmap)
library(leaflet)
library(spdep)
library(sf)

# Load the data
Census.Data <-read.csv("practical_data.csv")

# Load the output area shapefiles
Output.Areas <- st_read(".", layer = "Camden_oa11")

# join our census data to the shapefile
OA.Census <- merge(Output.Areas, Census.Data, by.x="OA11CD", by.y="OA")

#spatial distribution across our study area.
tm_shape(OA.Census) + 
  tm_fill(
    fill = "Qualification", 
    fill.scale = tm_scale_intervals(style = "quantile", n=7, values = "Reds"),
    fill.legend = tm_legend(title = "% with a Qualification", reverse= T)) +
  tm_borders(alpha = 0.4) +
  tm_layout(frame = FALSE)

tm_shape(OA.Census) + 
  tm_fill(
    fill = "Qualification", 
    fill.scale = tm_scale_intervals(style = "quantile", n=5, values = "-Spectral"),
    fill.legend = tm_legend(title = "% with a Qualification", reverse= T)) +
  tm_borders(alpha = 0.4) +
  tm_layout(frame = FALSE)

plot(OA.Census, border = 'lightgrey', lwd = 0.3)

#===========================================================================
#=============================Calculate neighbours==========================
#===========================================================================
#Queen's criterion: Spatial units that share an edge and/or a vertex are considered neighbors.

neighbours <- poly2nb(OA.Census)
neighbours

centroids <- st_coordinates(st_centroid(st_geometry(OA.Census)))

plot(st_geometry(OA.Census), border = 'lightgrey', lwd = 0.3)
plot(neighbours, centroids, add = TRUE, col = 'blue')

#===========================================================================
#====================Calculate the Rook's case neighbours===================
#===========================================================================

#Tower criterion: Neighbors are those that share an edge (vertices are excluded)
#Opción queen: if TRUE, a single shared boundary point meets the contiguity 
#condition, if FALSE, more than one shared point is required; note that more 
#than one shared boundary point does not necessarily mean a shared boundary line

neighbours2 <- poly2nb(OA.Census, queen = F)
neighbours2

# compares different types of neighbours
plot(st_geometry(OA.Census), border= 'lightgrey', lwd = 0.3, main="Neighborhood connections", cex.main= 1.1)
plot(neighbours, centroids, add= TRUE, col = 'green', lwd= 0.1, pch= 2, cex= 0.5)
plot(neighbours2, centroids, add= TRUE, col='red', lwd= 0.1, pch= 2, cex= 0.5)
legend("right", 
       legend = c("Queen's criterion", "Tower criterion"), 
       col = c("green", "red"), 
       lwd = 1, 
       pch = 2,
       cex = 0.8,
       bty = "n")
#===========================================================================
#===============Convert the neighbour data to a listw object================
#===========================================================================
listw <- nb2listw(neighbours) # construction of a binary spatial weight matrix

#The function may return the error “Error in nb2listw(filename): Empty neighbor sets found.”
#This is because you have some regions that have NO neighbors.
#This is most likely due to digitization errors in the GIS data that need to be corrected in the GIS, or:
  #     –You can use the k-nearest neighbors method
  #     –You can add: zero.policy=T to the nb2listw call
  #     > nb2listw(sids_nbq, zero.policy=T)
listw

#Binary weight matrix: “0” if they are not neighbors and “1” if they are neighbors.
#Row standardization: Each element of the matrix is divided by the sum of
#the weights in each row. Therefore, the sum of the weights in each row equals one.
# B is the basic binary coding; W is row-standardized.
#S0 is the sum of the weights.

#**************************************************************
#===========================================================================
#=================Running a GLOBAL spatial autocorrelation==================
#===========================================================================

#Moran’s test. This will create a correlation score
#between -1 and 1. Much like a correlation coefficient, 1 determines perfect postive spatial autocorrelation
#(so our data is clustered), 0 identifies the data is randomly distributed and -1 represents negative spatial
#autocorrelation (so dissimilar values are next to each other).
# global spatial autocorrelation

moran.test(OA.Census$Qualification, listw)

#The Moran I statistic is 0.54, we can therefore determine that there our 
#qualification variable is positively autocorrelated. 
#In other words, the data does spatially cluster. 
#We can also consider the p-value as a measure of the statistical significance 
#of the model.

#===========================================================================
#===========================creates a moran plot============================
#===========================================================================
#It basically explores the relationship between the data and their neighbours as
#a scatter plot. Style="W” weights are row standardised
moran <- moran.plot(OA.Census$Qualification, listw = nb2listw(neighbours2, style = "W"))

#*****************************************************************************

#===========================================================================
#===================Running a LOCAL spatial autocorrelation=================
#===========================================================================
# creates a local moran output
local <- localmoran(x = OA.Census$Qualification,
                    listw = nb2listw(neighbours, style = "W")) #'W: row-standardized - B: binary weighting'

head(local) # I local, media, varianza, p-valor

#===========================================================================
#======================Map of LOCAL spatial autocorrelation=================
#===========================================================================

#A positive value of Ii indicates that the unit is surrounded by units with similar values.

moran.map <- cbind(OA.Census, local)
moran.map

# maps the results
tm_shape(moran.map) + 
  tm_fill(
    fill = "Ii", 
    fill.scale = tm_scale_intervals(style = "quantile"),
    fill.legend = tm_legend(title = "Local moran statistic", reverse= T)
  ) +
  tm_borders(alpha = 0) +
  tm_layout(frame = FALSE)

#From the map it is possible to observe the variations in autocorrelation across 
#space. We can interpret that there seems to be a geographic pattern to the autocorrelation. 

#A positive value indicates the presence of a spatial cluster of similar values (high or low) around the plot.
#Values with the highest absolute values are those that contribute most to the overall value of Moran's I.

#===========================================================================
#=========================To create LISA cluster map========================
#===========================================================================
#Let's create a numeric vector with a length equal to the number of rows (data)
quadrant <- vector(mode="numeric",length=nrow(local))
quadrant

# centers the variable of interest around its mean
#We subtract the mean value of the corresponding column from each data point
m.qualification <- OA.Census$Qualification - mean(OA.Census$Qualification)
m.qualification

# centers the local Moran's around the mean
#We subtract the mean value of the Local Moran's I from each Local Moran's I
m.local <- local[,1] - mean(local[,1])
m.local <- local[,1] - 0
mean(m.local)

# significance threshold
signif <- 0.05

# builds a data quadrant
quadrant[m.qualification >0 & m.local>0] <- 4 # Variable High surrounded by high
quadrant[m.qualification <0 & m.local>0] <- 1 # Variable low surrounded by low
quadrant[m.qualification <0 & m.local<0] <- 2 # Variable low surrounded by high
quadrant[m.qualification >0 & m.local<0] <- 3 # Variable high surrounded by low
quadrant[local[,5]>signif] <- 0 # “I moran” is not statistically significant

# plot
colors <- c("white",rgb(0,0,1,alpha=0.8),"lightblue",rgb(1,0,0,alpha=0.3),"red")

OA.Census$quadrant_label <- factor(
  quadrant,
  levels = 0:4,
  labels = c("insignificant", "low-low", "low-high", "high-low", "high-high")
)

tm_shape(OA.Census) + 
  tm_fill(
    fill= "quadrant_label",
    fill.scale= tm_scale_categorical(values= colors),
    fill.legend= tm_legend(title= "LISA cluster", reverse= T)) +
  tm_borders(alpha = 0.2) +
  tm_layout(frame = FALSE) 

OA.Census$quadrant_label <- NULL

#It is apparent that there is a statistically significant geographic pattern to the clustering of our qualification
#variable in Camden.

#******************************************************************************

#===========================================================================
#===============================Gi Getis-Ord================================
#===========================================================================

#Hot-spot analysis. 
#The Getis-Ord Gi Statistic looks at neighbours within a defined proximity to identify where either high or
#low values cluster spatially. Here statistically significant hot-spots are recognised as areas of high values
#where other areas within a neighbourhood range also share high values too.

#New set of neighbours.for Getis-Ord we are defining neighbours based on proximity.

# creates centroid and joins neighbours within 0 and 800 units
nb <- dnearneigh(centroids,0,900)

# creates listw
nb_lw <- nb2listw(nb, style = 'B') # Binary

#Now the criterion is based on the distance between the centroids, not on the edges of the polygons.

# plot the data and neighbours
plot(st_geometry(OA.Census), border= 'lightgrey', lwd = 0.3)
plot(nb, centroids, add= TRUE, col='red', lwd= 0.1, pch= 2, cex= 0.3)

#Some areas do not have any defined nearest neighbours so we will need to Expand search radius. e.g. 900

# compute Getis-Ord Gi statistic
local_g <- localG(OA.Census$Qualification, nb_lw)
local_g <- cbind(OA.Census, as.matrix(local_g)) #join data
names(OA.Census)
names(local_g)
names(local_g)[6] <- "gstat"
names(local_g)

# map the results
tm_shape(local_g) + 
  tm_fill(
    fill = "gstat", 
    fill.scale = tm_scale_intervals(style = "pretty", values = "-RdBu"),
    fill.legend = tm_legend(title = "Gi* z-score", reverse= T)) +
  tm_borders(alpha = .4) +
  tm_layout(frame = FALSE)

#The Gi Statistic is represented as a Z-score.
#Greater values represent a greater intensity of clustering and the direction (positive or negative)
#indicates high or low clusters.

#The final map should indicate the location of hot-spots across Study area.
tm_shape(local_g) + 
  tm_fill(
    fill = "gstat", 
    fill.scale = tm_scale_intervals(style = "quantile", n=5, values = "-RdBu"),
    fill.legend = tm_legend(title = "Gi* z-score", reverse= T)
  ) +
  tm_borders(alpha = .4) +
  tm_layout(frame = FALSE)

tm_shape(local_g) + 
  tm_fill(
    fill = "gstat", 
    fill.scale = tm_scale_intervals(style = "equal", n=7, values = "-RdBu"),
    fill.legend = tm_legend(title = "Gi* z-score", reverse= T)
  ) +
  tm_borders(alpha = .4) +
  tm_layout(frame = FALSE)

