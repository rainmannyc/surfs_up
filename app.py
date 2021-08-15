from flask import Flask

app = Flask(__name__)

@app.route('/')
def ais_rule():
    return "I WILL CHANGE THE WORLD!"

