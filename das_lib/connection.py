import socket
from time import sleep

class Connection:
    def __init__(self):
        self.s = socket.socket()

    def connect(self, host, port):
        self.s.settimeout(2)
        self.s.connect((host, port))
        sleep(0.1)
        
    def ConnectToServer(self):
        
        sleep(0.1)
        self.Connect("127.0.0.1",9800)
        ba=bytearray("LOGIN "+"USER"+" "+"PASSWORD"+" "+"ACCOUNT"+"\r\n",encoding="ascii") #// Input your own USERID -- PASSWORD -- ACCOUNT
        self.Login(ba)
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

    def disconnect(self):
        self.s.sendall(b"QUIT\r\n")
        self.s.close()