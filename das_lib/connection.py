import socket
from time import sleep

class Connection:
    def __init__(self):
        self.s = socket.socket()

    def connect_to_das(self, host, port):
        self.s.settimeout(10)
        self.s.connect((host, port))
        sleep(0.1)

    def connect_to_server(self):

        sleep(0.1)
        print("Connecting to DAS server...")
        self.connect_to_das("127.0.0.1", 9800)
        print("Connected to DAS server.")
        ba=bytearray("LOGIN "+"CD15147"+" "+"F#ynm@n1918"+" "+"115147"+"\r\n",encoding="ascii") #// Input your own USERID -- PASSWORD -- ACCOUNT
        self.login(ba)
        print("Login successful.")
        #self.SendScript(bytearray("SCRIPT GLOBALSCRIPT SwitchDesktop default"+"\r\n",encoding="ascii"))

    def login(self, login_data):
        self.s.sendall(login_data)
        sleep(0.1)
        print((self.s.recv(1024 * 1024)).decode("ascii"))

    def send_script(self, script):
        try:
            self.s.sendall(script)
            sleep(0.1)
            data = self.recvall()
        except socket.error as e:
            print(f"Socket error: {e}")
            return ""
        return data.decode("ascii").strip()

    def recvall(self):
        data = b""
        bufsize = 4096
        while True:
            packet = self.s.recv(bufsize)
            data += packet
            if len(packet) < bufsize:
                break
        return data

    def disconnect_from_server(self):
        try:
            if self.s:
                self.s.sendall(b"QUIT\r\n")
                self.s.close()
                print("Disconnected from server.")
        except (socket.error, TimeoutError) as e:
            print(f"Error during disconnection: {e}")
        finally:
            self.s = None
        
    # Add context manager methods
    def __enter__(self):
        # Initialize the connection when entering the context
        self.s = socket.socket()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure the connection is closed when exiting the context
        self.disconnect_from_server()