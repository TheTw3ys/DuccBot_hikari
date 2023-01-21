import requests
from dotenv import load_dotenv
import os
import json
import time
load_dotenv()
os.chdir(os.getcwd() + "/storage")
bazaar = str(os.path.join(os.getcwd(), "bazaar.json"))
print(bazaar)


class BazaarItem:
    def __init__(self, name, sell_price, sell_volume, sell_moving_week, sell_orders, buy_price, buy_volume, buy_moving_week, buy_orders):
        self.name = name
        self.sell_price = sell_price # instasell price -> buy price
        self.sell_volume = sell_volume 
        self.sell_moving_week = sell_moving_week
        self.sell_orders = sell_orders
        self.buy_price = buy_price # instabuy price -> sell price
        self.buy_volume = buy_volume
        self.buy_moving_week = buy_moving_week 
        self.buy_orders = buy_orders

    def get_decimal_margin(self) -> float:
        try:
            return (self.buy_price / self.sell_price) -1 
        except ZeroDivisionError:
            return (0)

    def get_relative_probability_of_quick_market_response(self)->float:
        """
        THIS IS JUST A TECHNICAL IDEA OF QUICK MARKET RESPONSE
        this does not take into account the "item-moving"
        just if offer and demand are almost equal 
        whereas almost 0 means almost no demand -> no market response
        and something hugely bigger than 1 no offer -> also no market response  
        """
        try:
            probability = (self.buy_moving_week/self.sell_moving_week)
        except ZeroDivisionError:
            return (0)
        return probability


def get_current_bazaar() -> list:
    headers = {"Api-Key": os.getenv("HYPIXEL_TOKEN")}
    response = requests.request(
        url="https://api.hypixel.net/skyblock/bazaar", headers=headers, method="GET")
    if not os.path.exists(os.path.join(bazaar)):
        with open(bazaar, "w") as f:
            f.write("{}")
    with open(bazaar, "r") as f:
        quick_status_list = []
        data = json.load(f)
        with open(bazaar, "w") as d:
            json.dump(response.json(), d, indent=2)
        for item in data["products"]:
            quick_status_list.append(data["products"][item]["quick_status"])

    
    return (quick_status_list)

#TODO maybe add OOP already in get_current_bazaar() for workability


def sort_by_current_realistic_float_margin(data: list)-> list:
    """ gets all current margins of bazaar items availible"""
    full_list = []
    for bazaar_item in data:
        x = data.index(bazaar_item)
        item = BazaarItem(name=data[x].get("productId"), sell_price=data[x].get("sellPrice"), sell_volume=data[x].get("sellVolume"), sell_moving_week=data[x].get("sellMovingWeek"), sell_orders=data[x].get(
            "sellOrders"), buy_price=data[x].get("buyPrice"), buy_volume=data[x].get("buyVolume"), buy_moving_week=data[x].get("buyMovingWeek"), buy_orders=data[x].get("buyOrders"))
        if item.get_decimal_margin() > 0:  #and not item.name.startswith("ENCHANTMENT_ULTIMATE"):
            full_list.append(item)

    sorted_list = sorted(full_list, key=lambda x: x.get_decimal_margin(), reverse=True)
    realistic_list = []
    for bazaar_item in sorted_list:
        if bazaar_item.buy_volume < 4000:
            if bazaar_item.sell_volume< 4000:
                continue
        if bazaar_item.get_decimal_margin() >= 100:
            """
            TODO This technically removes a way of quick money
                 May be updated with sorting of buy-/sell_moving_week 
                 for more accuracy calculate way of 
                 see https://stackoverflow.com/questions/31623177/how-to-sort-by-closest-number
                 for reference on how to bring BazaarItem.get_relative_probability_of_quick_market_response()
                 in sorted way for market_reaction_probability
            """    

            continue 
        else:   realistic_list.append(bazaar_item)   
        
    return realistic_list
    
   
#print(len(sort_by_current_float_margin(get_current_bazaar())))

#for item in sort_by_current_float_margin(get_current_bazaar()):
    #print(item.get_decimal_margin(), item.name, item.buy_price, item.sell_price)

for item in sort_by_current_realistic_float_margin(get_current_bazaar()):
    print(item.name, item.get_decimal_margin(), item.get_relative_probability_of_quick_market_response())

print(len(sort_by_current_realistic_float_margin(get_current_bazaar())))