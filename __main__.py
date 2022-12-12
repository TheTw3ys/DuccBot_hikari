from lightbulb import commands
import lightbulb
import hikari
import json
import os
import time

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')



# noinspection PyTypeChecker
bot = lightbulb.BotApp(token=token, prefix="!!", intents=hikari.Intents.ALL)

bot.load_extensions_from("./commands")
bot.load_extensions_from("./slash_commands")


@bot.command()
@lightbulb.add_checks(lightbulb.owner_only | lightbulb.has_roles(715209651326812180))
@lightbulb.command(name="reload", description="reload extensions")
@lightbulb.implements(commands.PrefixCommand)
async def reload_extensions(ctx: lightbulb.context.PrefixContext):
    if len(bot.extensions) != 0:
        await ctx.respond("Unloaded all extensions")
        bot.reload_extensions()
        time.sleep(1)
    else:

        bot.load_extensions_from("./commands")
        bot.load_extensions_from("./slash_commands")

    await ctx.respond("Loaded all extensions from ./commands and ./slash_commands")


@bot.command()
@lightbulb.add_checks(lightbulb.owner_only | lightbulb.has_roles(715209651326812180))
@lightbulb.option("extensions", type=str, description="The extensions to unload",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("type", type=str, description="Prefix or SlashCommands")
@lightbulb.command(name="unload", description="reload extensions")
@lightbulb.implements(commands.PrefixCommand)
async def unload_extensions(ctx: lightbulb.context.PrefixContext):
    args = ctx.options.extensions
    plugin = ctx.options.type
    args = args.split(" ")
    x = 0
    await ctx.respond(f"If you didn't unload a plugin see !help for the name of the plugin ")
    for _ in args:
        x += 1
    for y in range(x - 1):
        if plugin.lower() == "slash":
            print(args)
            bot.unload_extensions(f"slash_commands.{args[(y + 1)].lower()}")
            print(f"commands.{args[y]}")
        if plugin.lower() == "prefix":
            print(args)
            bot.unload_extensions(f"commands.{args[(y + 1)].lower()}")
        await ctx.respond(f"Removed Plugin {str(args[(y + 1)])}")
        print(bot.extensions)


@bot.command()
@lightbulb.add_checks(lightbulb.owner_only | lightbulb.has_roles(715209651326812180))
@lightbulb.option("extensions", type=str, description="The extensions to unload",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("plugin", type=str, description="Prefix or SlashCommands")
@lightbulb.command(name="load", description="reload extensions")
@lightbulb.implements(commands.PrefixCommand)
async def load_extensions(ctx: lightbulb.context.base.Context):
    args = ctx.options.extensions
    args = args.split(" ")
    plugin = ctx.options.plugin
    x = 0
    for _ in args:
        x += 1
    for y in range(x - 1):
        if plugin.lower() == "slashcommand":
            print(args)
            bot.load_extensions(f"slash_commands.{args[(y + 1)].lower()}")
            print(f"commands.{args[y]}")
        if plugin.lower() == "prefixcommand":
            print(args)
            bot.load_extensions(f"commands.{args[(y + 1)].lower()}")
        await ctx.respond(f"Added Plugin {str(args[(y + 1)])}")
        print(bot.extensions)


if os.name != "nt":
    # noinspection PyUnresolvedReferences
    import uvloop

    uvloop.install()
    print("loaded uvloop")

if __name__ == "__main__":
    print(bot.extensions)
    print(bot.plugins)
    bot.run()
