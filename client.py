import requests
import json
import time
import sys

def exit_connection(config):
    print("Logging out...")
    message = {'id': config["id"]}
    res = requests.post(server_url + '/close/', json=json.dumps(message)).json()
    print("Done.")
    print("Client finished.")
    exit(0)

filename = sys.argv[1]

with open(filename) as config_file:
    config = json.load(config_file)
server_url = "http://" + config["server"]["ip"] + ":" + config["server"]["port"]

print("Registering with the server...")
message = {"id": config["id"], "password": config["password"]}
res = requests.post(server_url + "/register/", json=json.dumps(message)).json()

if "error" in res:
    print(res["error"])
    exit_connection(config)
print("Registered successfully.")

url_nxt = res["url"]
actions = config["actions"]["steps"]
delay = int(config["actions"]["delay"])

for item in actions:
    action, value = item.split(' ')
    value = int(value)
    if action == 'DECREASE':
        value *= -1
    elif action == 'INCREASE':
        value *= 1
    else:
        print('error: invalid action value in json')
        continue

    print("Sending value delta " + str(value) + "...")
    message = {'id': config["id"], 'delta': value}
    res = requests.post(server_url + url_nxt, json=json.dumps(message)).json()

    if "error" in res:
        print(res["error"])
        exit_connection(config)
    print("New value set to " + str(res["new_value"]) + ".")
    print("Done.")

    time.sleep(delay)

exit_connection(config)