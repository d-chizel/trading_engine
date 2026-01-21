"""
Gets stocks that have gapped through time.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from datetime import datetime, date, timedelta
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import get_list_of_tickers_from_daily_aggs, parse_arguments, parse_date, get_next_weekday, is_weekday, calculate_overnight_change, get_results_outputs, bars_to_df
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
    input_file_path = "D:/OneDrive/Documents/stonks_testing/massive_backtests/us_stocks_daily_flat_files/"
    if args.mac:
        input_file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/massive_backtests/us_stocks_daily_flat_files/"
        input_file_path = input_file_path_mac
        
    # Loop through all weekdays between start and end date
    prev_date = start_date
    all_results = []
    current_market_caps = {}
        
    print(f"Starting analysis from {start_date}...")
    
    # Get market caps for all tickers on start date
    # TO DO: Should we be getting the tickers from a file so that we can have an in and out sample?
    daily_aggs = analyzer.fetch_daily_aggs(start_date)
    for ticker_agg in daily_aggs:
        ticker = ticker_agg.ticker
        ticker_details = analyzer.fetch_ticker_details(ticker)
        market_cap = ticker_details.market_cap
        current_market_caps[ticker] = {'market_cap': market_cap}
        ticker_prev_agg = analyzer.fetch_previous_day_agg(ticker)
        print(ticker_prev_agg)
        current_market_caps[ticker]['prev_close'] = ticker_prev_agg[0].close if ticker_prev_agg and len(ticker_prev_agg) > 0 else None
        print(f"Ticker: {ticker}, Market Cap: {market_cap}, Prev Close: {current_market_caps[ticker]['prev_close']}")

    current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    while current_date <= end_date:
        print(current_date)
        
        daily_aggs = analyzer.fetch_daily_aggs(current_date)
        current_date_tickeres = get_list_of_tickers_from_daily_aggs(daily_aggs)           
            
                
        # Move to next day
        prev_date = current_date
        current_date = get_next_weekday(prev_date + timedelta(days=1))
    

if __name__ == "__main__":
    main()
