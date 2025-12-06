"""
Gets stocks that have gapped through time.
"""
import csv
from datetime import datetime, date, timedelta
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments, parse_date, get_next_weekday, is_weekday, calculate_overnight_change, get_results_outputs, bars_to_df
import pandas as pd

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Initialize with API key
    analyzer = GapAnalyzer(args.api_key)
    
    if args.verbose:
        print(f"Using gap threshold: {args.gap_threshold * 100}%")
        print(f"Gap direction: {args.gap_direction}")
        print(f"Market cap range: ${args.min_market_cap:,.0f} - ${args.max_market_cap:,.0f}")
        
    # Parse dates from command line arguments
    try:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date) if args.end_date else None
        
        if end_date:
            print(f"Getting gap stocks from {start_date} to {end_date}")
        else:
            print(f"Getting gap stocks from {start_date} to present")
            end_date = date.today()  # Use today as end date if not specified
            
        # Validate date range
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")
            
        # Ensure start_date is a weekday
        start_date = get_next_weekday(start_date)
        
        # Calculate total weekdays in range
        weekday_count = 0
        temp_date = start_date
        while temp_date <= end_date:
            if is_weekday(temp_date):
                weekday_count += 1
            temp_date += timedelta(days=1)
            
        print(f"Total weekdays to analyze: {weekday_count}")
            
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return
        
    if args.verbose:
        print(f"Start date object: {start_date}")
        print(f"End date object: {end_date}")
        
    # Load tickers for dates
    file_path = "D:/OneDrive/Documents/stonks_testing/"
    if args.mac:
        file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/"
        file_path = file_path_mac
    file_name = file_path + "all_tickers.csv"
    
    # Load tickers from CSV and iterate through them
    all_tickers = {}
    try:
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                if row[0] in all_tickers:
                    all_tickers[row[0]].append(row[1])
                else:
                    all_tickers[row[0]] = [row[1]]
    except FileNotFoundError:
        print(f"Ticker file not found: {file_name}")
        return
    except Exception as e:
        print(f"Error reading ticker file: {e}")
        return
        
    # Loop through all weekdays between start and end date
    prev_date = start_date
    all_results = []
    
    print(f"Starting analysis from {start_date}...")
    
    current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    while current_date <= end_date:
        print(current_date)
        
        current_date_tickers = all_tickers[current_date]
        price_filtered_tickers = analyzer.filter_tickers_for_min_price(current_date_tickers, prev_date)
        # TO DO: grab current prices and output list with prices from current_date
        market_cap_filtered_tickers = analyzer.filter_tickers_by_market_cap(current_date_tickers)
        # TO DO : Fix adjust market caps for date
        price_filtered_tickers = analyzer.filter_tickers_for_min_price(market_cap_filtered_tickers, prev_date)
        price_filtered_tickers_list = price_filtered_tickers['tickers_list']
        price_filtered_tickers_prices = price_filtered_tickers['tickers_with_prices']
        
        for ticker in price_filtered_tickers_list:
            bars = analyzer.fetch_custom_bars(ticker, None, None, prev_date, current_date)
            prev_ticker_price = price_filtered_tickers_prices[ticker]
            bars_df = bars_to_df(bars, ticker, prev_date, current_date)
            
            
                
        # Move to next day
        prev_date = current_date
        current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    print(f"Completed analysis for {len(all_results)} tickers")
        
    # Save to CSV if requested
    if args.output_csv:
        df = all_results['dataframe']
        df.to_csv(args.output_csv, index=False)
        print(f"Results saved to {args.output_csv}")
    
    # Verbose output
    #if args.verbose:
    #    df = all_results['dataframe']
    #    print(f"\nDataFrame shape: {df.shape}")
    #    print("\nFirst 5 rows:")
    #    print(df.head())

if __name__ == "__main__":
    main()
