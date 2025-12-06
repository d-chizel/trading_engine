"""
Gets stocks that have gapped through time.
"""
import csv
from datetime import datetime, date, timedelta
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments, parse_date, get_next_weekday, is_weekday, calculate_overnight_change, get_results_outputs

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
        
    # Loop through all weekdays between start and end date
    prev_date = start_date
    all_results = []
    
    print(f"Starting analysis from {start_date}...")

    all_tickers = analyzer.fetch_all_tickers_for_date(prev_date)
    
    prev_date_daily_agg = analyzer.fetch_daily_aggs(prev_date)
    if len(prev_date_daily_agg) == 0:
        prev_date = get_next_weekday(prev_date + timedelta(days=1))
        prev_date_daily_agg = analyzer.fetch_daily_aggs(prev_date)

    current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    while current_date <= end_date:
        print(current_date)
        
        all_tickers = analyzer.fetch_all_tickers_for_date(current_date)
                
        # Move to next day
        prev_date = current_date
        #prev_date_daily_agg = current_date_daily_agg
        current_date = get_next_weekday(prev_date + timedelta(days=1))
    
    print(f"Completed analysis")
    
    # Verbose output
    #if args.verbose:
    #    df = all_results['dataframe']
    #    print(f"\nDataFrame shape: {df.shape}")
    #    print("\nFirst 5 rows:")
    #    print(df.head())

if __name__ == "__main__":
    main()
