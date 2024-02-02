import requests
import json

url = 'https://eodhd.com/api/fundamentals/AAPL.US?filter=Earnings::History&api_token=demo&fmt=json'
data = requests.get(url).json()

# Pretty print the JSON data
print(json.dumps(data, indent=4))
