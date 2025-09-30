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
    if args.mac_or_pc == "mac":
        file_path = file_path_mac
        
    # Load overnight gapped stocks from CSV
    csv_file = file_path + "overnight_gapped_stocks.csv"
    df = pd.read_csv(csv_file)
    filtered_results = df['ticker'].tolist()

    utils = Utils()
    cmd = CmdAPI(df)
    
    #Extract one row of the df for testing
    #fifth_element = df.iloc[4:5]
    
    with Connection() as connection:
        try:
            connection.connect_to_server()
            stay_alive = True
            
            while stay_alive:
                """locate_orders = cmd.get_short_locate_orders(connection)
                locate_orders_array = locate_orders.split()
                grouped_orders = [locate_orders_array[i:i+13] for i in range(0, len(locate_orders_array), 13)]
                headers = grouped_orders[:1][0]  # Remove the header row from data
                grouped_orders = grouped_orders[1:-1] # Remove the header row
                grouped_orders_df = pd.DataFrame(grouped_orders, columns=headers)"""
                
                cmd.get_positions(connection)
                #grouped_orders_df = cmd.get_short_locate_orders_df(connection)
                cmd.short_sell_open_auction_new_order(connection, 'MSFT', 1, 'SMAT', 'DAY')
                
                stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()
    
if __name__ == "__main__":
    asyncio.run(main())