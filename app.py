# Sahar Massachi for Sanders Campaign
# Style: camelCase for functions, underscore_case for variables

from flask import Flask, json
import helper

app = Flask(__name__)

# Gets a listing of available calls
@app.route("/available")
def available():
	slots = helper.getAvailableSlots()
	for slot in slots:
	    del slot[helper.ARROWTIME]
	#raise
	return json.dumps(slots)


@app.route('/')
def hello():
	#return json.jsonify(helper.getAvailableSlots())
	return "yo"
	#return "Hello World!"

if __name__ == '__main__':
	helper.setup()
	print("gc")
	print(helper.gc)
	app.run(debug=True)
	


