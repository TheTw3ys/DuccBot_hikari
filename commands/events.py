from functions_and_classes import Administration
import lightbulb
import hikari
import json
import sys
import os
os.chdir(os.getcwd() + "/storage")

sys.path.append(f"{os.getcwd()}")


plugin = lightbulb.Plugin(
    name="StupidStuff", description="Some things I came up with dunno")


@plugin.listener(event=hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    guild = await event.app.rest.fetch_guild(event.message.guild_id) 
    guild_json = str(os.path.join(os.getcwd(), "ranking", (guild.name + ".json")))
    member = event.member
    with open(guild_json, "r") as f:
        users = json.load(f)
        for user in users:
            if f'{user.id}' == member.id:
                print("Hi")
            else:
                return("Hi new" )
                # greet new member


@plugin.listener(event=hikari.MemberDeleteEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    member = event.member
    await event.app.rest.create_message(channel=event.channel_id,
                                        content=f'{member.name} has left')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")
