import requests
import pprint

printer = pprint.PrettyPrinter()

headers = {
    'User-Agent': 'YourAppName/1.0',  # Replace with a relevant user agent
}

response = requests.get('https://api.chess.com/pub/leaderboards', headers=headers)

if response.status_code == 200:
    data = response.json()
    printer.pprint(data)
else:
    print(f"Error: {response.status_code} - {response.text}")


