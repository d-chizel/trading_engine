import asyncio
from das_lib import Connection, CmdAPI, Utils
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
import pandas as pd

async def main():
    
    '''
        3. Loop through each of the stocks
            3.4. Store the information in the dictionary
            3.5. SLPRICEINQUIRE Short Locate Price Inquire
            3.6. SLNEWORDER Short Locate New Order
            3.7. SLOFFEROPERATION Short Locate Offer Operation to accept the lowest price locate offer
            3.8. NEWORDER to place a market short sale order for the number of shares
        4. #POS Get all positions
        5. Loop through each position
            5.1. If the position is a short position, place a stop loss buy to cover order at 100% above the short sale price
        6. Disconnect from DAS
    '''
    
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
    cmd = CmdAPI()
    
    #Extract one row of the df for testing
    #fifth_element = df.iloc[4:5]
    
    with Connection() as connection:
        try:
            connection.connect_to_server()
            stay_alive = True

            while(stay_alive):
                for index, row in df.iterrows():
                    ticker = row['ticker']
                    shares_to_locate = row.get('shares_to_locate', 0)
                    print(f"\nProcessing ticker: {ticker}, locating {shares_to_locate} shares")
                    short_locate_results = cmd.short_locate_price_inquire_lowest(connection, ticker, shares_to_locate)
                    df.at[index, 'locate_price'] = short_locate_results['locate_price']
                    df.at[index, 'total_locate_cost'] = short_locate_results['total_locate_cost']
                    df.at[index, 'route'] = short_locate_results['route']
                    df.at[index, 'shortable'] = short_locate_results['shortable']

                print(f"\n{df}")
                get_offer = input("Enter Y to repeat or hit Enter to quit: ")

                if get_offer.lower() == 'y':
                    stay_alive = True
                else:
                    stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()
    
if __name__ == "__main__":
    asyncio.run(main())