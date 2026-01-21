import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boto3
from botocore.config import Config
from datetime import date, timedelta
from polygon_stonks_lib.utils import parse_arguments
    
args = parse_arguments()

# Set start and end dates
start_date = "2022-01-01"
end_date = "2023-12-31"
start_date = date.fromisoformat(start_date)
end_date = date.fromisoformat(end_date)

def get_next_weekday(d):
    """
    Returns the next date that is a weekday (Monday-Friday).
    """
    next_day = d + timedelta(days=1)
    while next_day.weekday() >= 5:  # Monday is 0 and Sunday is 6
        next_day += timedelta(days=1)
    return next_day

print(f"Start date: {start_date}, End date: {end_date}")

'''
response = input("Press Enter to continue, or type 'exit' to quit: ")
if response.lower() == 'exit':
    print("Exiting script.")
    exit()
'''

file_path = "D:/OneDrive/Documents/stonks_testing/us_stocks_daily_flat_files/"
if args.mac:
    file_path_mac = "/Users/derrickkchan/Library/CloudStorage/OneDrive-Personal/Documents/stonks_testing/us_stocks_daily_flat_files/"
    file_path = file_path_mac

# Initialize a session using your credentials
session = boto3.Session(
  aws_access_key_id='c72eda21-4ca5-453c-adb1-5ed22346e5b3',
  aws_secret_access_key='oPNvU_u9B3eHFJrSG7ppDrnP4HGmgPqU',
)

# Create a client with your session and specify the endpoint
s3 = session.client(
  's3',
  endpoint_url='https://files.massive.com',
  config=Config(signature_version='s3v4'),
)

# Specify the bucket name
bucket_name = 'flatfiles'

get_date = start_date
while get_date <= end_date:
    # File location is: us_stocks_sip/day_aggs_v1/2025/12/2025-12-13.csv.gz
    object_key = f'us_stocks_sip/day_aggs_v1/{get_date.year}/{get_date.month:02d}/{get_date}.csv.gz'
    local_file_name = object_key.split('/')[-1]  # e.g., '2025-06-12.csv.gz'
    local_file_path = file_path + local_file_name

    print(f"Downloading file '{object_key}' from bucket '{bucket_name}'...")

    # Download the file
    try:
        s3.download_file(bucket_name, object_key, local_file_path)
        print(f"File downloaded successfully and saved to '{local_file_path}'")
    except Exception as e:
        print(f"Error downloading file for date {get_date}: {e}")

    get_date = get_next_weekday(get_date)