# app.py
from flask import Flask, render_template, request
import socketserver
import logging
from dotenv import load_dotenv
import os
from buildhat import Motor


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Getting variables from .env file. This is the pin number we need to type to get access.
load_dotenv()
PIN = os.getenv('pin')

# Setting up LEGO
legoMotor = Motor('A')

def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)

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
        legoMotor.when_rotated = handle_motor
        legoMotor.set_default_speed(50)
        legoMotor.run_for_degrees(90)
    else:
        result = "DENIED"

    return render_template('numpad.html', access_result=result)  # Pass the result to the templat

if __name__ == '__main__':
    app.run(debug=True)
