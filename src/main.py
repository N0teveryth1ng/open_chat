# import eventlet
# eventlet.monkey_patch()

# import socketio
# from flask import Flask, render_template


# # Flask app setup
# flask_app = Flask(__name__, template_folder="templates")


# # Socket.IO setup
# sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
# app = socketio.WSGIApp(sio, flask_app)



# # list of users online


# # server home page route
# @flask_app.route("/")
# def index():
#     return render_template('home.html') 

# # Serve home page -- optional
# @flask_app.route('/home')
# def home():
#     return render_template('home.html')


# # setup connection
# @sio.event
# def connect(sid, environ): 
#     usernames[sid] = "Guest"
#     sio.emit("usernames", list(usernames.values()))
#     print("connected: ", sid)



# # message recived
# usernames = {}

# @sio.event     
# def my_mssg(sid, data):
#     username = usernames.get(sid, "Unknown")
#     print(f" {username}: {data}")
#     sio.emit("message", f"{username}: {data}")




# #  - - - - - add username
# @sio.event
# def add_username(sid, name):
#     usernames[sid] = name
#     print(f"{sid} set username to {name}")
#     sio.emit("usernames", list(usernames.values()))



# # --------------------   disconnect -------------------------
# @sio.event
# def disconnect(sid, reason=None):
#     if sid in usernames:
#         usernames.pop(sid, None)
#     sio.emit("usernames", list(usernames.values()))
#     print(f" {sid} disconnected! reason={reason} ")    





# # test modules 
# if __name__ == "__main__":
#     eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)    
    
    
    
    
    
    
    
    




    















import os
import eventlet
eventlet.monkey_patch()

import socketio
from flask import Flask, render_template
import json

PORT = int(os.environ.get("PORT", 8000))

# ─── Setup ─────────────────────────────
flask_app = Flask(__name__, template_folder="templates")

sio = socketio.Server(
    async_mode='eventlet',
    cors_allowed_origins='*'
)

app = socketio.WSGIApp(sio, flask_app)

usernames = {}


# ─── Routes ────────────────────────────
@flask_app.route("/")
def index():
    return render_template("home.html")


@flask_app.route("/home")
def home():
    return render_template("home.html")


# ─── Connect ───────────────────────────
@sio.event
def connect(sid, environ):
    usernames[sid] = "Guest"


    sio.emit("usernames", list(usernames.values()))
    sio.emit("system", "A user joined")


    print("Connected:", sid)


# ─── Username ──────────────────────────
@sio.event
def add_username(sid, name):
    usernames[sid] = name


    sio.emit("usernames", list(usernames.values()))
    sio.emit("system", f"{name} joined")


    print(f"{sid} -> {name}")


# ─── Message (STRICT JSON ONLY) ────────
@sio.event
def my_mssg(sid, data):
    username = usernames.get(sid, "Unknown")


    try:
        parsed = json.loads(data)
    except Exception as e:
        print("❌ Invalid JSON received:", data)
        return  # HARD FAIL — don't send garbage


    # enforce structure
    payload = {
        "username": username,
        "type": parsed.get("type", "text"),
        "text": parsed.get("text", ""),
        "name": parsed.get("name"),
        "mime": parsed.get("mime"),
        "size": parsed.get("size"),
        "dataUrl": parsed.get("dataUrl")
    }


    sio.emit("message", json.dumps(payload))


# ─── Disconnect ────────────────────────
@sio.event
def disconnect(sid, reason=None):
    name = usernames.get(sid, "Unknown")
    usernames.pop(sid, None)


    sio.emit("usernames", list(usernames.values()))
    sio.emit("system", f"{name} left")


    print(f"{sid} disconnected")


# ─── Run ───────────────────────────────
if __name__ == "__main__":
    eventlet.wsgi.server(
        eventlet.listen(("0.0.0.0", PORT)),
        app
    )






































    