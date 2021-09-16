import requests
import json
import time

with open('config_1.json') as config_file:
    config = json.load(config_file)
server_url = "http://" + config["server"]["ip"] + ":" + config["server"]["port"]

message = {"id": config["id"], "password": config["password"]}
res = requests.post(server_url + "/register/", json=json.dumps(message)).json()
#print(dt)
#print(res)

#if res != 0:
#    print('error ' + str(res))
#    exit(0)
#print(res)

url_nxt = res["url"]
actions = config["actions"]["steps"]
delay = int(config["actions"]["delay"])

for item in actions:
    action, value = item.split(' ')
    value = int(value)
    if action == 'DECREASE':
        value *= -1
    message = {'id': config["id"], 'delta': value}
    res = requests.post(server_url + url_nxt, json=json.dumps(message)).json()

#     if res != 0:
#         print('error ' + str(res))
#         exit(0)
    time.sleep(delay)

message = {'id': config["id"]}
res = requests.post(server_url + '/close/', json=json.dumps(message)).json()