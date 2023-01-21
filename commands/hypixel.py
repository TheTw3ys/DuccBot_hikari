import requests
from dotenv import load_dotenv
load_dotenv()
import lightbulb
import hikari
import json
import sys
import os
os.chdir(os.getcwd() + "/storage")
bazaar =str(os.path.join(os.getcwd(), "bazaar.json"))
print(bazaar)
sys.path.append(f"{os.getcwd()}")
plugin = lightbulb.Plugin(
    name="Hypixel", description="Some things for Hypixel")


def get_current_bazaar_prices()-> list:
    headers= {"Api-Key": os.getenv("HYPIXEL_TOKEN") }
    response = requests.request(url="https://api.hypixel.net/skyblock/bazaar", headers=headers ,method="GET")
    with open("bazaar", "r") as f:
        liste = []
        data = json.load(f)
        with open(bazaar, "w") as d:
            json.dump(response.json(), d, indent=2)
        for item in data["products"]:
            liste.append(data["products"][item]["quick_status"])
    return(liste)

@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option(name="item", type=hikari.Member, description="", required=False)
@lightbulb.command(name="bazaar_raw", description="Gives you your levelinformation")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_bazaar_raw(ctx: lightbulb.context.PrefixContext):
    bazaar = get_current_bazaar_prices()
    await ctx.respond(bazaar)
    




def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")

