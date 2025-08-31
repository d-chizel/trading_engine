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
    
    # Load CSV file
    input_df = pd.read_csv('input.csv')
    print("Loaded input.csv:")
    
    overnight_data = []

    for index, row in input_df.iterrows():
        date_str = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
        ticker = row['Ticker']

        # Find matching times
        overnight_data.append(analyzer.get_overnight_reference_time_prices(ticker, date_str, print_data_to_file=args.print_data_to_file, verbose=args.verbose))

    df = pd.DataFrame(overnight_data)
    print(df)
    df.to_csv('overnight_prices.csv', index=False)
    print("DataFrame saved to overnight_prices.csv")


if __name__ == "__main__":
    main()
