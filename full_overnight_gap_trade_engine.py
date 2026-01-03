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

    # Initialize with your API key
    api_key = "oPNvU_u9B3eHFJrSG7ppDrnP4HGmgPqU"
    analyzer = GapAnalyzer(api_key)
    
    # Fetch market snapshot
    print("Fetching market snapshot...")
    analyzer.fetch_snapshot()
    
    # Analyze gaps
    print("Analyzing gaps...")
    results = analyzer.analyze_gaps(gap_threshold=0.2, gap_direction="up", after_open=args.after_open)
    filtered_results = analyzer.filter_tickers_by_market_cap(
        results['gapped_stocks'],
        min_market_cap=args.min_market_cap,
        max_market_cap=args.max_market_cap
    )
    
    # Display results
    print(f"Filtered stocks by market cap: {filtered_results[:]}")  # Show all
    print(f"Filtered stocks that gap up more than 20%: {len(filtered_results)}")
    
    portfolio_value = args.port_value
    short_size = min(portfolio_value * (3/3) / len(filtered_results), portfolio_value/10)
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    #yesterday = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    #print(f"Yesterday's date: {yesterday}")
    
    print(f"Trade value per stock: {short_size}")
    ticker_dict = {}
    for ticker in filtered_results:
        last_quote = analyzer.fetch_last_quote(ticker)
        daily_ticker_snapshot = analyzer.fetch_snapshot_ticker(ticker)
        volume = daily_ticker_snapshot.prev_day.volume
        bid_price = 0
        ask_price = 0

        if last_quote:
            if last_quote.bid_price > 0:
                bid_price = last_quote.bid_price
            if last_quote.ask_price > 0:
                ask_price = last_quote.ask_price
            shares_to_locate = analyzer.get_locate_shares_amount(short_size, last_quote.bid_price)
            ticker_dict[ticker] = {"last_quote_bid": bid_price, "last_quote_ask": ask_price, "shares_to_locate": shares_to_locate, "short_size": short_size, "volume": volume}
        else:
            print(f"No last quote data for {ticker}, skipping...")
                    
    df = pd.DataFrame.from_dict(ticker_dict, orient='index')
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    print(df)

    df.to_csv(f"{file_path}overnight_gapped_stocks.csv")
    
    # Load overnight gapped stocks from CSV
    #csv_file = f"{file_path}overnight_gapped_stocks.csv"
    #df = pd.read_csv(csv_file, index_col=0)

    utils = Utils()
    cmd = CmdAPI(df)

    #Extract one row of the df for testing
    #fifth_element = df.iloc[4:5]

    with Connection() as connection:
        try:
            connection.connect_to_server()
            stay_alive = True
            stay_alive_2 = True
            first_run = True

            while(stay_alive):
                cmd.update_df_with_short_locate_orders(connection)
                if first_run:
                    cmd.inquire_short_locate_for_all_gapped_stocks(connection)
                    first_run = False
                    
                cmd.get_shares_to_short()
                cmd.pre_locate_checks()
                cmd.update_df_with_positions(connection)
                cmd.pre_trade_checks()
                
                print(f"\nUpdated ticker_df with positions:\n{cmd.ticker_df}")
                
                if args.autorun == True:
                    get_locates = "yes"
                else:
                    get_locates = input("Type 'Yes' to create short locate orders or Enter to skip: ")

                if get_locates.lower() == 'yes':
                    cmd.short_locate_new_order_for_all_gapped_stocks(connection, autorun=args.autorun)
                else:
                    print("Skipping short locate order creation.\n")
                    
                cmd.update_df_with_short_locate_orders(connection)
                cmd.pre_trade_checks()
                print(f"\nUpdated ticker_df with positions:\n{cmd.ticker_df}\n")
                    
                if args.autorun == True:
                        sell_short = "yes"
                else:
                    sell_short = input("Type 'Yes' to create short sell orders or Enter to quit: ")
                    
                if sell_short.lower() == 'yes':
                    while(stay_alive_2):

                        cmd.short_sell_join_offer_for_all_gapped_stocks(connection, autorun=args.autorun)
                        
                        rerun_sell = input("Type 'Yes' to re-attempt any execution Enter to quit: ")
                        if rerun_sell.lower() != 'yes':
                            stay_alive_2 = False

                stay_alive = False

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.disconnect_from_server()

if __name__ == "__main__":
    asyncio.run(main())