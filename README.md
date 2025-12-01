# OpenChat

A very simple real‑time chat app built with **Flask**, **python‑socketio**, and **Eventlet**.  
Clients connect via Socket.IO from the browser, pick a username, and exchange messages in a shared room.

Project Link -> https://open-chat-gh0x.onrender.com

---

## Features

- Real‑time messaging using Socket.IO (WebSocket / long‑polling).
- Username selection via browser prompt; messages are shown as `username: text`.
- Basic online‑users broadcast (logged in the browser console).
- Simple responsive UI: scrollable message area + input + Send/Leave buttons.

---

## Tech Stack

- **Backend**: Python, Flask, python‑socketio, Eventlet.
- **Frontend**: Plain HTML + CSS + vanilla JS + Socket.IO client.
- **Entry point**: `src/main.py`
- **Template**: `src/templates/home.html`

---

## Project Structure

chatApp/
  src/
    main.py              # Flask + Socket.IO server
    templates/
      home.html          # Chat UI + Socket.IO client---

## Setup & Run (Local)

1. **Create and activate a virtualenv** (optional but recommended):

  
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   2. **Install dependencies**:

  
   pip install flask python-socketio eventlet
   3. **Run the server** from the project root (where `src/` lives):

  
   python -m src.main
   4. **Open the app** in your browser:

   - Go to `http://localhost:8000/`.

5. **Use it**:

   - On page load you’ll be prompted for a username.
   - Type a message in the input and click **Send** (or press Enter).
   - Open multiple tabs/windows to see real‑time chat between them.
   - Click **leave** to disconnect the current tab.

---

## How It Works (Quick Overview)

- `main.py`
  - Creates a Flask app to serve `home.html`.
  - Wraps Flask with a Socket.IO server using Eventlet as the async mode.
  - Tracks users in a `usernames` dict: `sid -> username`.
  - Events:
    - `connect`: sets default username `"Guest"` and broadcasts usernames.
    - `add_username(sid, name)`: updates the username for that connection.
    - `my_mssg(sid, data)`: prepends the username and emits a `message` event to all clients.
    - `disconnect`: removes the user and rebroadcasts usernames.

- `home.html`
  - Renders a simple chat card layout (message list + input + buttons).
  - Connects to the server via `const socket = io();`.
  - On load, prompts for a username and emits `add_username`.
  - Listens for:
    - `message` → appends a `<li>` with the message text.
    - `usernames` → logs the current list of usernames to the console.
  - `Send` button / Enter key emits `my_mssg`.
  - `leave` button calls `socket.disconnect()`.

---

## Deploying (High‑Level)

This is a **long‑running Python Socket.IO server**, so it cannot be deployed to static‑only hosts like Netlify.

Typical options:

- **Render / Railway / Fly.io / a VPS**:
  - Add a `requirements.txt` with:

   
    flask
    python-socketio
    eventlet
      - Configure the service to run:

   
    python -m src.main
      - Optionally, read the port from the `PORT` env variable instead of hard‑coding `8000`.

Once deployed, use the provided URL (e.g. `https://your-app.onrender.com`) in your browser to access OpenChat.

---
