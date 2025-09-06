"""
Identifies the stocks within a market cap band that have gapped overnight.
"""

from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments
from clearstreet_trading_lib import ClearStreetClient
from clearstreet_trading_lib.utils import format_currency, normalize_symbol, validate_symbol

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    ##### Get gapped stocks from Polygon Start #####
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
    
    ##### Get gapped stocks from Polygon End #####
    
    ##### Get Trade stocks in ClearStreet Start #####
    # Initialize client with your credentials
    clearStreetClient = ClearStreetClient(
        client_id="peHRscbk4tio7g4fPpe1XK8cOAlXqTvL",
        client_secret="bGeu70ZimnTdw7oXUcDfXeAKibQwpKHcpaLLi_5RTaijW2iTOMpTHo6Ul2Tr5Dvm",
        account_id="115147"
    )
    
    # Find the locates for each of the filtered symbols
    filtered_instruments = []
    for symbol in filtered_results:
        try:
            instrument = clearStreetClient.get_instruments(symbol)
            filtered_instruments.append(instrument)
            print(f"Fetched instrument for {symbol}: {instrument}")
        except Exception as e:
            print(f"Error fetching instrument for {symbol}: {e}")
            
    # Create a sell trade for each of the filtered symbols that has a successful locate
    
    # Create a stop loss order for each of the symbols that have been successfully shorted
    
    # Close out all of the open positions at 1030
    
        
    ##### Get Trade stocks in ClearStreet Start #####

if __name__ == "__main__":
    main()
