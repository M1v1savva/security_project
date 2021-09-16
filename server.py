from flask import Flask, request, url_for
import json

app = Flask(__name__)

id_present = dict()
id_password = dict()
id_url = dict()
id_value = dict()

@app.route('/register/', methods = ['POST'])
def register():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    id = data["id"]
    password = data["password"]

    if id in id_password and id_password[id] != password:
        return {}, 401

    if id not in id_present:
        id_present[id] = 1
        id_url[id] = url_for("update")
    else:
        id_present[id] += 1
    id_password[id] = password
    id_value[id] = 0

    result = {"url": id_url[id]}
    return json.dumps(result)

@app.route('/update/', methods = ['POST'])
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    id = data["id"]
    val = data["delta"]
    id_value[id] += val
    print(id_value[id])
    result = {"response": 0}
    return json.dumps(result)

@app.route('/close/', methods = ['POST'])
def close():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    id = data["id"]
    id_present[id] -= 1
    if id_present[id] == 0:
        id_present.pop(id, None)
        id_password.pop(id, None)
        id_url.pop(id, None)
        id_value.pop(id, None)

    result = {"response": 0}
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, port=13370)