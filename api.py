import requests
import json

url = 'https://eodhd.com/api/eod-bulk-last-day/US?api_token=zdvzvzd&symbols=AVON&fmt=json'
data = requests.get(url).json()

# Pretty print the JSON data
print(json.dumps(data, indent=4))


