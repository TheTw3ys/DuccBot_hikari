import hikari
import lightbulb
import os
import datetime
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
    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)}/{count} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")



def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
os.chdir("..")
