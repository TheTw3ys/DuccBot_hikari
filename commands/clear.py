import hikari
import lightbulb
import os

plugin = lightbulb.Plugin(name="Clear")
os.chdir(os.getcwd() + "/storage")

@plugin.command
@lightbulb.add_checks(
    lightbulb.checks.owner_only | lightbulb.checks.has_role_permissions(
        hikari.Permissions.MANAGE_MESSAGES | hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("text", type=str, description="Some text you can add",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("count", type=int, description="The amount of messages to delete", required=False)
@lightbulb.command(name="clear",
                   description="Deletes messages")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_clear(ctx: lightbulb.context.PrefixContext):
    count = int(ctx.options.count)
    channel = ctx.get_channel()
    await plugin.bot.rest.delete_messages(
        ctx.channel_id,
        await plugin.bot.rest.fetch_messages(ctx.channel_id).limit(count))
    await ctx.respond(f'Cleared {count} messages.')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
os.chdir("..")
