#---------------------------------------------------------#
#                        MODULER                        #
#---------------------------------------------------------#
import requests #importerer requests modulet


#---------------------------------------------------------#
#                        VARIABLER                        #
#---------------------------------------------------------#
url = "http://192.168.0.79:5000/process" # URL'ens opbygning: Protocol (http://),  IP/DOMÆNENAVN (192.168.0.79), Port (:5000) og Sti (/process)
pin = "0001" # Vi sætter vores pinkode til "0001"
payload = {"pincode": pin} # data der skal sendes der 


# Sæt response-objektet til at være "response". 
# Response-objektet sender et POST request til vres url med vores payload.
response = requests.post(f"http://{url}", data = payload)

# Hvis respons attributten (.text) indeholder "DENIED" skal terminale printe PIN + vores pinkode + DENIED
if "DENIED"  in response.text:
    print(f"PIN {pin} DENIED")
# Ellers skal den printe ACCESS WITH PIN: vores pinkode
else:
    print(f"""################### ACCESS WITH PIN: {pin} ####################""")