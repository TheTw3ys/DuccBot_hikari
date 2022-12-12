import hikari
import lightbulb
from hikari import Embed
import json
import os
os.chdir(os.getcwd() + "/storage")


plugin = lightbulb.Plugin(name="Reactrole")
reactrole_json = str(os.path.join(os.getcwd(), "reactrole.json"))  # makes path availabile for Linux and Windows
@plugin.command
@lightbulb.add_checks(
    lightbulb.checks.owner_only | lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_ROLES)
    )
@lightbulb.option("text", type=str, description="Some text you can add",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("role", type=hikari.Role, description="The Role the member should get")
@lightbulb.option("emoji", type=hikari.Emoji, description="The Emoji on which will be reacted")
@lightbulb.command(name="reactrole",
                   description="Erstellt eine Nachricht mit der man durch reagieren eine Rolle bekommt")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_reactrole(ctx: lightbulb.context.PrefixContext):
    message = ctx.options.text
    role = ctx.options.role
    emoji = ctx.options.emoji
    reaction_embed = Embed(description=message)
    msg = await ctx.respond(embed=reaction_embed)
    msg = await msg.message()
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


@plugin.listener(event=hikari.GuildReactionAddEvent)
async def reaction_add(event: hikari.GuildReactionAddEvent):
    with open(reactrole_json) as react_file:
        if event.member == hikari.PartialUser.is_bot:
            print("Ein Bot hat anscheinend reagiert")
        else:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == event.message_id and x['emoji'] == event.emoji_name:
                    # checks if the found member id is equal to the id from the
                    # checks if the found emoji is equal to the reacted emoji
                    # message where a reaction was added
                    member = event.member

                    await member.add_role(int(x['role_id']),
                                          reason="reactionrole")  # gives the member who reacted the role


@plugin.listener(event=hikari.GuildReactionDeleteEvent)
async def reaction_remove(event: hikari.GuildReactionDeleteEvent):
    with open(reactrole_json) as react_file:
        data = json.load(react_file)
        for x in data:
            if x['message_id'] == event.message_id and x['emoji'] == event.emoji_name:

                await event.app.rest.remove_role_from_member(guild=event.guild_id, role=x["role_id"],
                                                             user=event.user_id)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)

os.chdir("..")
