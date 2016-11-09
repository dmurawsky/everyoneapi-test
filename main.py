from flask import Flask, render_template, request
import phonenumbers
import requests
import json

app = Flask(__name__)

def get_phone_data(phone=None):
    return requests.get( "https://api.everyoneapi.com/v1/phone/+1"+phone+"?account_sid=ACbfc1f1309d2048e8bb4bb6f55aea62ef&auth_token=AU406afc41863a466dadacce7721f8802c")

def send_email(email=None, phone=None):
    result = get_phone_data(phone)
    print result.text
    return requests.post(
        "https://api.mailgun.net/v3/sandboxe555194db1b0449ebd95384dbe755cde.mailgun.org/messages",
        auth=("api", "key-25c2c05589bd05267bb84b1e982665f8"),
        data={"from": "Everyone API Inbox <d.r.murawsky@gmail.com>",
              "to": email,
              "subject": "Results from Everyone API Inbox",
              "text": json.dumps(result.text)})

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone = request.form['phone']
        email = request.form['email']
        send_email(phone, email)
    return render_template("index.html")

@app.route("/phone/<number>")
def phone(number=None):
    if len(number) > 9:
        phone = phonenumbers.parse(number, "US")
        if phonenumbers.is_valid_number(phone):
            return "valid"
        else:
            return "invalid"
    return "short"

if __name__ == "__main__":
    app.run(debug=True)
