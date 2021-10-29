from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import jsonify, Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

# curl -u susan:bye -i -X GET http://127.0.0.1:5000/api/token

app = Flask(__name__)
auth = HTTPBasicAuth()

# tokens = {
#     "secret-token-1": "john",
#     "secret-token-2": "susan"
# }
#
# app.config['SECRET_KEY'] = 'secret'
#
# def generate_auth_token(user_id, expiration=600):
#     s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
#     return s.dumps({'id': user_id})
#
# def verify_auth_token(token):
#     s = Serializer(app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except SignatureExpired:
#         return None  # valid token, but expired
#     except BadSignature:
#         return None  # invalid token
#     return data['id']

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

# @app.route('/api/token')
# @auth.login_required
# def get_auth_token():
#     user_id = auth.username
#     token = generate_auth_token(user_id)
#     return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % auth.current_user()})

@auth.verify_password
def verify_password(username, password):
    # user_id = verify_auth_token(username)
    user_id = None
    if not user_id:
        if username in users and check_password_hash(users.get(username), password):
            return True
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)