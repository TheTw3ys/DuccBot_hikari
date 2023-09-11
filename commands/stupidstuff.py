import time
import hikari
import lightbulb
from hikari import Embed
from lightbulb import commands
import random
import requests
import json

plugin = lightbulb.Plugin(name="StupidStuff", description="Some things I came up with dunno")


@plugin.command
@lightbulb.option("reason", "The reason why you want to hit someone", type=str, required=False,
                  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name="member", type=hikari.Member, description="The member you want to slap")
@lightbulb.command(name="slap", description="Slaps someone", guilds=[911288030210428938, 715208493237403731])
@lightbulb.implements(commands.PrefixCommand)
async def command_slap(ctx: lightbulb.context.PrefixContext):
    reason = ctx.options.reason
    member = ctx.options.member

    embed = Embed(title="***SLAP***",
                  description=f"{member.mention} wurde von {ctx.member.mention} geslapt!",
                  color=0x22a7f0)
    embed.add_field(name="Grund:", value=reason)
    if member != ctx.author:
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("Warum schlägst du dich selbst?")


@plugin.command
@lightbulb.option("text", type=str, description="Some text you can add", required=False,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name="member", type=hikari.Member, description="The member you want to slap")
@lightbulb.command(name="claim", description="Claims someone")
@lightbulb.implements(commands.PrefixCommand)
async def command_claim(ctx: lightbulb.context.PrefixContext):
    args = ctx.options.text
    member = ctx.options.member
    claim = Embed(title='Claim',
                  description=f'{member} wurde von {str(ctx.author.mention)} geclaimt',
                  color=0x22a7f0)

    await ctx.respond(embed=claim)
    if args:
        await ctx.respond(embed=Embed(description=f"Und was auch immer das hier noch sollte:\r\n```{args}```"))


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only | lightbulb.has_guild_permissions(hikari.Permissions.MENTION_ROLES))
@lightbulb.command(name="someone", description="Someone from the guild")
@lightbulb.implements(commands.PrefixCommand)
async def command_someone(ctx: lightbulb.context.PrefixContext):
    liste = []
    guild = await ctx.app.rest.fetch_guild(ctx.guild_id)
    for member in guild.get_members():
        liste.append(member)
    print(len(liste))
    member = random.choice(liste)
    member = await ctx.app.rest.fetch_member(user=member, guild=ctx.guild_id)
    await ctx.respond(f"{member.mention}>")


@plugin.command
@lightbulb.command(name="inspire", description="Gives ")
@lightbulb.implements(commands.PrefixCommand)
async def command_inspire(ctx: lightbulb.context.PrefixContext):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    embed = Embed(title=f"Quote for {ctx.member.nickname}", description=quote)

    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option(name="Seconds", description="The seconds. Must be Integers.", type=str, required=True)
@lightbulb.command(name="timer", description="Starts a timer")
@lightbulb.implements(commands.PrefixCommand)
async def timer(ctx: lightbulb.context.PrefixContext):
    timesecond = ctx.options.Seconds
    try:
        timeseconds = int(timesecond)
        timer_msg = await ctx.respond(f'**{timeseconds}** seconds remaining!')
        while timeseconds != 0:
            time.sleep(1)
            timeseconds -= 1
            await timer_msg.edit(content=f'**{timeseconds}** seconds remaining!')

        await timer_msg.edit(f'{ctx.author.mention} **TIMER ENDED!!!**')
    except ValueError:
        await ctx.respond('Sorry, it must be a number!')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
