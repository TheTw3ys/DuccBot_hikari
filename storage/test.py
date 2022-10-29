import json

data = {
    "guilds": {
        "911288030210428938": {
            "this sjdhfjsdfhb": "thatsd fkjs kfdhkjdf",
            "this": "that"
        }
    }
}


# guild = "911288030210428938"
# print(data["guilds"][guild])
class AlreadyTrigger(Exception):
    pass




def test(message, guild):
    if "when i say" in message:

        liste = message.split("you say")  # splits message to ['when i say this ', ' that']
        you_say = str(liste[1]).strip()  # thing that is reacted to

        liste_2 = str(liste[0]).strip().split("when i say")
        when_i_say = str(liste_2[1]).strip()  # trigger
        when_i_say_data = {f"{when_i_say}": f"{you_say}"}  # data

        with open(r"C:\Users\mansf\PycharmProjects\Hikari-Tests\lightbulb_bot\v2\storage\triggers.json") as f:
            data: dict = json.load(f)
            liste = []
            if guild in data["guilds"]:  # if guild_id in storage
                if when_i_say in data["guilds"][guild]:  # if the trigger already registered
                    raise AlreadyTrigger

                data["guilds"][guild].update(when_i_say_data)  # just update the triggers of the guild_id
            else:
                data["guilds"].update({guild: when_i_say_data})  # add new guild_id to storage and first triggers

        with open(r"C:\Users\mansf\PycharmProjects\Hikari-Tests\lightbulb_bot\v2\storage\triggers.json", 'w') as f:
            json.dump(data, f, indent=2)  # add new trigger and response


try:
    test("when i say Thissss you say SsS", "91128803010428938")
except AlreadyTrigger:
    print("Already a trigger, do you want to edit the triggers?")

