import uuid
import asyncio
from datetime import datetime, timedelta

class CmdAPI:
    def __init__(self):
        self.uniq = uuid.uuid4()

    async def subscribe(self, connection):
        symbol = input("Enter symbol for subscription: ")
        script = f"SB {symbol.upper()} Lv1\r\n"
        print(f"Sending: {script}")
        try:
            retdata = connection.send_script(bytearray(script, encoding="ascii"))
            print(f"Received: {retdata}")
        except Exception as e:
            print(f"Error: {e}")

    def account_details(self, connection):
        script = "GET AccountInfo\r\n"
        try:
            retdata = connection.send_script(bytearray(script, encoding="ascii"))
            print(f"Account Info: {retdata}")
        except Exception as e:
            print(f"Error: {e}")