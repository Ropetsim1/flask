import json
from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


class User:
    def __init__(self, accountname, password, secretkey):
        self.accountname = accountname
        self.password = password
        self.secretkey = secretkey


def load_data():
    with open("db.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@app.route("/createaccount")
def createaccount():
    return render_template("createaccount.html")
@app.route("/login")
def login():
    return render_template("login.html")
    pass
@app.route("/api/login", methods=["POST"])
def loginapi():
    data = load_data()

    username = request.form["username"]
    password = request.form["password"]

    if username not in data["users"]:
        return render_template("Invalid_password_or_username.html")

    if data["users"][username]["password"] == password:
        response = make_response("Logged in")
        response.set_cookie("identifier", username)
        return response

    return render_template("Invalid_password_or_username.html")
@app.route("/api/createaccount", methods=["POST"])
def createaccountapi():
    data = load_data()

    username = request.form["username"]
    password = request.form["password"]
    secretkey = random.randint(00000,99999)
    user = User(username, password, secretkey)

    if username in data["users"]:
        return "User already exists", 400

    data["users"][user.accountname] = {
        "password": user.password,
        "secretkey": user.secretkey
    }

    save_data(data)

    return f"Created account: {user.accountname} ur secret key is {secretkey}"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
