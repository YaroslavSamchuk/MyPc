import requests 
import json

data = requests.get("https://api.binance.com/api/v1/exchangeInfo")
data = data.json()
while True:
    for i in data["symbols"]:
        symbol = i["symbol"]
        data_symbol = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        print(str(i['baseAsset']) + "/" + str(i["quoteAsset"]))
        data_symbol = data_symbol.json()
        
        
    with open('binance/json.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    
    