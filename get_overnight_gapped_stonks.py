"""
Identifies the stocks within a market cap band that have gapped overnight.
"""

from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
import pandas as pd

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    file_path = "D:/OneDrive/Documents/stonks_testing/"
    file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/"
    if args.mac_or_pc == "mac":
        file_path = file_path_mac

    
    # Initialize with your API key
    api_key = "oPNvU_u9B3eHFJrSG7ppDrnP4HGmgPqU"
    analyzer = GapAnalyzer(api_key)
    
    # Fetch market snapshot
    print("Fetching market snapshot...")
    analyzer.fetch_snapshot()
    
    # Analyze gaps
    print("Analyzing gaps...")
    results = analyzer.analyze_gaps(gap_threshold=0.2, gap_direction="up", pre_market=args.pre_market)
    filtered_results = analyzer.filter_tickers_by_market_cap(
        results['gapped_stocks'],
        min_market_cap=args.min_market_cap,
        max_market_cap=args.max_market_cap
    )
    
    # Display results
    print(f"Filtered stocks by market cap: {filtered_results[:]}")  # Show all
    print(f"Filtered stocks that gap up more than 20%: {len(filtered_results)}")
    
    portfolio_value = 30000
    short_size = min(portfolio_value * 0.5 / len(filtered_results), portfolio_value/10)
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    #yesterday = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    #print(f"Yesterday's date: {yesterday}")
    
    print(f"Trade value per stock: {short_size}")
    ticker_dict = {}
    for ticker in filtered_results:
        last_quote = analyzer.fetch_last_quote(ticker)
        daily_open_close_agg = analyzer.fetch_daily_open_close_agg(ticker, today)
        
        if last_quote and last_quote.bid_price > 0:
            shares_to_locate = analyzer.get_locate_shares_amount(short_size, last_quote.bid_price)
            ticker_dict[ticker] = {"last_quote_bid": last_quote.bid_price, "shares_to_locate": shares_to_locate, "short_size": short_size, "volume": daily_open_close_agg.volume}
            #print(f"{ticker} - Bid Price: {last_quote.bid_price}, Shares to Short: {shares_to_short}")
            
    df = pd.DataFrame.from_dict(ticker_dict, orient='index')
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    print(df)

    df.to_csv(f"{file_path}overnight_gapped_stocks.csv")

if __name__ == "__main__":
    main()
