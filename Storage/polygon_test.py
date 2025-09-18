from polygon import RESTClient

api_key = "oPNvU_u9B3eHFJrSG7ppDrnP4HGmgPqU"  # Replace with your actual API key
client = RESTClient(api_key)

try:
    snapshot = client.get_daily_open_close_agg("IHT", "2025-09-15", adjusted=True)
    print(snapshot)
except Exception as e:
    print(f"Error connecting to Polygon API: {e}")