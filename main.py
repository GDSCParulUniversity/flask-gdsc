from flask import Flask, request
import requests
import psycopg2

conn = psycopg2.connect(
    host="db.cxdnkcyfjguofrvmmemo.supabase.co",
    database="postgres",
    user="postgres",
    password="Temp@4717$1i723471",
    port="5432"
)

cur = conn.cursor()

def sendOtp(phoneNumber):
    headers = {
        "Content-Type": "application/json",
        "ApiKey": "6be2dd73-cc5c-4a03-a42a-3638d687ffc5"
    }
    data = {
        "PhoneNumber": phoneNumber
    }
    res = requests.post("https://api.igniteauth.in/OTP/sendOTP", headers=headers, json=data)
    return res.text

def userExists(phoneNumber):
    cur.execute("SELECT * FROM users WHERE phone_number = %s", (phoneNumber,))
    return cur.fetchone() is not None

def verifyOtp(phoneNumber, verificationCode, otp):
    headers = {
        "Content-Type": "application/json",
        "ApiKey": "6be2dd73-cc5c-4a03-a42a-3638d687ffc5"
    }
    data = {
        "PhoneNumber": phoneNumber,
        "VerificationCode": verificationCode,
        "OTP": otp
    }
    res = requests.post("https://api.igniteauth.in/OTP/verifyOTP", headers=headers, json=data)
    return res.text

password = "xUSx9r8DZpmURiNe"

app = Flask(__name__)

@app.route('/')
def home():
    return "HELLO GDSC"

@app.route('/login', methods=['POST'])
def login():
    postData = request.json
    phoneNumber = postData.get("phoneNumber")

    if userExists(phoneNumber):
        otp = sendOtp(phoneNumber)
        return otp
    else:
        return "User not found"

@app.route('/verify', methods=['POST'])
def verify():
    postData = request.json
    verificationCode = postData.get("verificationCode")
    phoneNumber = postData.get("phoneNumber")
    otp = postData.get("otp")
    res = verifyOtp(phoneNumber, verificationCode, otp)
    return res

@app.route('/signup', methods=['POST'])
def signup():
    postData = request.json
    phoneNumber = postData.get("phoneNumber")
    username = postData.get("username")
    otp = sendOtp(phoneNumber)

    # Save the username to the PostgreSQL database
    cur.execute("INSERT INTO users (username, phone_number) VALUES (%s, %s)", (username, phoneNumber))
    conn.commit()

    return otp

@app.route('/verifySignup', methods=['POST'])
def verifySignup():
    postData = request.json
    verificationCode = postData.get("verificationCode")
    phoneNumber = postData.get("phoneNumber")
    otp = postData.get("otp")
    res = verifyOtp(phoneNumber, verificationCode, otp)
    return res

if __name__ == '__main__':
    app.run(debug=True)
