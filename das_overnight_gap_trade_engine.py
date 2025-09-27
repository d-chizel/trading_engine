import asyncio
from das_lib import Connection, CmdAPI, Utils
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
import pandas as pd

async def main():
    
    '''
        4. #POS Get all positions
        5. Loop through each position
            5.1. If the position is a short position, place a stop loss buy to cover order at 100% above the short sale price
        6. Disconnect from DAS
    '''
    
    # Parse command line arguments
    args = parse_arguments()
    
    file_path = "D:/OneDrive/Documents/stonks_testing/"
    if args.mac_or_pc == "mac":
        file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/"
        file_path = file_path_mac

    # Load overnight gapped stocks from CSV
    csv_file = f"{file_path}overnight_gapped_stocks.csv"
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

            while(stay_alive):
                cmd.update_df_with_short_locate_orders(connection)
                cmd.inquire_short_locate_for_all_gapped_stocks(connection)
                cmd.get_shares_to_short()
                cmd.pre_trade_checks()

                print(args.autorun)

                print(f"\n{cmd.ticker_df}")
                if args.autorun == True:
                    get_locates = "yes"
                else:
                    get_locates = input("Type 'Yes' to create short locate orders or Enter to skip: ")

                if get_locates.lower() == 'yes':
                    cmd.short_locate_new_order_for_all_gapped_stocks(connection, autorun = args.autorun)
                    
                if args.autorun == True:
                    sell_short = "yes"
                else:
                    sell_short = input("Type 'Yes' to create short sell orders or Enter to quit: ")

                if sell_short.lower() == 'yes':
                    cmd.short_sell_market_new_order_for_all_gapped_stocks(connection, df, autorun = args.autorun)

                stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()

if __name__ == "__main__":
    asyncio.run(main())