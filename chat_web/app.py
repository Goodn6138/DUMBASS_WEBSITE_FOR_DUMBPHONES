from flask import Flask, request, redirect, render_template
import json
import time
import os

app = Flask(__name__)

DB_FILE = "messages.json"

# initialize
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        text = request.form["message"]
        save_msg(username, text)
        return redirect("/")

    messages = load_msgs()

    return render_template("chat.html", messages=messages)

app.run(host="0.0.0.0", port=10000)
