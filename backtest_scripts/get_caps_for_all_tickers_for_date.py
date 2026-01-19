"""
Gets stocks that have gapped through time.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from datetime import datetime, date, timedelta
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments, parse_date, get_next_weekday, is_weekday, calculate_overnight_change, get_results_outputs
import pandas as pd


def main():
    # Parse command line arguments
    args = parse_arguments()
    
    file_path = "D:/OneDrive/Documents/stonks_testing/us_stocks_daily_flat_files/"
    if args.mac:
        file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/us_stocks_daily_flat_files/"
        file_path = file_path_mac
        
    # Set start and end dates
    start_date = args.start_date
    start_date = date.fromisoformat(start_date)
    
    # Load CSV file that includes start_date in the name
    csv_filename = f"{file_path}{start_date}.csv"
    print(csv_filename)
    csv_file_path = os.path.join(os.path.dirname(__file__), csv_filename)
    
    ticker_details_dict = {}
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Use the first column as key, or customize as needed
                key = row[reader.fieldnames[0]]
                ticker_details_dict[key] = row
        print(f"Loaded {len(ticker_details_dict)} entries from {csv_filename}")
    else:
        print(f"Warning: CSV file {csv_filename} not found")
    
    # Initialize with API key
    analyzer = GapAnalyzer(args.api_key)
    
    # Loop through ticker_details_dict
    for key, row_data in ticker_details_dict.items():
        market_cap_data = analyzer.get_market_cap_for_ticker(key)
        ticker_details_dict[key]['market_cap'] = market_cap_data['market_cap'] if market_cap_data else ""
        ticker_details_dict[key]['security_type'] = market_cap_data['type'] if market_cap_data else ""
        print(f"{key} {ticker_details_dict[key]['market_cap']} {ticker_details_dict[key]['security_type']}")

    # Convert dictionary to dataframe and save
    df = pd.DataFrame.from_dict(ticker_details_dict, orient='index')
    output_filename = f"{file_path}market_cap_{start_date}.csv"
    df.to_csv(output_filename, index=False)
    print(f"Saved market cap data to {output_filename}")

if __name__ == "__main__":
    main()
