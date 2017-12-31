from flask import Flask, abort, jsonify, request
import json
import requests

# Predict the sepal length from all the other features
# The data to predict is here in the payload
payload = {
    "Sepal.Length":5.1,
    "Sepal.Width":3.5,
    "Petal.Length":1.4,
    "Petal.Width":0.2,
    "Species":"setosa"
}

### Might need this:  https://www.youtube.com/watch?v=s-i6nzXQF3g ###
url = 'http://localhost:5000/gen_price'

# Convert to JSON
data = json.dumps(payload)

r = requests.post(url, data=data)
print(r.json())


