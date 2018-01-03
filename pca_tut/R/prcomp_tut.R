rm(list=ls())

library(mboost)
library(caret)
library(data.table)
library(doMC)
library(ggplot2)

## Register parallel backend
registerDoMC(cores = 4)

data("bodyfat", package="TH.data")
bodyfat <- data.table(bodyfat)

bf <- bodyfat[, .(DEXfat, waistcirc, hipcirc, anthro3a, anthro3b, anthro4, elbowbreadth, kneebreadth)]
pairs(bf)

bf_pca <- prcomp(bf, scale=T)
plot(bf_pca)
plot(bf_pca, type="line")
biplot(bf_pca)

(bf_pca$center)
(bf_pca$scale)

(bf_pca$rotation)
(bf_pca$rotation[, 1:2])



