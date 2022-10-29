import hikari
from hikari import Embed
import lightbulb
from lightbulb import commands

plugin = lightbulb.Plugin(name="SlashCommands_StupidStuff", description="Yeah I dunno why I made those slashcommands")


@plugin.command
@lightbulb.option("reason", "The reason why you want to hit someone", type=str, required=False,
                  default="Es gab anscheinend keinen")
@lightbulb.option(name="member", type=hikari.User, description="The member you want to slap")
@lightbulb.command(name="slap", description="Slaps someone", guilds=[715208493237403731, 911288030210428938])
@lightbulb.implements(commands.SlashCommand)
async def slash_command_slap(ctx: lightbulb.context.SlashContext):
    reason = ctx.options.reason
    member = ctx.options.member
    embed = Embed(title="***SLAP***",
                  description=f"{member.mention} wurde von {ctx.member.mention} geslapt!",
                  color=0x22a7f0)
    embed.add_field(name="Grund:", value=reason)
    if member != ctx.member:
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("Warum schlägst du dich selbst?")


@plugin.command
@lightbulb.option(name="member", type=hikari.User,
                  description="The member you want to claim", required=False)
@lightbulb.command(name="claim", description="Claims someone",
                   guilds=[715208493237403731, 911288030210428938])
@lightbulb.implements(commands.SlashCommand)
async def slash_command_claim(ctx: lightbulb.context.SlashContext):
    member: hikari.User = ctx.options.member
    claim = Embed(title='Claim', color=0x22a7f0)
    if not member or member.id == ctx.member.id:
        await ctx.respond("Aren't you owning yourself already?")
        return

    if member:
        claim.description = f"{member} was claimed by {str(ctx.author.mention)}"
        await ctx.respond(embed=claim)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
