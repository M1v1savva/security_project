from flask import Flask, session, request, jsonify
import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
auth = HTTPBasicAuth()
limiter = Limiter(app, key_func=get_remote_address)
users = dict() #id - hashed password
id_present = dict() # id - num of active sessions for id
id_value = dict() # id - id's counter

@limiter.limit("10/minute")
@auth.verify_password
def verify_password(username, password):
    # user_id = verify_auth_token(username)
    user_id = None
    if not user_id:
        if username in users and check_password_hash(users.get(username), password):
            return True
        elif username in users:
            return False
        users[username] = generate_password_hash(password)
        return True
    return True
@limiter.limit("10/minute")
@app.route('/register/')
@auth.login_required
def register():
    id = auth.current_user()
    if id in id_present:
        id_present[id] += 1
    else:
        id_present[id] = 1
        id_value[id] = 0
    return jsonify({'data': 'Hello, %s!' % auth.current_user()})


@app.route('/update/', methods = ['POST'])
@auth.login_required()
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    try:
        id = auth.current_user()
        val = int(data["delta"])
    except:
        return jsonify({"error": "invalid data sent to the server"})

    id_value[id] += val
    print("id " + id + " value = " + str(id_value[id]))
    result = {"new_value": id_value[id]}
    return json.dumps(result)

@app.route('/close/')
@auth.login_required()
def close():
    id = auth.current_user()
    id_present[id] -= 1
    if id_present[id] == 0:
        id_present.pop(id, None)
        id_value.pop(id, None)
        users.pop(id, None)
    result = {"response": 0}
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=13370)

# curl -u susan:bye -i -X GET http://127.0.0.1:13370/register/
# curl -u susan:bye -i -X POST "Content-Type: application/json" -d '{"delta":"1"}' http://127.0.0.1:13370/update/
# curl -u susan:bye -i -X GET http://127.0.0.1:13370/close/
