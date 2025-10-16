import asyncio
import cmd
from das_lib import Connection, CmdAPI, Utils
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
import pandas as pd

async def main():
    
    # Parse command line arguments
    args = parse_arguments()
    
    file_path = "D:/OneDrive/Documents/stonks_testing/"
    if args.mac:
        file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/"
        file_path = file_path_mac

    # Load overnight gapped stocks from CSV
    csv_file = f"{file_path}overnight_gapped_stocks.csv"
    df = pd.read_csv(csv_file, index_col=0)

    utils = Utils()
    cmd = CmdAPI(df)

    #Extract one row of the df for testing
    #fifth_element = df.iloc[4:5]

    with Connection() as connection:
        tasks = []
        try:
            connection.connect_to_server()
            stay_alive = True
            rerun_order_entry = "yes"

            while(stay_alive):
                cmd.update_df_with_short_locate_orders(connection)
                cmd.inquire_short_locate_for_all_gapped_stocks(connection)
                cmd.get_shares_to_short()
                cmd.pre_locate_checks()
                cmd.update_df_with_positions(connection)
                cmd.pre_trade_checks()
                print(f"\nUpdated ticker_df with positions:\n{cmd.ticker_df}")

                if rerun_order_entry.lower() == 'yes':
                    
                    for index, row in cmd.ticker_df.iterrows():
                        print(f"Processing ticker: {row['ticker']}")
                        tasks.append(asyncio.create_task(cmd.get_ask_price(connection, "LV1", row['ticker'])))

                    await asyncio.gather(*tasks)

                    rerun_order_entry = input("Type 'Yes' to create another order or Enter to quit: ")
                    if rerun_order_entry.lower() != 'yes':
                        stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()

if __name__ == "__main__":
    asyncio.run(main())