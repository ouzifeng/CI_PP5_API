import requests
import json

url = 'https://eodhd.com/api/fundamentals/0AB3.LSE?filter=General&api_token=649401f5eeff73.67939383&fmt=json'
data = requests.get(url).json()

# Pretty print the JSON data
print(json.dumps(data, indent=4))
