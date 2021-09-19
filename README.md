# Computer security project

---
Authors:<br/>
*Poliakov Ivan*<br/>
*Topal Christian*
---

##How to use:<br/>
1) install python and flask<br/>
2) open the terminal, run server:<br/>
```console   
python server.py
```
3) open another terminal window, run client:<br/>
```console   
python client.py config_1.json
```
You can use any other config instead of config_1.json

##How it works:<br/>
The server is written in flask.<br/>
For communication server and client use REST API.<br/>
First, client sends POST request to the server with ID and the password.<br/>
If given ID is already in session, password is verified to be the same as of ID in session.<br/>
If passwords are not the same the server returns "authentification error".<br/>
If password is the same or there is no client with the same ID that is already connected
the server makes all necessary updates and returns URL for ID's value update.
Then the server starts sending POST requests, one request per value update.<br/>
To wrap it up, the client sends another POST request to log out from the server:<br/>
if there is no client with the given ID remainins, all its data is erased from the server.<br/>
While processing all POST requests, server checks if json data sent to it contains necessary items through try-catch.
If the data is invalid, server returns "invalid data sent to the server"