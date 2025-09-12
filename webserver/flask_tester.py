# flask_tester.py
from flask import Flask, render_template, request
import socketserver
import logging
from dotenv import load_dotenv
import os
import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Getting variables from .env file
load_dotenv()
PIN = os.getenv('pin')

#### NTFY FOR NOTIFICATION ####
# Ntfy.sh url and topic for posting request with IP data
#ntfy_topic: str = "<INSERT NTFY TOPIC>" # Put your custom topic here, remember this is basically your password, so make it hard to guess!
#ntfy_url: str = "https://ntfy.sh/"


#### FLASK APP TO SERVE WEB APP INTERFACE ####
app = Flask(__name__)

@app.route('/')
def numpad():
    return render_template('numpad.html')

@app.route('/process', methods=['POST'])
def process():
    pincode = request.form['pincode']
    # Do something with the user input, like printing it
    print("Pincode:", pincode)
    if pincode == PIN:
        result = "ACCESS"
        #Use the https://notify.sh application to notify you when someone finds the four-digit code.
        ntfy_data = f"{request.remote_addr} has opened the vault!"
        #ntfy_response = requests.post(ntfy_url + ntfy_topic , data=ntfy_data)

    elif pincode == "0000":
        result = "LOCKED"
        #legoMotor.run_for_seconds(1,-50)
        print("Vault Locked")
    else:
        result = "DENIED"

    print(result)
    return render_template('numpad.html', access_result=result)  # Pass the result to the templat

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
