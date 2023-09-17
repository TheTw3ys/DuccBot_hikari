import os
import hikari
import lightbulb
import pymongo
from hikari import Embed
from pymongo.collection import Collection
import pymongo
host, port = os.getenv("DB_HOST"), int(os.getenv("DB_PORT"))
client = pymongo.MongoClient(host, port)

db = client["DuccBotRanking"]
plugin = lightbulb.Plugin(name="Leveling", description="Leveling I guess")
guild_list = [699010600331771955, 911288030210428938, 715208493237403731]
global_collection = db.Global


@plugin.command
@lightbulb.option("rest", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False, default="1")
@lightbulb.command(name="leaderboard", description="The leaderboard of the Ducc Bot")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_leaderboard(ctx: lightbulb.context.PrefixContext):
    rest_list = str(ctx.options.rest).split(" ")
    try:
        if not rest_list[0].isnumeric() and not rest_list[1].isnumeric():
            max_number = 10
        else:
            max_number = int(rest_list[0])*10 if rest_list[0].isnumeric() else int(rest_list[1])*10
    except IndexError:
        max_number = 10
    min_number = max_number - 10

    guild_name = ctx.get_guild().name
    embed = Embed()
    description = ""
    embed.set_thumbnail(ctx.get_guild().icon_url)
    guild_string = f"{ctx.guild_id}-{guild_name}"
    if "global" in rest_list[0].lower() or "global" in rest_list[1].lower():
        embed.set_thumbnail()
        guild_string = "Global"
        guild_name = "Global"
    embed.title = f"Leaderboard for {guild_name}"

    leaderboard = db[guild_string].find().sort("experience", pymongo.DESCENDING)
    x = 0
    len_leaderboard = 0
    for member in leaderboard:
        x += 1
        len_leaderboard += 1
        if min_number < x <= max_number:
            user_name = f"<@!{int(member['_id'])}>"
            string = f"{x}. {user_name} {member['experience']}exp lvl {member['level']}\r\n"
            description += string

    embed.description = str(description)
    if not description:
        embed.description = "Empty\r\nBro read the page number"
    embed.set_footer(f"Page {int(max_number/10)}/{int((len_leaderboard+ 10)/10)}        Full view at "
                     f"https://duccbot.ichweissja.net")
    embed.url = "https://duccbot.ichweissja.net"
    await ctx.respond(embed=embed)


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
    collection = db[f"{guild.id}-{guild.name}"] if str(ctx.options.text).lower() != "global" else db.Global
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
    guild_name_string = f"{guild.id}-{guild.name}"
    experience = 10
    try:
        experience = client["DuccBotConfig"].get_collection("info").find_one(filter={"_id": guild.id}).get("expchange")
    except AttributeError:
        client["DuccBotConfig"].get_collection("info").insert_one({"_id": guild.id, "expchange": 5, "name": guild.name})

    if not event.author.is_bot:
        if guild_name_string not in db.list_collection_names():
            db.create_collection(name=guild_name_string)

    else:
        return
    collection = db.get_collection(guild_name_string)

    async def update_full_data(collection: Collection, exp=5):
        await update_data(user=event.author, collection=collection)
        await add_experience(user=event.author, collection=collection, exp=exp)
        await level_up(user=event.author, collection=collection, event=event)

    await update_full_data(collection, experience)
    await update_full_data(global_collection)


@plugin.listener(event=hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    guild = await event.app.rest.fetch_guild(event.guild_id)
    user = event.member.user
    collection = db[f"{guild.id}-{guild.name}"]
    await update_data(user, collection)


async def update_data(user, collection: Collection) -> None:
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
