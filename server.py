from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/determine_escalation/', methods = ['POST'])
def determine_escalation():
    jsondata = request.get_json()
    data = json.loads(jsondata)

    #stuff happens here that involves data to obtain a result

    result = {'escalate': True}
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)