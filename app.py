from flask import Flask, request, jsonify, render_template, session, redirect, url_for, request
import pandas as pd
from flask_cors import CORS
# import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os

from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
from bson import ObjectId


# def send_email(recipient_email):
#     otp = random.randint(100000, 999999)
#     sender_email = "seekandfindigdtuw@gmail.com"
#     sender_password = os.getenv('Email_password')
#     subject = "OTP for login to SeekAndFind - IGDTUW"
#     body = '''Hello,
#     Thank you for logging into SeekAndFind - IGDTUW. Please enter this OTP to verify your credentials.
#     {} 
#     Best regards,
#     Team SeekAndFind'''.format(otp)

#     # Setup the email server
#     smtp_server = "smtp.gmail.com"  # Example: smtp.gmail.com
#     smtp_port = 587

#     # Create the server object and login
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(sender_email, sender_password)

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     text = msg.as_string()
#     server.sendmail(sender_email, recipient_email, text)

#     server.quit()
#     return otp
#     print("done")

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


'''def send_email(recipient_email):
    otp = random.randint(100000, 999999)

    message = Mail(
        from_email='seekandfindigdtuw@gmail.com',
        to_emails=recipient_email,
        subject='OTP for SeekAndFind',
        html_content=f'<strong>Your OTP is {otp}</strong>'
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
        return otp
    except Exception as e:
        print("SendGrid error:", e)
        return None
'''
def send_email(recipient_email):
    otp = random.randint(100000, 999999)

    message = Mail(
        from_email='seekandfindigdtuw@gmail.com',
        to_emails=recipient_email,
        subject='OTP for SeekAndFind',
        html_content=f'<strong>Your OTP is {otp}</strong>'
    )

    try:
        api_key = os.getenv('SENDGRID_API_KEY')
        print("API KEY FOUND:", bool(api_key))

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print("STATUS CODE:", response.status_code)
        print("RESPONSE BODY:", response.body)
        print("RESPONSE HEADERS:", response.headers)

        if response.status_code == 202:
            print("Email accepted by SendGrid")
            return otp
        else:
            print("Email NOT accepted")
            return None

    except Exception as e:
        print("SendGrid FULL ERROR:", repr(e))
        return None
app = Flask(__name__)
app.secret_key =os.getenv('secret_key')
CORS(app)

# ---------------- CLOUDINARY ---------------- #

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# ---------------- MONGODB ---------------- #

client = MongoClient(os.getenv("MONGO_URI"))
db = client["seekandfind"]
collection = db["items"]



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    session['flag'] = True
    return render_template('dashboard.html')

# @app.route('/found')
# def found():
#     if session.get('flag'):
#         return render_template('found.html')
    

# @app.route('/lost')
# def lost():
#     if session.get('flag'):
#         return render_template('lost.html')

# @app.route('/report')
# def report():
#     if session.get('flag'):
#         return render_template('report.html')

@app.route('/lost')
def lost():
    items = list(collection.find({"type": "lost"}))
    return render_template('lost.html', items=items)


@app.route('/found')
def found():
    items = list(collection.find({"type": "found"}))
    return render_template('found.html', items=items)


@app.route('/report')
def report():
    return render_template('report.html')


# ✅ FORM SUBMISSION (CLOUDINARY + MONGO)
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get("name")
        item_name = request.form.get("item_name")
        description = request.form.get("description")
        contact = request.form.get("contact")
        email = request.form.get("email")
        item_type = request.form.get("type")

        file = request.files.get("image")

        image_url = None
        if file and file.filename != "":
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result.get("secure_url")

        data = {
            "name": name,
            "item_name": item_name,
            "description": description,
            "contact": contact,
            "email": email,
            "type": item_type,
            "image": image_url
        }

        collection.insert_one(data)

        return jsonify({"message": "Item submitted successfully!"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# @app.route('/process', methods=['POST'])
# def process_data():
#     data = request.json
#     user_input = data.get('user_input')
#     result = send_email(user_input)
#     return jsonify({'result': result})

@app.route('/process', methods=['POST'])
def process_data():
    print("Request received")

    data = request.get_json()
    print("DATA:", data)

    try:
        result = send_email(data.get('user_input'))
        print("OTP SENT:", result)
        return jsonify({'result': result})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500
    


@app.route('/dashboard-data')
def dashboard_data():
    email = request.args.get('email')

    # 🔒 DOMAIN CHECK
    if not email.endswith("@igdtuw.ac.in"):
        return jsonify({"error": "Unauthorized"}), 403
    
    lost_items = list(collection.find({"email": email, "type": "lost"}))
    found_items = list(collection.find({"email": email, "type": "found"}))

    # convert ObjectId to string
    for item in lost_items + found_items:
        item['_id'] = str(item['_id'])

    return jsonify({
        "lost": lost_items,
        "found": found_items
    })

@app.route('/delete-item', methods=['POST'])
def delete_item():
    data = request.get_json()
    item_id = data.get("id")

    collection.delete_one({"_id": ObjectId(item_id)})

    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)


