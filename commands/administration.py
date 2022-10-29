import hikari
import lightbulb
from hikari.permissions import Permissions
import sys
import os
os.chdir(os.getcwd() + "/storage")

sys.path.append(f"{os.getcwd()}")

from functions_and_classes import Administration

plugin = lightbulb.Plugin(name="StupidStuff", description="Some things I came up with dunno")


@plugin.command()
@lightbulb.add_checks(
    lightbulb.checks.owner_only | lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_ROLES))
# @lightbulb.option(name="channel", type=hikari.GuildChannel,
#                  description="The channel, if you only want to mute them there", required=False)
# @lightbulb.option(name="time", type=int, description="The time, in minutes", required=True)
@lightbulb.option(name="member", type=hikari.Member, description="The member you want to slap")
@lightbulb.command(name="mute", description="Mutes a member")
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_mute(ctx: lightbulb.context.PrefixContext):
    member: hikari.Member = ctx.options.member
    guild = ctx.get_guild()
    muted_role: hikari.Guild.Role = Administration.get_role(server=guild, name="muted")
    print(muted_role)
    if muted_role is None:
        muted_role = await plugin.bot.rest.create_role(guild=guild, name="muted", permissions=None)
        overwrite = hikari.PermissionOverwrite(

            type=hikari.PermissionOverwriteType.ROLE,
            id=muted_role.id,
            allow=(
                    Permissions.VIEW_CHANNEL
                    | Permissions.READ_MESSAGE_HISTORY
            ),
            deny=(
                    Permissions.MANAGE_MESSAGES
                    | Permissions.SPEAK | Permissions.SEND_MESSAGES))

        for x in guild.get_channels():
            channel = guild.get_channel(x)
            await channel.edit(permission_overwrites=overwrite)
    # TODO overwrite doesnt work in loop
    await member.add_role(muted_role)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")
