import json
import os
import sys

import hikari
import lightbulb

os.chdir(os.getcwd() + "/storage")  # changes directory to ./v2/storage

# adds folder "/storage" to sys.path temporarily
sys.path.append(f"{os.getcwd()}")

plugin = lightbulb.Plugin(name="When I say you say...",
                          description="Some things I came up with dunno")

# makes path available for Linux and Windows
trigger_list = str(os.path.join(os.getcwd(), "triggers.json"))


class AlreadyTrigger(Exception):
    pass


@plugin.listener(hikari.MessageCreateEvent)  # TODO Write this better
async def on_message(event: hikari.MessageCreateEvent):
    msg = event.content
    r_guild = await event.app.rest.fetch_guild(event.message.guild_id)
    if event.is_human and "!!" not in msg:
        if "if i say" in msg:
            def split_message(message, guild):
                # splits message to ['when i say this ', ' that']
                liste = message.split("you say")
                you_say = str(liste[1]).strip()  # thing that is reacted to

                liste_2 = str(liste[0]).strip().split("if i say")
                when_i_say = str(liste_2[1]).strip()  # trigger
                when_i_say_data = {f"{when_i_say}": f"{you_say}"}  # data
                if not os.path.exists(trigger_list):
                    with open(trigger_list,
                              "w") as a:  # possible because it is the same as above but now actually created
                        a.write('{'
                                '"guilds":{'
                                '}'
                                '}')
                with open(trigger_list) as f:
                    data: dict = json.load(f)

                    if guild in data["guilds"]:  # if guild_id in storage
                        # if the trigger already registered
                        if when_i_say in data["guilds"][guild]:
                            raise AlreadyTrigger

                        # just update the triggers of the guild_id
                        data["guilds"][guild].update(when_i_say_data)
                    else:
                        data["guilds"].update(
                            {guild: when_i_say_data})  # add new guild_id to storage and first triggers

                with open(trigger_list, 'w') as f:
                    # add new trigger and response
                    json.dump(data, f, indent=2)

            try:
                split_message(msg, str(r_guild.id))
                await event.message.respond("Added Trigger to database")
            except AlreadyTrigger:
                await event.message.respond("This is already a Trigger. Do you want to edit it?")
        else:
            msg = event.message.content
            with open(trigger_list, "r") as f:
                data = json.load(f)
                liste = []
                for id in data["guilds"]:
                    liste.append(id)
                if str(event.message.guild_id) in liste:
                    try:
                        data = data["guilds"][str(event.message.guild_id)]
                    except KeyError:
                        with open(trigger_list, "w") as d:
                            data = json.load(d)
                            data["guilds"].update({str(event.message.guild_id): {}})
                            json.dump(data, d, indent=2)
                    for trigger in data:
                        if trigger in msg:
                            answer = data.get(trigger)
                            await event.message.respond(f"{answer}")


@plugin.command
@lightbulb.option(name="rest", required=False, description="just so i dont get any errors",
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST, )
@lightbulb.command(name="triggers", description="Shows you the triggers of your guild")
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_show_triggers(ctx: lightbulb.context.PrefixContext):
    with open(trigger_list) as f:
        data: dict = json.load(f)
        guild = ctx.get_guild()
        string = "Triggers:\r\n"

        for trigger in data["guilds"][f"{guild.id}"]:
            value = data["guilds"][f"{guild.id}"].get(trigger)
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
    with open(trigger_list, "r") as f:
        data = json.load(f)
        if trigger in data["guilds"][str(guild.id)]:
            data["guilds"][str(guild.id)][trigger] = answer

        else:
            await ctx.respond(f"There is no trigger with the name: {trigger}")
            return
    with open(trigger_list, "w") as f:
        json.dump(data, f, indent=2)


@plugin.command
@lightbulb.option(name="trigger", description="The Trigger you want to edit", required=True, type=str,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command(name="trigger-delete", description="Edits a specific trigger in your guild",
                   aliases=["trigger-remove"])
@lightbulb.implements(lightbulb.commands.PrefixCommand)
async def command_delete_trigger(ctx: lightbulb.context.PrefixContext):
    trigger = ctx.options.trigger
    guild = ctx.get_guild()
    with open(trigger_list, "r") as f:
        data = json.load(f)
        if trigger in data["guilds"][str(guild.id)]:
            data["guilds"][str(guild.id)].pop(trigger)
            await ctx.respond(f"Removed Trigger: **{trigger}**")
        else:
            await ctx.respond("That trigger was not found. Maybe you misspelled it?")
    with open(trigger_list, "w") as f:
        json.dump(data, f, indent=2)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


os.chdir("..")
