from flask import Flask, request, url_for, jsonify
import json


#python client.py config_1.json

# encrypted id and password
# get rid of /update url or authentication check on each update
# port listener
# decrease or decease (config typo)
# client not working when server under dos
#

# false accusations:
# authomatic logging out is on purpose
# counters are not separate on purpose


app = Flask(__name__)

id_present = dict()
id_password = dict()
id_url = dict()
id_value = dict()

@app.route('/register/', methods = ['POST'])
def register():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    try:
        id = data["id"]
        password = data["password"]
    except:
        return jsonify({"error": "invalid data sent to the server"})

    if id in id_password and id_password[id] != password:
        return jsonify({"error": "authentification error"})

    if id not in id_present:
        id_present[id] = 1
        id_url[id] = url_for("update")
    else:
        id_present[id] += 1
    id_password[id] = password
    id_value[id] = 0

    result = {"url": id_url[id]}
    return jsonify(result)

@app.route('/update/', methods = ['POST'])
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    try:
        id = data["id"]
        val = int(data["delta"])
    except:
        return jsonify({"error": "invalid data sent to the server"})

    id_value[id] += val
    print("id " + id + " value = " + str(id_value[id]))
    result = {"new_value": id_value[id]}
    return json.dumps(result)

@app.route('/close/', methods = ['POST'])
def close():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    try:
        id = data["id"]
    except:
        return jsonify({"error": "invalid data sent to the server"})
    id_present[id] -= 1
    if id_present[id] == 0:
        id_present.pop(id, None)
        id_password.pop(id, None)
        id_url.pop(id, None)
        id_value.pop(id, None)

    result = {"response": 0}
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=13370)