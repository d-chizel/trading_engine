"""
Example usage of the polygon_stonks library.
"""

from polygon_stonks_lib import GapAnalyzer

def main():
    # Initialize with your API key
    api_key = "8N6bwNZ7awkAPNHQySbg8eQVI_yM6OTD"
    analyzer = GapAnalyzer(api_key)
    
    # Fetch market snapshot
    print("Fetching market snapshot...")
    analyzer.fetch_snapshot()
    
    # Analyze gaps
    print("Analyzing gaps...")
    results = analyzer.analyze_gaps(gap_threshold=0.2, gap_direction="down")
    
    # Display results
    print(f"\nTotal stocks analyzed: {results['total_stocks']}")
    print(f"Stocks with gaps > 20%: {results['gapped_count']}")
    print(f"Gapped stocks: {results['gapped_stocks'][:]}")  # Show all
    
    # Display DataFrame info
    df = results['dataframe']
    print(f"\nDataFrame shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df)

if __name__ == "__main__":
    main()
