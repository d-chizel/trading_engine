from datetime import date
import pandas as pd
from polygon import RESTClient
from polygon.rest.models import (
    TickerSnapshot,
    Agg,
)

client = RESTClient("8N6bwNZ7awkAPNHQySbg8eQVI_yM6OTD")

snapshot = client.get_snapshot_all(
	"stocks",
)

#print(snapshot)

# Convert snapshot data to pandas DataFrame
data_rows = []
gap_down_percentage = 0.2

def get_gapped_stonks(snapshot, gap_down_percentage):
    """
    Function to get gapped stocks based on the provided snapshot and gap down percentage.
    """
    gapped_stocks = []
    
    # crunch some numbers and collect data
    for item in snapshot:
        # verify this is a TickerSnapshot
        if isinstance(item, TickerSnapshot):
            # verify this is an Agg
            if isinstance(item.prev_day, Agg):
                # verify this is a float
                if isinstance(item.prev_day.open, float) and isinstance(
                    item.prev_day.close, float
                ):
                    if (hasattr(item.min, 'close') and item.min.close != 0 and hasattr(item.prev_day, 'close') and item.prev_day.close != 0):
                        overnight_change = (
                            item.min.close / item.prev_day.close - 1
                        )
                    else:
                        overnight_change = 0
                    
                    if overnight_change < -gap_down_percentage:
                        gapped_stocks.append(item.ticker)
    
    return gapped_stocks

def get_overnight_change(item):
    """
    Function to calculate the overnight change for a given TickerSnapshot item.
    """
    if hasattr(item.min, 'close') and item.min.close != 0 and hasattr(item.prev_day, 'close') and item.prev_day.close != 0:
        return item.min.close / item.prev_day.close - 1
    return 0

# crunch some numbers and collect data
for item in snapshot:
    # verify this is a TickerSnapshot
    if isinstance(item, TickerSnapshot):
        # verify this is an Agg
        if isinstance(item.prev_day, Agg):
            # verify this is a float
            if isinstance(item.prev_day.open, float) and isinstance(
                item.prev_day.close, float
            ):
                if (hasattr(item.min, 'close') and item.min.close != 0 and hasattr(item.prev_day, 'close') and item.prev_day.close != 0):
                    overnight_change = (
                        item.min.close / item.prev_day.close - 1
                    )
                else:
                    overnight_change = 0
                
                # Collect data for DataFrame
                row_data = {
                    'ticker': item.ticker,
                    'prev_open': item.prev_day.open,
                    'prev_close': item.prev_day.close,
                    'prev_high': item.prev_day.high if hasattr(item.prev_day, 'high') else None,
                    'prev_low': item.prev_day.low if hasattr(item.prev_day, 'low') else None,
                    'prev_volume': item.prev_day.volume if hasattr(item.prev_day, 'volume') else None,
                    'min_close': item.min.close if hasattr(item, 'min') and hasattr(item.min, 'close') else None,
                    'overnight_change': overnight_change,
                }
                data_rows.append(row_data)
                """
                print(
                    "{:<15}{:<15}{:<15}{:.2f} %".format(
                        item.ticker,
                        item.prev_day.open,
                        item.prev_day.close,
                        item.min.close if hasattr(item, 'min') and hasattr(item.min, 'close') else 0,
                        percent_change,
                    )
                )
                """                

# Create DataFrame
df = pd.DataFrame(data_rows)

# Display DataFrame info
print(f"\nDataFrame created with {len(df)} rows")
print("\nFirst 10 rows:")
print(df.head(10))

print(f"\nDataFrame columns: {list(df.columns)}")
print(f"\nDataFrame shape: {df.shape}")

gap_stonks = get_gapped_stonks(snapshot, gap_down_percentage)
print(gap_stonks)
