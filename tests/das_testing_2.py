import asyncio
from das_lib import Connection, CmdAPI, Utils
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
import pandas as pd

async def main():

    # Parse command line arguments
    args = parse_arguments()
    
    file_path = "D:/OneDrive/Documents/stonks_testing/"
    file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/"
    if args.mac:
        file_path = file_path_mac
        
    # Load overnight gapped stocks from CSV
    csv_file = file_path + "overnight_gapped_stocks.csv"
    df = pd.read_csv(csv_file, index_col=0)

    cmd = CmdAPI(df)
    
    #Extract one row of the df for testing
    #fifth_element = df.iloc[4:5]
    
    with Connection() as connection:
        try:
            connection.connect_to_server()
            stay_alive = True
            
            while stay_alive:                
                cmd.create_buy_new_order(connection, 'MSFT', 1, 500.00, 'XALL', 'DAY')
                
                cmd.get_bid_ask_price(connection, "LV1", "MSFT")
                
                stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()
    
if __name__ == "__main__":
    asyncio.run(main())