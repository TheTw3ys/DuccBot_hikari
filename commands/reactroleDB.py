import hikari
import lightbulb
from hikari import Embed
import os
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
    new_obj = {'role_name': role.name,
               'role_id': role.id,
               'emoji': emoji,
               'guild_name': ctx.get_guild().name,
               '_id': msg.id}

    collection.insert_one(new_obj)


@plugin.listener(event=hikari.GuildReactionAddEvent)
async def reaction_add(event: hikari.GuildReactionAddEvent):
    if event.member.id == 715216302863548508 or event.member.id == 717349947858485268:
        pass
    else:
        obj = collection.find_one(filter={"_id": event.message_id})
        if event.emoji_name == obj["emoji"]:
            await event.member.add_role(int(obj["role_id"]),
                                        reason="reactionrole")


@plugin.listener(event=hikari.GuildReactionDeleteEvent)
async def reaction_remove(event: hikari.GuildReactionDeleteEvent):
    obj = collection.find_one(filter={"_id": event.message_id})
    if event.emoji_name == obj["emoji"]:
        await event.app.rest.remove_role_from_member(guild=event.guild_id, role=obj["role_id"],
                                                     user=event.user_id)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
