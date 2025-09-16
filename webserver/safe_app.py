#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import socketserver
import logging
from dotenv import load_dotenv
import os
from buildhat import Motor
import requests
import argparse
from datetime import datetime, timedelta
import argparse

"""
Lego Vault - Flask app med valgfri lockout via argparse.

Kør uden lockout (elever kan brute-force):
    python3 app.py

Kør med lockout:
    python3 app.py -l
    python3 app.py --lockout

Bemærk: Dette er et undervisningsprojekt. Kør kun mod din egen Pi i et kontrolleret netværk.
"""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Getting variables from .env file
load_dotenv()
PIN = os.getenv('pin')

# Enkel in-memory struktir til demo (ikke vedvarende)
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_LOCKOUT_SECONDS = 60    # lockout tid, fx 60 sekunder
DEFAULT_DELAY_SECONDS = 1 # delay ved forkert PIN for at gøre brute-force dyrere

# In-memory struktur til at holde failed attempts (til undervisning)
# Struktur: { ip: {"count": int, "locked_until": datetime or None } }
failed_attempts = {}


def ip_from_request():
    # For klassens netværk er request.remote_addr ofte tilstrækkeligt
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        # tag første IP i listen
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"

def is_locked(ip):
    info = failed_attempts.get(ip)
    if not info:
        return False
    locked_until = info.get("locked_until")
    if locked_until and datetime.utcnow() < locked_until:
        return True
    return False

def record_failed(ip, max_attempts, lockout_seconds):
    info = failed_attempts.setdefault(ip, {"count": 0, "locked_until": None})
    info["count"] += 1
    print(f"FAILED: {ip}, ATTEMPTS: {failed_attempts.get(ip).get('count')}/{max_attempts}")
    if info["count"] >= max_attempts:
        info["locked_until"] = datetime.utcnow() + timedelta(seconds=DEFAULT_LOCKOUT_SECONDS)
        info["count"] = 0  # nulstil tæller efter lock
        app.logger.info(f"IP {ip} locked until {info['locked_until'].isoformat()}")

def reset_failed(ip):
    failed_attempts.pop(ip, None)


#### FLASK APP TO SERVE WEB APP INTERFACE ####
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('numpad.html')

@app.route('/process', methods=['POST'])
def process_pin():
    ip = ip_from_request()
    # hent config
    lockout_enabled = app.config.get("LOCKOUT_ENABLED", False)
    max_attempts = app.config.get("MAX_ATTEMPTS", DEFAULT_MAX_ATTEMPTS)
    lockout_seconds = app.config.get("LOCKOUT_SECONDS", DEFAULT_LOCKOUT_SECONDS)
    delay_seconds = app.config.get("DELAY_SECONDS", DEFAULT_DELAY_SECONDS)

    if lockout_enabled and is_locked(ip):
        print("LOCKED")
        return "LOCKED", 403


    pincode = (request.form.get('pincode') or "").strip()
    # Do something with the user input, like printing it
    print("Pincode:", pincode)
    if pincode == PIN:
        result = "ACCESS"
        reset_failed(ip)

    elif pincode == "0000":
        result = "LOCKED"
        print("Vault Locked")
    else:
        result = "DENIED"
        record_failed(ip, max_attempts, lockout_seconds)

    return render_template('numpad.html', access_result=result)  # Pass the result to the


def parse_args():
    parser = argparse.ArgumentParser(description="Lego Vault Flask server (med valgfri lockout)")
    # Alias: -l/--lockout og --logout (du nævnte -l eller --logout)
    parser.add_argument("-l", "--lockout", action="store_true", help="Aktiver lockout / rate-limiting")
    parser.add_argument("--logout", action="store_true", help="Alias for --lockout (tilfælde af stavefejl)")
    parser.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS,
                        help=f"Max antal forkerte forsøg før lock (default: {DEFAULT_MAX_ATTEMPTS})")
    parser.add_argument("--lockout-seconds", type=int, default=DEFAULT_LOCKOUT_SECONDS,
                        help=f"Lockout længde i sekunder (default: {DEFAULT_LOCKOUT_SECONDS})")
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS,
                        help=f"Delay i sekunder ved forkert PIN (default: {DEFAULT_DELAY_SECONDS})")
    parser.add_argument("--host", default="0.0.0.0", help="Host at bind to (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port to run Flask on (default 5000)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # Hvis enten lockout eller logout er sat, aktiver lockout
    lockout_on = args.lockout or args.logout
    app.config["LOCKOUT_ENABLED"] = lockout_on
    app.config["MAX_ATTEMPTS"] = args.max_attempts
    app.config["LOCKOUT_SECONDS"] = args.lockout_seconds
    app.config["DELAY_SECONDS"] = args.delay_seconds

    if lockout_on:
        print("Lockout ER aktiveret.")
        print(f"Max forsøg: {args.max_attempts}, Lockout tid: {args.lockout_seconds}s, Delay: {args.delay_seconds}s")
    else:
        print("Lockout ER IKKE aktiveret. Server kører sårbar: elever kan brute-force (kun til undervisning).")

    # Start Flask direkte (kør ikke via `flask run` hvis du vil bruge argparse)
    app.run(host=args.host, port=args.port)
