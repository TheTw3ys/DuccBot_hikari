import asyncio
import json
import os
import sys

import hikari
import lightbulb
from hikari import Embed

os.chdir(os.getcwd() + "/storage")

sys.path.append(f"{os.getcwd()}")  # adds folder "/storage" to sys.path temporarily
_json = ".json"

from functions_and_classes import \
    Leveling  # module can now be used from ./v2/storage/functions_and_classes

plugin = lightbulb.Plugin(name="Leveling", description="Leveling I guess")
guild_list = [699010600331771955, 911288030210428938, 715208493237403731]

global_users_json = str(os.path.join(os.getcwd(), "ranking", "Global.json"))  # makes path availabile for Linux and Windows
info_json = str(os.path.join(os.getcwd(), "info.json"))  # makes path availabile for Linux and Windows


@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("number", type=int, description="The list of the leaderboard ", required=False)
@lightbulb.command(name="leaderboard", description="The leaderboard of the global Ducc Bot")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_leaderboard(ctx: lightbulb.context.PrefixContext):
                                # TODO add way of list e.g. 1-10; 11-20 etc.
    guild = ctx.get_guild()
    users_json = str(os.path.join(os.getcwd(), "ranking", (guild.name + _json)))
    leaderboard = Leveling.get_leaderboard(users_json=users_json)
    embed = Embed(title="Global Leaderboard")
    liste = ""
    x = 1
    for list1 in leaderboard:
        member = f"<@!{list1[0]}>"
        # embed.add_field(name=member, value=list1[1])
        string = f"{x}. {member} {list1[1]}exp lvl {int(list1[1] ** (1 / 3))}\r\n"
        x += 1
        liste += string
    embed.description = str(liste)
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("exp", type=str, description="the Experience you should get now (an Integer please)", required=False)
@lightbulb.command(name="expchange", description="Changes the Experience you gain from the leveling system")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_expchange(ctx: lightbulb.context.PrefixContext):
    args1 = ctx.options.exp
    embed = Embed(title="Expchange")
    print(args1)                                                    #TODO rewrite so that each guild has own kind of exp
    if args1.isdigit():
        with open(info_json, "r") as f:
            newexp = json.load(f)
            newexp["expchange"] = int(args1)
            with open(info_json, "w") as d:
                json.dump(newexp, d)
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
    users_json = str(os.path.join(os.getcwd(), "ranking", (guild.name + _json)))
    with open(users_json, "r") as f:
        data = json.load(f)

        if not member:
            user = ctx.author
        else:
            user = member
        experience = data[f"{user.id}"].get("experience")
        levels = data[f"{user.id}"].get("level")
        next_experience = round((levels + 1) ** 3)
        name = str(user)[:-5]
        embed = Embed(title=f"Levelsystem Info von {name}",
                      description=f"Level: {levels}\r\n"
                                  f"Experience: {experience}XP\r\n"
                                  f"Experience für das nächste Level: {next_experience}XP",
                      color=0x22a7f0)
        embed.set_thumbnail(user.avatar_url)
        embed.set_footer(text=f"Sent in guild: {guild.name} Full view at https://duccbot.ichweissja.net")
    await ctx.respond(embed=embed)


@plugin.listener(event=hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    guild = await event.app.rest.fetch_guild(event.message.guild_id)
    guild_id = str(guild.id)
    users_json = str(os.path.join(os.getcwd(), "ranking", (guild.name + _json)))
    if not event.author.is_bot and os.path.exists(users_json):
        with open(users_json, "w") as a:    # possible because it is the same as above but now actually created
            a.write("{}")



    async def update_full_data(userjson):
        if not os.path.exists(os.path.join(os.getcwd(), ("info.json"))):
            with open(os.path.join(os.getcwd(), ("info.json")), "w") as f:
                f.write("{"+ f'"{guild_id}" : 5' + "}")
        await asyncio.sleep(1)
        exp = 5
        if str(userjson) != global_users_json:
            with open(info_json, "r") as d:              
                d = json.load(d)
                exp = int(d.get(guild_id))
                print(exp)
        asyncio.sleep
        with open(userjson) as b:
            users = json.load(b)
        
        await update_data(users, event.author)
        await add_experience(users, event.author, exp)
        await level_up(users, event.author, event)
        with open(userjson, 'w') as f:
            json.dump(users, f, indent=2)
    await asyncio.sleep(1)

    await update_full_data(users_json)
    await update_full_data(global_users_json)


@plugin.listener(event=hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    guild = await event.app.rest.fetch_guild(event.guild_id)
    users_json = str(os.path.join(os.getcwd(), "ranking", (guild.name + _json)))

    if not os.path.exists(os.path.join(os.getcwd(), "ranking", (guild.name + _json))):
        with open(os.path.join(os.getcwd(), "ranking", (guild.name + _json)), "w") as a:
            a.write("{}")
    with open(users_json, "r") as c:
        users = json.load(c)

    await update_data(users, event.member.user)

    with open(users_json, 'w') as f:
        json.dump(users, f)


async def update_data(users, user) -> None:
    if f'{user.id}' not in users:
        users[f"{user.id}"] = {}
        users[f'{user.id}']["id"] = int(user.id)
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['name'] = str(user.username)


async def add_experience(users, user, exp):
    users[f'{str(user.id)}']['experience'] += exp


async def level_up(users, user, event):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 3))
    if lvl_start < lvl_end:
        users[f'{user.id}']['level'] = lvl_end
        if lvl_end % 5 == 0:
            await event.app.rest.create_message(channel=event.channel_id,
                                                content=f'{user.mention} has leveled up to level {lvl_end}')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")
