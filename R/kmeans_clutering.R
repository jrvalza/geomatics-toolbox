
# Clustering with K-Means

library(cluster)
library("tmap")
library("sp")
library("sf")

setwd("")

# Load the data
Census.Data <-read.csv("practical_data.csv")
names(Census.Data)
head(Census.Data[,-1]) # without first column

#Coefficient of variation
cv <- function(x) sd(x) / mean(x)
sapply(Census.Data[, c("White_British", "Low_Occupancy", "Unemployed", "Qualification")], cv)

#Standardization of variables
Census.Data.st <- scale(Census.Data[,-1])
head(Census.Data.st)
summary(Census.Data.st)

#standard deviations 
c(sd(Census.Data.st[,1]),sd(Census.Data.st[,2]),sd(Census.Data.st[,3]),sd(Census.Data.st[,4]))

#************************************************************************
#**************************K-Means clustering****************************
#************************************************************************
k.means.fit <- kmeans(Census.Data.st, 3) # k = 3 

#A random set of (distinct) rows in x is chosen as the initial centres
attributes(k.means.fit)

#cluster:A vector of integers (from 1:k) indicating the cluster to which each point is allocated.
#centers:A matrix of cluster centres.
#totss:The total sum of squares.
#withinss: Vector of within-cluster sum of squares, one component per cluster.
#tot.withinss: Total within-cluster sum of squares, i.e. sum(withinss).
#betweenss: The between-cluster sum of squares, i.e. totss-tot.withinss.
#size: The number of points in each cluster.
#iter:The number of (outer) iterations.
#ifault integer: indicator of a possible algorithm problem – for experts.

# Centroids:
k.means.fit$centers

# Clusters:
k.means.fit$cluster

# Cluster size:
k.means.fit$size

# Sum of squares
k.means.fit$withinss

#Optimum number of clusters: Elbow criterion
#The percentage of variance explained is considered as a function of the number of clusters.
#If you plot the percentage of variance explained by the clusters against the number of clusters, 
#the first few clusters will explain a lot of variance, but at some point the marginal gain will decline,
#causing the curve to turn on the graph.

wssplot <- function(data, nc=15, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i)$withinss)
  }
  plot(1:nc, 
       wss, type="b",
       pch=20,
       xlab="Number of Clusters",
       ylab="Within groups sum of squares")
}

wssplot(Census.Data.st, nc=6) 

#numerical results
ws <- (nrow(Census.Data.st)-1)*sum(apply(Census.Data.st,2,var))
ws

for (i in 2:20){
  set.seed(1234)
  ws[i] <- sum(kmeans(Census.Data.st, centers=i)$withinss)
  print(ws[i])
}

#We calculate the F statistic
#If F is greater than 10, the number of groups increases from k to k+1.
for (k in 1:19){
  print( c(k, (ws[k]-ws[k+1])/(ws[k+1]/(749-k-1) )) )
}

k.means.fit <- kmeans(Census.Data.st[,c(1,2,3,4)], 3) #c(1,2,3,4)  These are the columns used for the analysis

#solution into 2 dimensions:
clusplot(Census.Data.st,
         k.means.fit$cluster,
         main= '2D representation of the Cluster solution',
         color= T,
         shade= F,
         labels= 5,
         lines= 0,
         col.p = k.means.fit$cluster,
         cex = 0.6,
         cex.txt = 0.6,
)

#************************************************************************
#**************************Hierarchical clustering:**********************
#************************************************************************

#Hierarchical methods use a distance matrix as an input for the clustering algorithm. 
#The choice of an appropriate metric will influence the shape of the clusters, as some 
#elements may be close to one another according to one distance and farther away according 

d <- dist(Census.Data.st, method = "euclidean") 

#Ward’s minimum variance criterion minimizes the total within-cluster variance.
#"Ward" Calculate the sum of the squared distances from each point in a group to the centroid of the group to be merged
#The "ward" method has been renamed to "ward.D"; note new "ward.D2"
H.fit <- hclust(d, method="ward")

#dendrogram
plot(H.fit,
     main = "Cluster Dendrogram",
     xlab = "",
     sub = "",
     labels = F,
     hang = -1
)

#add borders around the 4 clusters
rect.hclust(H.fit, k = 4, border = c("red", "blue", "green", "orange"))

#association of each record with the groupings created
hgroups <- cutree(H.fit, k=4)
table(Census.Data[,1],hgroups)

#****************************************************************
#********************Map of Clustering***************************
#****************************************************************

# Load the output area shapefiles
Output.Areas <- st_read(".", layer = "Camden_oa11")

# join our census data to the shapefile

#Kmeans groups
Census.Data.cluster <- cbind(Census.Data,k.means.fit$cluster)
names(Census.Data.cluster)[6]<-c("kmeansgroups")

#Hierarchical groups
Census.Data.cluster <- cbind(Census.Data.cluster,hgroups)
names(Census.Data.cluster)[7]<-c("hgroups")

#merge data and set CRS
OA.Census <- merge(Output.Areas, Census.Data.cluster, by.x="OA11CD", by.y="OA")
st_crs(OA.Census) <- 27700

#Spatial distribution of K-means clusters in the study area.
cluster_colors <- c("1" = "red", "2" = "blue", "3" = "green", "4" = "orange")

OA.Census$kmeansgroups <- factor(OA.Census$kmeansgroups, levels = c("1","2","3"))
OA.Census$hgroups <- factor(OA.Census$hgroups, levels = c("1","2","3","4"))

# Spatial distribution of K-means clusters
tm_shape(OA.Census) + tm_fill(fill= "kmeansgroups", 
                              fill.scale = tm_scale_categorical(values = cluster_colors[c("1","2","3")]),
                              fill_alpha = 0.6,
                              fill.legend= tm_legend(title = "K-means clusters",
                                                     title.size= 0.95,
                                                     text.size= 0.9,
                                                     position = c("left", "bottom"),
                                                     frame= T)) +
  tm_borders(alpha = .4) +
  tm_layout(frame = F)

#Spatial distribution of Hclust clusters in the study area.
tm_shape(OA.Census) + tm_fill(fill= "hgroups", 
                              fill.scale = tm_scale_categorical(values = cluster_colors[c("1","2","3","4")]),
                              fill_alpha = 0.6,
                              fill.legend= tm_legend(title = "Hierarchical clusters",
                                                     title.size= 0.95,
                                                     text.size= 0.9,
                                                     position = c("left", "bottom"),
                                                     frame= T)) +
  tm_borders(alpha = .4) +
  tm_layout(frame = F)

#export the data in excel format
#write.csv(file="practical.data.cluster.csv",Census.Data.cluster,row.names=F)

