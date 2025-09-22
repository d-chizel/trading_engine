import asyncio
from das_lib import Connection, CmdAPI

async def main():
    
    '''
        1. Get the gapped stocks from overnight
        2. Create a dictionary to store each stock and relevant information
        2. Connect to DAS
        3. Loop through each of the stocks
            3.1. Subscribe to Level 1 data
            3.2. Wait to receive Level 1 data
            3.3. Parse the Level 1 data to extract the B: price
            3.4. Divide 1000 by the B: price from the Level 1 data to get number of shares to sell
            3.5. Store the information in the dictionary
            3.6. SLPRICEINQUIRE Short Locate Price Inquire
            3.7. SLNEWORDER Short Locate New Order
            3.8. SLOFFEROPERATION Short Locate Offer Operation to accept the lowest price locate offer
            3.9. NEWORDER to place a market short sale order for the number of shares
        4. #POS Get all positions
        5. Loop through each position
            5.1. If the position is a short position, place a stop loss buy to cover order at 100% above the short sale price
        6. Disconnect from DAS
    '''
    
    cmd = CmdAPI()
    with Connection() as connection:
        try:
            connection.connect_to_server()
            stay_alive = True
            
            while(stay_alive): 
                await cmd.subscribe(connection, "Lv1", "AAPL")
                stay_alive = False  # For demo purposes, exit after one iteration
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()

if __name__ == "__main__":
    asyncio.run(main())