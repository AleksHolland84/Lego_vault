import socketserver

PINCODE = 4444
HOST = ""
PORT = 8000

class BotHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
            print(f"Bot with ip {self.client_address[0]} sent:")
            print(f"Type: {type(self.data)}, Data: {self.data}")
            data = self.data.decode()
            if data.isnumeric():
                print(f"Data is number {data}")
                if int(data) == PINCODE:
                    r = ("Access Granted\r\n")
                    self.request.send(r.encode())
                else:
                    self.request.send("Access denied!\r\n".encode())
            else:
                self.request.send("Access denied!\r\n".encode())


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), BotHandler) as server:
        try:
            server.serve_forever()
        except Exception as error:
            print("There was an error")
            print(error)
