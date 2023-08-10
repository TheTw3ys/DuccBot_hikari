import hikari
import lightbulb
from hikari import Embed
from lightbulb import commands
import os
import sys
os.chdir(os.getcwd() + "/storage")# changes directory to ./v2/storage

sys.path.append(f"{os.getcwd()}") # adds folder "/storage" to sys.path temporarily

from functions_and_classes import Leveling # module can now be used from ./v2/storage/functions_and_classes

plugin = lightbulb.Plugin(name="Userinformation", description="Gives users information about themselves or others")

users_json = str(os.path.join(os.getcwd(), "Global.json")) # makes path availabile for Linux and Windows


@plugin.command
@lightbulb.option("member", "The member you want information about", type=hikari.Member, required=False)
@lightbulb.command(name="userinfo", description="Gives you some information about a member or yourself")
@lightbulb.implements(commands.PrefixCommand)
async def command_userinfo(ctx: lightbulb.context.PrefixContext):
    global level, xp
    user = ctx.options.member
    if user:
        member = user
        print(member.created_at)
        print(type(member))
    else:
        member = ctx.member
        print(ctx.author.created_at)
    guild = ctx.get_guild()
    embed = Embed(title='Userinfo für {}'.format(member),
                  description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                  color=0x22a7f0)
    all_roles = ""
    roles = member.get_roles()
    for role in roles:
        if role.id != guild.id:
            all_roles += '{} \r\n'.format(role.mention)
    if all_roles:
        embed.add_field(name="Rollen", value=all_roles, inline=True)
    embed.set_thumbnail(member.avatar_url)
    joined_at = int(member.joined_at.timestamp())
    created_at = int(member.created_at.timestamp())
    embed.add_field(name='Server beigetreten', value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
                    inline=True)
    embed.add_field(name='Discord beigetreten', value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
                    inline=True)
    lb = Leveling.get_leaderboard(users_json=users_json)
    place = 1
    for list1 in lb:
        if list1[0] == member.id:
            xp = int(list1[1])
            level = int(xp ** (1 / 3))
            break
        else:
            place += 1
    rank = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:"}
    for x in rank:
        if x == place:
            place = rank.get(x)
    embed.add_field(name="Leveling:", value=f"Rank: {place}.\r\n"
                                            f"Experience: {xp}exp\r\n"
                                            f"Level: {int(level)}")
    embed.set_footer(text='hehe fishiis und so')
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option("member", "The member you want information about", type=hikari.Member, required=False)
@lightbulb.command(name="avatar", aliases=("pb", "pfp", "pfb", "Avatar"),
                   description="Gives you some information about a member or yourself")
@lightbulb.implements(commands.PrefixCommand)
async def command_avatar(ctx: lightbulb.context.PrefixContext):
    user = ctx.options.member
    if not user:
        avatar = ctx.author.avatar_url
    else:
        avatar = user.avatar_url
    await ctx.respond(avatar)


@plugin.command
@lightbulb.command(name="ping", description="Gives you some information about a member or yourself")
@lightbulb.implements(commands.PrefixCommand)
async def command_ping(ctx: lightbulb.context.PrefixContext):
    await ctx.respond(f"Pong! {(ctx.bot.heartbeat_latency * 1000):2f}ms")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")
