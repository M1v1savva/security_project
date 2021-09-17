import requests
import json
import time

with open('config_1.json') as config_file:
    config = json.load(config_file)
server_url = "http://" + config["server"]["ip"] + ":" + config["server"]["port"]

print("Registering with the server...")
message = {"id": config["id"], "password": config["password"]}
res = requests.post(server_url + "/register/", json=json.dumps(message)).json()

if "error" in res:
    print(res["error"])
    exit(0)
print("Registered successfully.")

url_nxt = res["url"]
actions = config["actions"]["steps"]
delay = int(config["actions"]["delay"])

for item in actions:
    action, value = item.split(' ')
    value = int(value)
    if action == 'DECREASE':
        value *= -1
    print("Sending value delta " + str(value) + "...")
    message = {'id': config["id"], 'delta': value}
    res = requests.post(server_url + url_nxt, json=json.dumps(message)).json()

    if "error" in res:
        print(res["error"])
        exit(0)
    print("New value set to " + str(res["new_value"]) + ".")
    print("Done.")

    time.sleep(delay)

print("Logging out...")
message = {'id': config["id"]}
res = requests.post(server_url + '/close/', json=json.dumps(message)).json()
print("Done.")
print("Client finished.")