
#****************ANOVA Analysis****************

#ANOVA: A statistical test used to determine whether there are significant differences 
#in the behavior of a quantitative variable across more than two populations.


install.packages("multcomp")
#****************

library(multcomp)

#Load data
Census.Data.cluster <-read.csv("practical.data.cluster.csv")
names(Census.Data.cluster)
unique(Census.Data.cluster$group)
head(Census.Data.cluster)

#We convert the group column to a character variable and rename the categories.
#This is necessary to perform an ANOVA and avoid confusion later on.
as.character(Census.Data.cluster$group)
Census.Data.cluster$group[Census.Data.cluster$group %in% c('1')] <- 'G1'
Census.Data.cluster$group[Census.Data.cluster$group %in% c('2')] <- 'G2'
Census.Data.cluster$group[Census.Data.cluster$group %in% c('3')] <- 'G3'
Census.Data.cluster$group[Census.Data.cluster$group %in% c('4')] <- 'G4'
head(Census.Data.cluster)

#We can visualize the data by plotting weight versus group or by using boxplots 
#per level of group

#~ means “depending on”
stripchart(Qualification ~ group, vertical = T, pch = 1, data = Census.Data.cluster)

#****Box-plots******
get_boxplot <- function(x,y,title,xlabel,ylabel){
  boxplot(x ~ y, data=Census.Data.cluster,
          main = title,
          xlab = xlabel,
          ylab = ylabel
  )
}

get_boxplot(Census.Data.cluster$Qualification, Census.Data.cluster$group,
            title= "Qualification by Cluster",
            xlabel= "Cluster",
            ylabel= "% with a Qualification" 
)

get_boxplot(Census.Data.cluster$White_British, Census.Data.cluster$group,
            title= "White_British by Cluster",
            xlabel= "Cluster",
            ylabel= "White_British" 
)

get_boxplot(Census.Data.cluster$Low_Occupancy, Census.Data.cluster$group,
            title= "Low_Occupancy by Cluster",
            xlabel= "Cluster",
            ylabel= "Low_Occupancy" 
)

get_boxplot(Census.Data.cluster$Unemployed, Census.Data.cluster$group,
            title= "Unemployed by Cluster",
            xlabel= "Cluster",
            ylabel= "Unemployed" 
)

#**********************************************************
#**********************ANOVA test**************************
#**********************************************************
#To perform an ANOVA, we choose one of the variables
means <- aggregate(Qualification ~ group,Census.Data.cluster,mean)
get_boxplot(Census.Data.cluster$Qualification, Census.Data.cluster$group,
            title= "Qualification by Cluster",
            xlabel= "Cluster",
            ylabel= "% with a Qualification" 
)

points(1:4, means$Qualification, col = "red")
text(1:4, means$Qualification - 2.0, labels = round(means$Qualification,2))

#Can we assume that all means are equal?
#To do this, we perform a hypothesis test

#fit the model
fit <- aov(Qualification ~ group, data=Census.Data.cluster)

#estimated coefficients
coef(fit) 
# (Intercept) it is the overall average, which is the average of group 1
# The other values are the alpha values—that is, the values that must be subtracted 
# from the overall mean to obtain the means for each group

#(Intercept)     groupG2     groupG3     groupG4 
#64.2412920 -23.9419588   0.5451095 -35.6529160 

residuals(fit) #each data point relative to the overall mean (intercept)

#**********************************************************
# ************We make predictions by group*****************
# ********The result will be the average of each group*****
#**********************************************************

predict(fit, newdata = data.frame(group = c("G1", "G2", "G3","G4")))

#We can change the order of groups.
predict(fit, newdata = data.frame(group = c("G2", "G1", "G3","G4")))

#***************************************************************
# We changed the overall average so that it is not the same as that of the first group
#***************************************************************

# The results refer to the differences between each group's mean and the intercept (overall mean) 
# There is no need to enter the value for Group 4 because it will be the opposite of the sum of the
# other groups' alpha values; that is, Group 4's alpha is 0

#The contrast function, contr.sum, provides orthogonal contrasts in which 
#all levels are compared to the overall mean. 
options(contrasts = c("contr.sum", "contr.poly")) 
fit2 <- aov(Qualification ~ group, data=Census.Data.cluster)
coef(fit2)

predict(fit2, newdata = data.frame(group =  c("G1", "G2", "G3","G4")))
#Note that the output of predict has not changed.
#The predicted values do not depend on the side-constraint that we employ

#**********************************************************
#********Comparison of Populations Using ANOVA*************
#**********************************************************

#*We wonder if:
#*Are the differences between the means large compared to the differences 
#*between the data points within each group?

# Hypothesis testing:
# H0: The means are equal
# H1: The means are different in at least 2 groups

summary(fit)
#residual variance = Mean Sq
# Nomenclature for p-value results
# *** extremely significant
# ** very significant
# * 99% confidence in rejecting H0
# . 95% confidence in rejecting H0
# Since the p-value (Pr(>F)) is less than 0.05, there is a significant difference between the groups.
# H0 can be rejected

drop1(fit, test = "F") #Table similar to the summary but with a different format (the summary is better) 


#*********************************************************************
#************ANOVA function used only to compare models***************
#*********************************************************************
#As the global test can also be interpreted as a test for comparing two different models,
#namely the cell means and the single means model.
#We can use the function anova to compare the two models.

## Fit single mean model:
# ANOVA without groups, everyone is in Group 1
fit.single <- aov(Qualification ~ 1, data=Census.Data.cluster) ## 1 means global mean (intercept)

## Compare with cell means model:
anova(fit.single, fit)

# This is used to calculate the R² coefficients (Multiple R-squared and Adjusted R-squared:)
# We focus on Multiple R-squared

# The overall mean is that of the first group
summary.lm(fit) # tells us whether the means are statistically significant 
confint(fit)

# The overall average is the average of the averages for each group
summary.lm(fit2)
confint(fit2)


#*********************************************************************
#**********Checking Model Assumptions (Residual Analysis)*************
#*********************************************************************

#First group
v1<-Census.Data.cluster[Census.Data.cluster$group=="G1",]

#Kolmogorov-Smirnov test
ks.test(v1$Qualification,pnorm,mean(v1$Qualification),sd(v1$Qualification))

#Histogram
hist(v1$Qualification)

#Homocesdaticity
summary(v1$Qualification)
sd(v1$Qualification)

#Second group
v1<-Census.Data.cluster[Census.Data.cluster$group=="G2",]

#Kolmogorov-Smirnov test
ks.test(v1$Qualification,pnorm,mean(v1$Qualification),sd(v1$Qualification))

#Histogram
hist(v1$Qualification)

#Homocesdaticity
summary(v1$Qualification)
sd(v1$Qualification)

#Third group
v1<-Census.Data.cluster[Census.Data.cluster$group=="G3",]

#Kolmogorov-Smirnov test
ks.test(v1$Qualification,pnorm,mean(v1$Qualification),sd(v1$Qualification))

#Histogram
hist(v1$Qualification)

#Homocesdaticity
summary(v1$Qualification)
sd(v1$Qualification)

#Fourth group
v1<-Census.Data.cluster[Census.Data.cluster$group=="G4",]

#Kolmogorov-Smirnov test
ks.test(v1$Qualification,pnorm,mean(v1$Qualification),sd(v1$Qualification))

#Histogram
hist(v1$Qualification)

#Homocesdaticity
summary(v1$Qualification)
sd(v1$Qualification)

#QQ-plot empirical quantiles (“what we see in the data”) vs. the theoretical quantiles (“what want we expect from the model”).
plot(fit, which = 2)

#plot the residuals vs. the fitted values. 
#To check whether the residuals have constant variance and whether the residuals have
#mean zero (i.e. they don’t show any deterministic pattern).
plot(fit, which = 1)


#**************************************************************************
#*******************Contrasts and Multiple Testing*************************
#**************************************************************************

#**************Groups by factor****************
#We convert the group column to a character variable to avoid the error in the glht function
Census.Data.cluster$group = as.factor(Census.Data.cluster$group)
options(contrasts = c("contr.treatment","contr.poly"))  # The default

# anova (media general = media grupo 1) 
fit <- aov(Qualification ~ group, data=Census.Data.cluster)
summary.lm(fit)

# Multiple comparisons of means with user-defined contrasts
# We take the fit, and then 
# the numbers c(1, -1/3, -1/3, -1/3) are the factors by which the group means are multiplied, with hypothesis testing in mind (they can be changed)
# H0: sum equals 0 (m1 * 1 + m2 * -1/2 + m3 * -1/3 + ...)
# H1: sum not equal to 0

# In this case, we compare the mean of Group 1 with the average of the means of the other 3 groups
fit.gh <- glht(fit, linfct = mcp(group = c(1, -1/3, -1/3,-1/3)))
summary(fit.gh) # Look at the p-value <0.05

confint(fit.gh)

#Different Contrasts
#*********Create a matrix where each *row* is a contrast*************
K <- rbind(c(1, -1/3, -1/3,-1/3), ## G1 vs. average of G2, G3 and G4
           c(1, 0, -1, 0), c(1, -1, 0,0)) ## G1 vs. G3, G1 vs. G2

fit.gh <- glht(fit, linfct = mcp(group = K))
summary(fit.gh)

## Individual p-values
summary(fit.gh, test = adjusted("none"))

#***********************************************************
#*********** Bonferroni corrected p-values *****************
#***********************************************************
#*# p-values are probabilities greater than or equal to
# Ponferroni slightly adjusts the p-value to allow for a better interpretation of the test
# Bonferroni takes into account the number of hypothesis tests performed and modifies the p-value based on that number

summary(fit.gh, test = adjusted("bonferroni"))

#Bonferroni-Holm is less conservative and uniformly more powerful than Bonferroni.
# p-value by confidence intervals
summary(fit.gh, test = adjusted("holm"))

#The Scheffé procedure controls for the search over any possible contrast.
fit.scheffe <- glht(fit, linfct = mcp(group = c(1/3, -1, 1/3, 1/3)))
summary(fit.scheffe)

#*******************************************************************************
#*********************Tukey Honest Significant Difference (HSD)*****************
#*******************************************************************************
#
#We could perform all pairwise t-tests with the function
#pairwise.t.test (it uses a pooled standard deviation estimate from all groups).
#Without correction (but pooled sd estimate)

# Comparison table of p-values for all possible comparisons without p-value adjustment
pairwise.t.test(Census.Data.cluster$Qualification, Census.Data.cluster$group, p.adjust.method = "none")

# With correction (and pooled sd estimate)
pairwise.t.test(Census.Data.cluster$Qualification, Census.Data.cluster$group, p.adjust.method = "holm")

## Tukey HSD with built-in function

#Calculate the confidence intervals for the p-values after comparing means
TukeyHSD(fit)
plot(TukeyHSD(fit)) #If zero is NOT within an interval, it means that the means are different

#Only the difference between G1 and G3 is not significant. 

## Tukey HSD with package multcomp:
fit.tukey <- glht(fit, linfct = mcp(group = "Tukey"))
summary(fit.tukey)

confint(glht(fit.tukey)) #confidence intervals
plot(confint(glht(fit.tukey)))

#Multiple comparisons with a control problem. 
#The corresponding procedure is called Dunnett procedure
fit.dunnett <- glht(fit, linfct = mcp(group = "Dunnett"))
summary(fit.dunnett)

#We get smaller p-values than with the Tukey HSD procedure because we have to correct for less tests
