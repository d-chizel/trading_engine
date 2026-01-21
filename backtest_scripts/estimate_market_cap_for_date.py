"""
The Massive API does not provide historical market caps, this script estimates the past market cap by
scaling the current market cap to the historical price.
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
    market_cap_file_path = "D:/OneDrive/Documents/stonks_testing/massive_backtests/market_cap_2026-01-16.csv"
    input_file_path = "D:/OneDrive/Documents/stonks_testing/massive_backtests/daily_bars_with_mkt_cap/"
    output_file_path = "D:/OneDrive/Documents/stonks_testing/massive_backtests/us_stocks_daily_flat_files/"
    if args.mac:
        market_cap_file_path = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/massive_backtests/market_cap_2026-01-16.csv"
        input_file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/massive_backtests/us_stocks_daily_flat_files/"
        output_file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/massive_backtests/daily_bars_with_mkt_cap/"
        input_file_path = input_file_path_mac
        output_file_path = output_file_path_mac
    
    # Load market cap data
    market_cap_df = pd.read_csv(market_cap_file_path)
    market_cap_dict = market_cap_df.set_index('ticker').to_dict('index')
    
    # Loop through all weekdays between start and end date
    prev_date = start_date
    all_results = []
    current_market_caps = {}
        
    print(f"Starting analysis from {start_date}...")
    
    current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    while current_date <= end_date:
        try:
            daily_bars_df = pd.read_csv(f"{input_file_path}{current_date}.csv")
            daily_bars_dict = daily_bars_df.set_index('ticker').to_dict('index')
            print(f"Evaluating date {current_date}")
                        
            # Get market caps for all tickers on current date
            for ticker in daily_bars_dict.keys():
                if ticker in market_cap_dict:
                    scaling_factor = daily_bars_dict[ticker]['close'] / market_cap_dict[ticker]['close']
                    scaled_market_cap = market_cap_dict[ticker]['market_cap'] * scaling_factor
                    daily_bars_dict[ticker]['recent_price'] = market_cap_dict[ticker]['close']                
                    daily_bars_dict[ticker]['recent_market_cap'] = market_cap_dict[ticker]['market_cap']
                    daily_bars_dict[ticker]['scaled_market_cap'] = scaled_market_cap
                    daily_bars_dict[ticker]['security_type'] = market_cap_dict[ticker]['security_type']
                else:
                    daily_bars_dict[ticker]['recent_price'] = None
                    daily_bars_dict[ticker]['recent_market_cap'] = None
                    daily_bars_dict[ticker]['scaled_market_cap'] = None
                    daily_bars_dict[ticker]['security_type'] = None
                            
            # Convert the dictionary back to a DataFrame
            output_df = pd.DataFrame.from_dict(daily_bars_dict, orient='index')
            
            # Save the DataFrame with market cap data to a new CSV
            output_df.to_csv(f"{output_file_path}{current_date}.csv")
            
        except FileNotFoundError:
            print(f"File not found for {current_date}, skipping.")
            # Move to next day
            prev_date = current_date
            current_date = get_next_weekday(current_date + timedelta(days=1))
            continue 
        
        # Move to next day
        prev_date = current_date
        current_date = get_next_weekday(current_date + timedelta(days=1))   

if __name__ == "__main__":
    main()
