import eventlet
eventlet.monkey_patch()

import socketio
from flask import Flask, render_template


# Flask app setup
flask_app = Flask(__name__, template_folder="templates")


# Socket.IO setup
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
app = socketio.WSGIApp(sio, flask_app)



# list of users online


# server home page route
@flask_app.route("/")
def index():
    return render_template('home.html') 

# Serve home page -- optional
@flask_app.route('/home')
def home():
    return render_template('home.html')


# setup connection
@sio.event
def connect(sid, environ): 
    usernames[sid] = "Guest"
    sio.emit("usernames", list(usernames.values()))
    print("connected: ", sid)



# message recived
usernames = {}

@sio.event     
def my_mssg(sid, data):
    username = usernames.get(sid, "Unknown")
    print(f" {username}: {data}")
    sio.emit("message", f"{username}: {data}")




#  - - - - - add username
@sio.event
def add_username(sid, name):
    usernames[sid] = name
    print(f"{sid} set username to {name}")
    sio.emit("usernames", list(usernames.values()))



# --------------------   disconnect -------------------------
@sio.event
def disconnect(sid, reason=None):
    if sid in usernames:
        usernames.pop(sid, None)
    sio.emit("usernames", list(usernames.values()))
    print(f" {sid} disconnected! reason={reason} ")    





# test modules 
if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)    
    
    
    
    
    
    
    
    