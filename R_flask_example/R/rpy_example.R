setwd("~/cc_interview/")
library(jsonlite)

bz <- function(input) {
    # Simple test function
  
    # Note do not need to convert to JSON - Will do it Python 
    return(input)
    
}

iris_predict <- function(input) {
  
  # Model
  iris_mdl <- readRDS('/Users/tim/cc_interview/models/iris_mdl.RData')
  
  # convert to dataframe
  newdata <- fromJSON(input)
  
  # prediction
  yhat <- predict(iris_mdl, newdata=newdata)
  
  return(yhat)

}
