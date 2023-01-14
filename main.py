import sys

from typing import Optional

import discord
import validators

from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context

from Admin.Private.manager import Manager
from Admin.DSC.debugger import Debugger

from Tools.Notices.notice import CommandNotification, AdminNotification

from Core.Cache.storage import Storage
from Core.beak import Beak

LOGGING = True

intents = Intents.default()
intents.members = True
intents.message_content = True

configuration = Manager.get_configuration(value="config", logging=LOGGING)
commands_config = Manager.get_configuration(value="commands", logging=LOGGING)
administrator_identifications = Manager.get_administrators(logging=LOGGING)

DEFAULT_COMMAND_PREFIX: Optional[str] = configuration.get("DEFAULT_COMMAND_PREFIX")
ADMINISTRATOR_COMMAND_PREFIX: Optional[str] = configuration.get("ADMINISTRATOR_COMMAND_PREFIX")

bot = commands.Bot(command_prefix=DEFAULT_COMMAND_PREFIX, intents=Intents.all())

beak: Beak



@bot.event
async def on_ready():
    global beak
    beak = Beak()

    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name=f"{DEFAULT_COMMAND_PREFIX}명령어"))

    Storage.Identification().set_beak_id(bot.user.id)
    Storage.Identification().set_admin_ids(administrator_identifications)


# @bot.event
# async def on_command_error(ctx: Context, e: Exception):
    
#     if isinstance(e, discord_command_errors.MissingRequiredArgument):
#         command_name: str = ctx.command.name

#         if command_name.__eq__("bplay"):
#             await CommandNotification.Error.notice_missing_required_arguments(ctx=ctx)


# @bot.event
# async def on_button_click(interaction: Interaction):
#     await interaction.response.send_message("Hi")





@bot.command(aliases=["btn"])
async def btntest(ctx: Context) -> None:
    await ctx.message.delete()

    await Beak.beak_button_test(ctx=ctx)




@bot.command(aliases=commands_config.get("bplay"))
async def bplay(ctx: Context, URL: str) -> None:
    await ctx.message.delete()

    if validators.url(URL):
        await beak.beak_play(ctx=ctx, URL=URL)

    else:
        await CommandNotification.Error.notice_unvalid_url(ctx=ctx)


@bot.command(aliases=commands_config.get("bskip"))
async def bskip(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_skip(ctx=ctx)


@bot.command(aliases=commands_config.get("bprev"))
async def bprev(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_prev(ctx=ctx)


@bot.command(aliases=commands_config.get("bpause"))
async def bpause(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_pause(ctx=ctx)


@bot.command(aliases=commands_config.get("breplay"))
async def breplay(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_replay(ctx=ctx)


@bot.command(aliases=commands_config.get("bloop"))
async def bloop(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_loop(ctx=ctx)


@bot.command(aliases=commands_config.get("blist"))
async def blist(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_heavy_playlist(ctx=ctx)


@bot.command(aliases=commands_config.get("bshuffle"))
async def bshuffle(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_shuffle(ctx=ctx)


@bot.command(aliases=commands_config.get("bremove"))
async def bremove(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_remove(ctx=ctx)


@bot.command(aliases=commands_config.get("bexit"))
async def bexit(ctx: Context) -> None:
    await ctx.message.delete()

    await beak.beak_exit(ctx=ctx)



@bot.command(aliases=[f"{ADMINISTRATOR_COMMAND_PREFIX}sudo"])
async def execute_DSC(ctx: Context, *args, **kwargs):
    raise NotImplementedError

    # if Storage.Identification().is_admin(ctx.author.id):
    #     ...

    # else:
    #     await AdminNotification.Admin.notice_not_authorized_user(ctx=ctx)


def main():
    if DEFAULT_COMMAND_PREFIX is not None and ADMINISTRATOR_COMMAND_PREFIX is not None:
        bot.run(configuration.get("TOKEN"))

    else:
        sys.stderr.write("Missing value in config\n")
        sys.stderr.write("Configuration must have values 'TOKEN', 'DEFAULT_COMMAND_PREFIX' and 'ADMINISTTRATOR_COMMAND_PREFIX'")

        sys.exit(1)



if __name__ == "__main__":
    main()