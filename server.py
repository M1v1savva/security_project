from flask import Flask, session, request, jsonify
import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
auth = HTTPBasicAuth()
limiter = Limiter(app, key_func=get_remote_address)
users = dict() #id - hashed password
id_present = dict() # id - num of active sessions for id
id_value = dict() # id - id's counter
id_last = dict() #id - last used time (session timeout monitor)

def clean_sessions():
    print('cleaning sessions')
    to_delete = []
    for id in id_last:
        interval = time.time() - id_last[id]
        if interval > 10 * 60:
            to_delete.append(id)
    print('sessions to be terminated:')
    print(to_delete)
    for id in to_delete:
        users.pop(id, None)
        id_present.pop(id, None)
        id_value.pop(id, None)
        id_last.pop(id, None)

scheduler = BackgroundScheduler()
scheduler.add_job(func=clean_sessions, trigger="interval", seconds=60 * 10)
scheduler.start()

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
    id_last[id] = time.time()
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
    id = auth.current_user()
    if id not in id_present:
        return jsonify({"error": "invalid data sent to the server"})
    id_last[id] = time.time()
    try:
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
    if id not in id_present:
        return jsonify({"error": "invalid data sent to the server"})
    id_last[id] = time.time()
    id_present[id] -= 1
    if id_present[id] == 0:
        id_present.pop(id, None)
        id_value.pop(id, None)
        users.pop(id, None)
    result = {"response": 0}
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=13370)

atexit.register(lambda: scheduler.shutdown())

# curl -u susan:bye -i -X GET http://127.0.0.1:13370/register/
# curl -u susan:bye -i -X POST "Content-Type: application/json" -d '{"delta":"1"}' http://127.0.0.1:13370/update/
# curl -u susan:bye -i -X GET http://127.0.0.1:13370/close/
