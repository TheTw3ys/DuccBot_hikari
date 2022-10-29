import json
import os
import sys

import hikari
import lightbulb
from hikari import Embed

os.chdir(os.getcwd() + "/storage")
sys.path.append(f"{os.getcwd()}")  # adds folder "/storage" to sys.path temporarily

reactrole_json = str(os.path.join(os.getcwd(), "reactrole.json"))  # makes path availabile for Linux and Windows

plugin = lightbulb.Plugin(name="Reactrole")


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

    with open(reactrole_json) as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
                          'role_id': role.id,
                          'emoji': emoji,
                          'message_id': msg.id}

        data.append(new_react_role)

    with open(reactrole_json, 'w') as f:
        json.dump(data, f, indent=4)

    if channel != ctx.get_channel():
        await ctx.respond(f"The Reaction-Message was created at {ctx_channel.mention}")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
