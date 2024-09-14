from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def send_email(recipient_email):
    otp = random.randint(100000, 999999)
    sender_email = "mathurkhushi027@gmail.com"
    sender_password = "uhrg plsv afhl kxho"
    subject = "OTP for login to Lost&Found - IGDTUW"
    body = '''Hello,
    Thank you for logging into Lost&Found - IGDTUW. Please enter this OTP to verify your credentials.
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
CORS(app)

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    user_input = data.get('user_input')
    result = send_email(user_input)
    return jsonify({'result': result})
    

if __name__ == '__main__':
    app.run(debug=True)
