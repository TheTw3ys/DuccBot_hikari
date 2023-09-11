import os

import hikari
import lightbulb
import pymongo

host, port = os.getenv("DB_HOST"), int(os.getenv("DB_PORT"))
client = pymongo.MongoClient(host, port)

db = client["DuccBotInfo"]
plugin = lightbulb.Plugin(name="When I say you say...",
                          description="Some things I came up with dunno")
collection = db.get_collection("when_i_say")


class AlreadyTrigger(Exception):
    pass


class GuildNotFound(Exception):
    pass


@plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    msg = event.content
    guild = await event.app.rest.fetch_guild(event.message.guild_id)
    if event.is_human and "!!" not in msg and "_id" not in msg:
        if "when i say" in msg.lower():
            message_list = msg.split("you say")
            answer = str(message_list[1].strip())  # said thing
            trigger = str(message_list[0]).strip().split("when i say")[1].strip()  # trigger
            print(message_list, "\r\n", trigger, "\r\n", answer)

            try:
                data = collection.find_one(filter={"_id": guild.id})
                if not data:
                    raise GuildNotFound

                if trigger in dict(data):
                    raise AlreadyTrigger

            except GuildNotFound:
                collection.insert_one({"_id": guild.id})

            except AlreadyTrigger:
                await event.message.respond(f'"{trigger}" is already a Trigger.')

            collection.update_one(filter={"_id": guild.id}, update={"$set": {trigger: answer}})
            await event.message.respond(f'Added Trigger: "{trigger}" to Database')
        else:
            try:
                data = collection.find_one(filter={"_id": guild.id})
                print(data)
            except GuildNotFound:
                return
            for trigger in data:
                print(trigger)
                if trigger in msg:
                    await event.message.respond(f"{data[trigger]}")


@plugin.command
@lightbulb.option(name="rest", required=False, description="just so i dont get any errors",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, )
@lightbulb.command(name="triggers", description="Shows you the triggers of your guild")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_show_triggers(ctx: lightbulb.context.PrefixContext):
    guild = ctx.get_guild()
    data = collection.find_one(filter={"_id": guild.id})
    string = "Triggers:\r\n"

    for trigger in data:
        if trigger == "_id":
            continue
        value = data[trigger]
        string += f"when you say **{trigger}** i say: **{value}**\r\n"
    embed = hikari.Embed(title="Triggers")
    embed.add_field(value=string, name=f"For Guild: **{guild.name}** ")
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option(name="answer", required=False, description="The new answer",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, )
@lightbulb.option(name="trigger", description="The Trigger you want to edit", required=True, type=str)
@lightbulb.command(name="trigger-edit", description="Edits a specific trigger in your guild")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_edit_trigger(ctx: lightbulb.context.PrefixContext):
    trigger = ctx.options.trigger
    answer = ctx.options.answer
    guild = ctx.get_guild()
    data = collection.find_one(filter={"_id": guild.id})
    if trigger in data and trigger != "_id":
        collection.update_one(filter={"_id": guild.id}, update={"$set": {trigger: answer}})
        await ctx.respond(f'Changed answer for Trigger: "{trigger}" to "{answer}" ')
    else:
        await ctx.respond(f"There is no trigger with the name: {trigger}")
        return


@plugin.command
@lightbulb.option(name="trigger", description="The Trigger you want to edit", required=True, type=str,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command(name="trigger-delete", description="Edits a specific trigger in your guild",
                   aliases=["trigger-remove"])
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_delete_trigger(ctx: lightbulb.context.PrefixContext):
    trigger = ctx.options.trigger
    guild = ctx.get_guild()
    data = collection.find_one(filter={"_id": guild.id})
    if trigger in data:
        collection.update_one(filter={"_id": guild.id}, update={"$unset": {trigger: ""}})
        await ctx.respond(f"Removed Trigger: **{trigger}**")
    else:
        await ctx.respond("That trigger was not found. Maybe you misspelled it?")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
