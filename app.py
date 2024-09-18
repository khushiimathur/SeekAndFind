from flask import Flask, request, jsonify, render_template, session, redirect, url_for, request
import pandas as pd
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os

def send_email(recipient_email):
    otp = random.randint(100000, 999999)
    sender_email = "mathurkhushi027@gmail.com"
    sender_password = os.getenv('Email_password')
    subject = "OTP for login to SeekAndFind - IGDTUW"
    body = '''Hello,
    Thank you for logging into SeekAndFind - IGDTUW. Please enter this OTP to verify your credentials.
    {} 
    Best regards,
    Team Lost&Found'''.format(otp)

    # Setup the email server
    smtp_server = "smtp.gmail.com"  # Example: smtp.gmail.com
    smtp_port = 587

    # Create the server object and login
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)

    server.quit()
    return otp
    print("done")

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    session['flag'] = True
    return render_template('dashboard.html')

@app.route('/found')
def found():
    if session.get('flag'):
        return render_template('found.html')
    

@app.route('/lost')
def lost():
    if session.get('flag'):
        return render_template('lost.html')

@app.route('/report')
def report():
    if session.get('flag'):
        return render_template('report.html')

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    user_input = data.get('user_input')
    result = send_email(user_input)
    return jsonify({'result': result})
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)

