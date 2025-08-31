#!/usr/bin/env python3
"""
Script to find close prices ('c' values) at specific New York times.
Searches for data at 9:30 AM, 10:30 AM, and 12:00 PM EST/EDT.
"""

import json
import argparse
from polygon_stonks_lib import GapAnalyzer
from polygon_stonks_lib.utils import parse_arguments, find_ny_times_in_data


def main():
    parser = argparse.ArgumentParser(description="Find close prices at specific NY times")
    parser.add_argument('file', help='JSON file to analyze')
    parser.add_argument('--times', nargs='+', help='Custom times in HH:MM format (e.g., 09:30 10:30 12:00)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Parse custom times if provided
    target_times = [(9, 30), (10, 30), (12, 0)]  # Default times
    if args.times:
        target_times = []
        for time_str in args.times:
            try:
                hour, minute = map(int, time_str.split(':'))
                target_times.append((hour, minute))
            except ValueError:
                print(f"Invalid time format: {time_str}. Use HH:MM format.")
                return
    
    # Load JSON data
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {args.file}")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {args.file}: {e}")
        return
    
    # Find matching times
    results = find_ny_times_in_data(data, target_times)
    
    # Display results
    if results:
        print(f"Found {len(results)} records at target NY times:")
        print("-" * 80)
        
        for result in results:
            print(f"Time: {result['target_time']} ({result['ny_time']})")
            print(f"Close Price: {result['close_price']}")
            print(f"Timestamp: {result['timestamp_ms']}")
            if args.verbose:
                print(f"Raw Data: {result['raw_item']}")
            print("-" * 40)
    else:
        print("No records found at the specified NY times.")
        
        if args.verbose:
            print("\nFirst few items in data for debugging:")
            sample_data = data if isinstance(data, list) else [data]
            for i, item in enumerate(sample_data[:3]):
                print(f"Item {i}: {item}")

if __name__ == "__main__":
    main()
