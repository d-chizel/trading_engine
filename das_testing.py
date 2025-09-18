import asyncio
from das_lib import Connection, CmdAPI

async def main():
    cmd = CmdAPI()
    with Connection() as connection:
        try:
            connection.connect("127.0.0.1", 9800)
            connection.login(bytearray("LOGIN USER PASSWORD ACCOUNT\r\n", encoding="ascii"))
            await cmd.subscribe(connection)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect()

if __name__ == "__main__":
    asyncio.run(main())