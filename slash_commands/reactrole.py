import hikari
import lightbulb
import os
from hikari import Embed
import pymongo
db_url= os.getenv("DB_URL")
client = pymongo.MongoClient(db_url)

plugin = lightbulb.Plugin(name="Reactrole")
db = client["DuccBotInfo"]
collection = db["reactionroles"]

@plugin.command
@lightbulb.add_checks(
    lightbulb.checks.owner_only | lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_ROLES)
    )
@lightbulb.option("text", type=str, description="Some text you can add")
@lightbulb.option("role", type=hikari.Role, description="The Role the member should get")
@lightbulb.option("emoji", type=hikari.Emoji, description="The Emoji on which will be reacted")
@lightbulb.option("channel", type=hikari.GuildChannel, description="The channel if you want to send it there",
                  required=False)
@lightbulb.command(name="reactrole",
                   description="Erstellt eine Nachricht mit der man durch reagieren eine Rolle bekommt")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def command_reactrole(ctx: lightbulb.context.SlashContext):
    message = ctx.options.text
    role: hikari.Role = ctx.options.role
    emoji: hikari.Emoji = ctx.options.emoji
    channel: hikari.GuildChannel = ctx.options.channel
    ctx_channel: hikari.GuildChannel = ctx.get_channel()

    if not channel:
        channel: hikari.PartialChannel = ctx.get_channel()

    reaction_embed = Embed(description=message)

    msg = await plugin.app.rest.create_message(channel=channel, embed=reaction_embed)

    await msg.add_reaction(emoji)

    new_obj = {'role_name': role.name,
               'role_id': role.id,
               'emoji': emoji,
               'guild_name': ctx.get_guild().name,
               '_id': msg.id}

    collection.insert_one(new_obj)

    if channel != ctx.get_channel():
        await ctx.respond(f"The Reaction-Message was created at {channel.mention}")


"""
REACTION_ADD AND REACTION_REMOVE GET HANDLED BY COMMANDS/REACTROLE.py
"""


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
