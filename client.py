import sys
import json
import requests

conv = [{'input': 'hi', 'topic': 'Greeting'}]
s = json.dumps(conv)
res = requests.post("http://127.0.0.1:5000/determine_escalation/", json=s).json()
print(res['escalate'])