import json
import os

import __main__
trigger_list = "triggers.json"
guild_id = "91128803021042893"
class User:
    def __init__(self):
        self.id = 330303
        self.experience = 20
        self.level = 20
        self.name = "meppi"


meppi = User()


def update_data(users, user) -> None:
    if f'{user.id}' not in users:
        print(users)
        users[f'{user.id}']["id"] = user.id
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['name'] = user.name

with open(r"/storage/ranking/Global.json", "r")as f:
    users = json.load(f)


def test():
    update_data(users, meppi)

with open(r"/storage/ranking/Global.json", "w")as d:
    json.dump(users, d)

test()
