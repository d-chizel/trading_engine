#!/usr/bin/env python3
"""
Script to find close prices ('c' values) at specific New York times.
Searches for data at 9:30 AM, 10:30 AM, and 12:00 PM EST/EDT.
"""

from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments, parse_date
import pandas as pd


def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Initialize with your API key
    api_key = args.api_key
    analyzer = GapAnalyzer(api_key)
    
    file_path = "D:/OneDrive/Documents/stonks_testing/intraday_prices_for_pnl_tracking/"
    file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/intraday_prices_for_pnl_tracking/"
    if args.mac_or_pc == "mac":
        file_path = file_path_mac
    
    input_file = f"{file_path}trades_data.csv"
    output_file = f"{file_path}open_high_low_close.csv"

    # Load CSV file
    input_df = pd.read_csv(input_file)
    print(f"Loaded {input_file}:")
    
    overnight_data = []

    for index, row in input_df.iterrows():
        date_str = pd.to_datetime(row['date']).strftime('%Y-%m-%d')
        ticker = row['ticker']

        # Find matching times
        overnight_data.append(analyzer.get_overnight_reference_time_prices(ticker, date_str, print_data_to_file=args.print_data_to_file, verbose=args.verbose))
        print(f"Processed {ticker} for {date_str}")

    df = pd.DataFrame(overnight_data)
    print(df)
    df.to_csv(output_file, index=False)
    print(f"DataFrame saved to {output_file}")

if __name__ == "__main__":
    main()
