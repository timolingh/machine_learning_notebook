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
fm <- as.formula("DEXfat ~ waistcirc + hipcirc + anthro3a + anthro3b + anthro4 + elbowbreadth + kneebreadth")

boost_control <- boost_control(mstop=1000)
glm0 <- glmboost(fm, data=bf, center=T, control=boost_control)
summary(glm0)
yhat <- predict(glm0, newdata=bf)

(cmp <- data.table(y=bf[, DEXfat], yhat=yhat))

cv10f <- cv(model.weights(glm0), type = "kfold")
cvm <- cvrisk(glm0, folds = cv10f, papply = mclapply)
(plot(cvm))
(mstop(cvm))

# the caret package
fitControl <- trainControl(method = "repeatedcv",  number = 10, repeats = 1)
glmGrid <- expand.grid(mstop = 1:100, prune = c("no","yes"))

set.seed(8888)
(tr.1 <- train(fm, data=bf, method="glmboost", trControl=fitControl, 
               tuneGrid=glmGrid,  metric="RMSE", center=T))
plot(tr.1)
best <- tr.1$bestTune

yhat2 <- predict(tr.1, newdata=bf)
cmp[, yhat2 := yhat2]

yhat3 <- predict(glm0[mstop(cvm)], newdata=bf)
cmp[, yhat3 := yhat3]

# DEXfat is the response var - not in the resulting matrix 
# Warning messages:
#   1: In model.matrix.default(fm, bodyfat) :
#   the response appeared on the right-hand side and was dropped
# 2: In model.matrix.default(fm, bodyfat) :
#   problem with term 2 in model.matrix: no columns are assigned

(pl <- ggplot(cmp, aes(x=yhat)) +
  geom_line(aes(y=yhat2), color='blue') +
    geom_line(aes(y=yhat3), color='red') +
    geom_abline(slope=1, intercept=0)
)

