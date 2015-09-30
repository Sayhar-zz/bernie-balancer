# Sahar Massachi for Sanders Campaign
# Style: camelCase for functions, underscore_case for variables

from flask import Flask, json
import helper

app = Flask(__name__)


# Gets a listing of available calls
@app.route("/available")
def available():
	slots = {
		1: {"date": "10/1/2015", "time": "11:00 AM", "host":"sam"},
		2: {"date": "10/1/2015", "time": "7:00 PM", "host":"Albert"}
	}
	return json.jsonify(slots)


@app.route('/')
def hello():
    return json.jsonify(helper.getMaster())
    #return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)

