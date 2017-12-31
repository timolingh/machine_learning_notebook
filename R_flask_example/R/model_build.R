setwd("~/cc_interview/")
library(jsonlite)

data(iris)

# Convert to JSON
iris_js <- toJSON(iris)
print(iris_js)

# Save the JSON file
# Comment out - this doesn't quite get the format that I want
# write_json(iris_js, "./data/iris.json")

# convert to dataframe
iris_df <- fromJSON(iris_js, simplifyDataFrame=T)

# regression model
iris_mdl <- lm(Sepal.Length ~ Sepal.Width + Petal.Length + Petal.Width, data = iris_df)
summary(iris_mdl)

# The prediction with the model object
yhat <- predict(iris_mdl, newdata=iris)

# Save the model
saveRDS(iris_mdl, file="./models/iris_mdl.RData")

