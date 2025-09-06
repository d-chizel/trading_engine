"""
Identifies the stocks within a market cap band that have gapped overnight.
"""

from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments

def main():
    # Parse command line arguments
    args = parse_arguments()
    
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

if __name__ == "__main__":
    main()
