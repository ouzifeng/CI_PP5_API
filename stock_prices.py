import requests
import json
from datetime import datetime

# URL for the API request
url = 'https://eodhd.com/api/eod/MCD.US?period=d&api_token=demo&fmt=json'

# Make the API request
response = requests.get(url)
data = response.json()

# Current year
current_year = datetime.now().year

# Calculate the start year (current year - 10)
start_year = current_year - 11

# Filter for end of year stock prices for the last 10 years
end_of_year_prices = []

for year in range(start_year, current_year + 1):
    # Find records for this year and sort them by date in descending order
    yearly_records = sorted(
        (record for record in data if int(record['date'][:4]) == year),
        key=lambda x: x['date'],
        reverse=True
    )
    
    # Find the last trading day of the year (could be 31st, 30th, or 29th)
    for record in yearly_records:
        if record['date'].endswith('-12-31') or record['date'].endswith('-12-30') or record['date'].endswith('-12-29'):
            end_of_year_prices.append(record)
            break  # Stop after finding the last trading day

# Pretty print the filtered end-of-year prices
print(json.dumps(end_of_year_prices, indent=4))
