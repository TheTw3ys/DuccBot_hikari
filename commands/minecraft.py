import requests
import hikari
import lightbulb

plugin = lightbulb.Plugin(name="Minecraft", description="Leveling")
guild_list = [699010600331771955, 911288030210428938, 715208493237403731]


@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option(name="ign", type=str, description="your Ingame Name", required=False)
@lightbulb.command(name="uuid", description="Gives you your UUID")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_ign(ctx: lightbulb.context.PrefixContext):
    ign = ctx.options.ign.strip()
    response = requests.request(url=f"https://minecraft-api.com/api/uuid/{ign}",method= "GET", timeout=20)
    await ctx.respond(hikari.Embed(description=response.text, color=0x22a7f0 ))


@plugin.command
@lightbulb.option("text", type=str, description="Why are you sending still something",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option(name="ip", type=str, description="your Ingame Name", required=False)
@lightbulb.command(name="server", description="Gives you your UUID")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_uuid(ctx: lightbulb.context.PrefixContext):
    ip = ctx.options.ip.strip()
    response = requests.request(url=f"https://minecraft-api.com/api/query/{ip}/{22565}", method= "GET", timeout=20)
    await ctx.respond(hikari.Embed(description=response.text, color=0x22a7f0 ))


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
