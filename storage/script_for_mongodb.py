import pymongo
import json
import os


client = pymongo.MongoClient("localhost", 27017)
db = client["DuccBotRanking"]

guild_id_object= {
    "Besenkammer": 679440617272770580,
    "Ententeich🦆": 699010600331771955,
    "Projektvorstellung": 1113201814901375089,
    "faintmau5 server for tests": 715208493237403731,
    "mfst": 911288030210428938,
}
for server in os.listdir():
    if server.endswith(".json"):
        with open(server, "r") as f:
            print(server[:-5])
            data = json.load(f)
            id = ""
            if server[:-5] in guild_id_object:
                print("inside")
                id = f"{guild_id_object[server[:-5]]}-"
            db.create_collection(name=f"{id}{server[:-5]}")
            for user_id in data:
                db[f"{id}{server[:-5]}"].insert_one(data[user_id])
