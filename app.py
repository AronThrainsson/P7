import random

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    number = random.randint(1, 10)
    return render_template("index.html", number=number)

@app.route("/goodbye")
def bye():
    return "Goodbye!"