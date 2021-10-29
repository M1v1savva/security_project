import requests
import json
import time
import sys

filename = None
try:
    filename = sys.argv[1]
except:
    filename = "config_1.json"

with open(filename) as config_file:
    config = json.load(config_file)
server_url = "http://" + config["server"]["ip"] + ":" + config["server"]["port"]

print("Registering with the server...")
message = {"id": config["id"], "password": config["password"]}
try:
    res = requests.get(server_url + "/register/", auth=(config["id"], config["password"]), json=json.dumps(message))
    res.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
print(res.json()['data'])

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
    message = {'delta': value}
    try:
        res = requests.post(server_url + '/update/', auth=(config["id"], config["password"]), json=json.dumps(message))
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print("New value set to " + str(res.json()["new_value"]) + ".")
    print("Done.")

    time.sleep(delay)

print("Logging out...")
try:
    res = requests.get(server_url + '/close/', auth=(config["id"], config["password"]))
    res.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
print("Done.")
print("Client finished.")