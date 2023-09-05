# app.py
from flask import Flask, render_template, request
import socketserver
import logging
from dotenv import load_dotenv
import os
from buildhat import Motor
import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Getting variables from .env file
load_dotenv()
PIN = os.getenv('pin')

# Ntfy.sh
#ntfy_topic: str = "<INSERT NTFY TOPIC>"
#ntfy_url: str = f"https://ntfy.sh/{ntfy_topic}"


# Setting up LEGO
legoMotor = Motor('C')
legoMotor.set_default_speed(50)
legoMotor.when_rotated = handle_motor

def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)



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
        legoMotor.run_for_seconds(1, 50)

        #Use the https://notify.sh application to notify you when someone finds the four-digit code.
        ntfy_data = f"{request.remote_addr} has opened the vault!"
        #ntfy_responce = requests.post(ntfy_url, data=ntfy_data)
                                      
    elif pincode == "0000":
        result = "LOCKED"
        #legoMotor.run_for_seconds(1,-50)
        legoMotor.run_to_position(-90, blocking=False, direction='anticlockwise')
        print("Vault Locked")
    else:
        result = "DENIED"

    return render_template('numpad.html', access_result=result)  # Pass the result to the templat

if __name__ == '__main__':
    app.run(debug=True)
