import os

import hikari
import lightbulb
import pymongo
from hikari import Embed
from pymongo.collection import Collection
host, port = os.getenv("DB_HOST"), int(os.getenv("DB_PORT"))
client = pymongo.MongoClient(host, port)
db = client["DuccBotRanking"]
plugin = lightbulb.Plugin(name="Leveling", description="Leveling I guess")
guild_list = [699010600331771955, 911288030210428938, 715208493237403731]
global_collection = db.Global
info_json = str(os.path.join(os.getcwd(), "info.json"))  # makes path availabile for Linux and Windows

# TODO make this leaderboard working
"""
@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("number", type=int, description="The list of the leaderboard ", required=False, default=1)
@lightbulb.command(name="leaderboard", description="The leaderboard of the global Ducc Bot")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_leaderboard(ctx: lightbulb.context.PrefixContext):
    max_number = int(ctx.options.number) * 10                     
    guild = ctx.get_guild()
    leaderboard = Leveling.get_leaderboard(users_json=user_json)
    embed = Embed(title="Global Leaderboard", description="empty")
    description = ""
    x = 0
    for list1 in leaderboard:
        x += 1
        if x <= max_number -10:            
            continue
        x + max_number - 10
        member = f"<@!{list1[0]}>"
        string = f"{x}. {member} {list1[1]}exp lvl {int(list1[1] ** (1 / 3))}\r\n"
        x - max_number + 10
        description+= string
        if x == max_number:
            break
    embed.description = str(description)
    if not description:
        embed.description= "Empty\r\nBro read the page number"    
    embed.set_footer(f"Page {int(max_number/10)}/{int(len(leaderboard)/10)+ 1}")
    await ctx.respond(embed=embed)
"""


@plugin.command
@lightbulb.option("text", type=str, description="Why are you still sending something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("exp", type=str, description="the Experience you should get now (an Integer please)", required=False)
@lightbulb.command(name="expchange", description="Changes the Experience you gain from the leveling system")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_expchange(ctx: lightbulb.context.PrefixContext):
    args1 = ctx.options.exp
    embed = Embed(title="Expchange")
    if args1.isdigit():
        client["DuccBotConfig"].get_collection("info").update_one({"_id": ctx.guild_id},
                                                                  {"$set": {"expchange": int(args1)}})
        embed.description = f'Changed Xp-Multiplier to {int(args1)}'

    else:
        embed.description = "You didn't send an integer."
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option(name="member", type=hikari.Member, description="", required=False)
@lightbulb.command(name="level", description="Gives you your levelinformation")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_level(ctx: lightbulb.context.PrefixContext):
    member = ctx.options.member
    guild = ctx.get_guild()
    collection = db[f"{guild.name}"] if str(ctx.options.text).lower() != "global" else db.Global
    user = ctx.author if not member else member
    obj = collection.find_one(filter={"_id": user.id})
    experience = obj.get('experience')
    level = obj.get('level')
    next_experience = round((level + 1) ** 3)
    name = str(obj.get("name"))
    embed = Embed(title=f"Levelsystem Info von {name}",
                  description=f"Level: {level}\r\n"
                              f"Experience: {experience}XP\r\n"
                              f"Experience für das nächste Level: {next_experience}XP",
                  color=0x22a7f0)
    embed.set_thumbnail(user.avatar_url)
    embed.set_footer(text=f"Sent in guild: {guild.name} Full view at https://duccbot.ichweissja.net")

    await ctx.respond(embed=embed)


@plugin.listener(event=hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    guild = await event.app.rest.fetch_guild(event.message.guild_id)
    if not event.author.is_bot:
        if guild.name not in db.list_collection_names():
            db.create_collection(name=guild.name)
            client["DuccBotConfig"].get_collection("info").insert_one({"_id": guild.id, "expchange": 5})
    else:
        return
    collection = db.get_collection(guild.name)

    async def update_full_data(collection: Collection, exp=5):
        await update_data(user=event.author, collection=collection)
        await add_experience(user=event.author, collection=collection, exp=exp)
        await level_up(user=event.author, collection=collection, event=event)

    await update_full_data(collection, client["DuccBotConfig"].get_collection("info").find_one(
        filter={"_id": guild.id}).get("expchange"))
    await update_full_data(global_collection)


@plugin.listener(event=hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    guild = await event.app.rest.fetch_guild(event.guild_id)
    user = event.member.user
    collection = db[f"{guild.name}"]
    await update_data(user, collection)


async def update_data(user, collection: Collection) -> None:
    print(collection.find_one({"_id": user.id}))
    if not collection.find_one({"_id": user.id}):
        object = {
            "_id": user.id,
            "experience": 0,
            "level": 1,
            "name": user.username
        }
        collection.insert_one(object)


async def add_experience(user, collection: Collection, exp):
    collection.update_one({"_id": user.id}, {"$inc": {"experience": exp}})


async def level_up(user, collection: Collection, event):
    experience = collection.find_one(filter={"_id": user.id}).get("experience")
    lvl_start = collection.find_one(filter={"_id": user.id}).get("level")
    lvl_end = int(experience ** (1 / 3))
    if lvl_start < lvl_end:
        collection.update_one({"_id": user.id}, {"$inc": {"level": 1}})
        if lvl_end % 5 == 0:
            await event.app.rest.create_message(channel=event.channel_id,
                                                content=f'{user.mention} has leveled up to level {lvl_end}')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
