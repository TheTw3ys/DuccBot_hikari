import requests
from dotenv import load_dotenv
import os
import json
import time
load_dotenv()
class BazaarItem:
    def __init__(self, name, sell_price, sell_volume, sell_moving_week, sell_orders, buy_price, buy_volume, buy_moving_week, buy_orders):
        self.name = name
        self.sell_price= sell_price
        self.sell_volume= sell_volume
        self.sell_moving_week= sell_moving_week
        self.sell_orders= sell_orders
        self.buy_price= buy_price
        self.buy_volume= buy_volume
        self.buy_moving_week= buy_moving_week
        self.buy_orders= buy_orders
    
    def get_margin(self):
        try:
            return((self.buy_price/self.sell_price))
        except ZeroDivisionError:
            return(0)

def get_current_bazaar() -> list:
    headers= {"Api-Key": os.getenv("HYPIXEL_TOKEN") }
    response = requests.request(url="https://api.hypixel.net/skyblock/bazaar", headers=headers ,method="GET")
    if not os.path.exists(os.path.join("hypixel.json")):
        with open("hypixel.json", "w") as f:
            f.write("{}")
            time.sleep(1)
    with open("hypixel.json", "r") as f:
        liste = []
        data = json.load(f)
        with open("hypixel.json", "w") as d:
            json.dump(response.json(), d, indent=2)
        for item in data["products"]:
            liste.append(data["products"][item]["quick_status"])
    #print(liste)
    return(liste)

data: list = get_current_bazaar()
liste = []
for bazaar_item in data:
   x = data.index(bazaar_item)
   #print(data[x])
   item = BazaarItem(name=data[x].get("productId"), sell_price=data[x].get("sellPrice"), sell_volume=data[x].get("sellVolume"), sell_moving_week=data[x].get("sellMovingWeek"), sell_orders=data[x].get("sellOrders"), buy_price=data[x].get("buyPrice"), buy_volume=data[x].get("BuyVolume"), buy_moving_week=data[x].get("buyMovingWeek"), buy_orders=data[x].get("buyOrders"))
   liste.append(item)
print(len(liste))

for item in liste:
    print(item.get_margin())

print(len(liste))