from flask import Flask, render_template, request
import phonenumbers
import requests
import json
import re
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

def get_phone_data(phone=None):
    app.logger.debug("phone: "+phone)
    return requests.get( "https://api.everyoneapi.com/v1/phone/+1"+phone+"?account_sid=ACbfc1f1309d2048e8bb4bb6f55aea62ef&auth_token=AU406afc41863a466dadacce7721f8802c")

def send_email(phone=None, email=None):
    result = get_phone_data(phone)
    app.logger.debug("send_email result: "+json.dumps(result.text))
    return requests.post(
        "https://api.mailgun.net/v3/sandboxe555194db1b0449ebd95384dbe755cde.mailgun.org/messages",
        auth=("api", "key-25c2c05589bd05267bb84b1e982665f8"),
        data={"from": "Everyone API Inbox <postmaster@sandboxe555194db1b0449ebd95384dbe755cde.mailgun.org>",
              "to": email,
              "subject": "Results from Everyone API Inbox",
              "text": json.dumps(result.text)})

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        phone = request.form['phone']
        email = request.form['email']
        non_decimal = re.compile(r'[^\d]+')
        clean_phone = non_decimal.sub('', phone)
        send_email(clean_phone, email)
        message = "Email Sent"
    return render_template("index.html", message=message)

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
