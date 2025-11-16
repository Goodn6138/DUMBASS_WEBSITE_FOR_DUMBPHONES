from flask import Flask, request, redirect, render_template, jsonify
from flask_cors import CORS
import json
import time
import os

app = Flask(__name__)

# Enable CORS only for your frontend
CORS(app, origins=["https://dumbass-website-for-dumbphones-this-one.onrender.com"])

DB_FILE = "messages.json"

# Initialize database if missing
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

def load_msgs():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_msg(username, text):
    messages = load_msgs()
    messages.append({
        "user": username,
        "text": text,
        "time": int(time.time())
    })
    with open(DB_FILE, "w") as f:
        json.dump(messages, f)

# GET all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(load_msgs())

# POST a message
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    save_msg(data["username"], data["message"])
    return jsonify({"status": "ok"})

# Optional: homepage rendering
@app.route("/")
def home():
    messages = load_msgs()
    return render_template("chat.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
