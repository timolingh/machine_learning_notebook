from flask import Flask, abort, jsonify, request
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage as STAP
import json

app = Flask(__name__)

@app.route('/gen_price', methods=['POST'])
def gen_price():
    data = request.get_json(force=True)

    # Write it to file - I haven't figured out a way to transfer this
    # EDIT: I did, but will keep this here JIK
    # with open('/Users/tim/cc_interview/tmp/data.json', 'w') as f:
    #     json.dump(data, f)

    # return(jsonify(results="0"))

    # The prediction can go here - interface to R via rpy2
    with open('/Users/tim/cc_interview/R/rpy_example.R', 'r') as f:
        string = "".join(f.readlines())

    # The prediction model stored in a R script
    bz = STAP(string, 'bz')
    foo = bz.iris_predict(json.dumps(data))  # 'dumps' method converts from Python dict to JSON string
    return(jsonify(results=foo[0]))          # rpy2 returns a string vector - take the first entry

    # foo = data
    # return(jsonify(results = foo))

if __name__ == '__main__':
    app.run(debug=True)



