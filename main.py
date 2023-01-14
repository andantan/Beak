import sys

from typing import Optional

import discord
import validators

from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context

from Admin.Private.manager import Manager

from Tools.Functions.function import CommandNotification, AdminNotification

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


@bot.event
async def on_command_error(ctx: Context, e: Exception):
    if isinstance(e, commands.errors.MissingRequiredArgument):
        command_name: str = ctx.command.name

        if command_name.__eq__("bplay"):
            await CommandNotification.Error.notice_missing_required_arguments(ctx=ctx)



@bot.command(aliases=["play", "p", "재생"])
async def bplay(ctx: Context, URL: str) -> None:
    await ctx.message.delete()

    if validators.url(URL):
        await beak.beak_play(ctx=ctx, URL=URL)

    else:
        await CommandNotification.Error.notice_unvalid_url(ctx=ctx)


@bot.command(aliases=[f"{ADMINISTRATOR_COMMAND_PREFIX}sudo"])
async def execute_DSC(ctx: Context, *args):
    if Storage.Identification().is_admin(ctx.author.id):
        if args.__getitem__(0) == "-n" or args.__getitem__(0) == "--notice":
            await ctx.send(f"{args[1]}")

    else:
        await AdminNotification.Admin.notice_not_authorized_user(ctx=ctx)


def main():
    if DEFAULT_COMMAND_PREFIX is not None and ADMINISTRATOR_COMMAND_PREFIX is not None:
        bot.run(configuration.get("TOKEN"))

    else:
        sys.stderr.write("Missing value in config\n")
        sys.stderr.write("Configuration must have values 'TOKEN', 'DEFAULT_COMMAND_PREFIX' and 'ADMINISTTRATOR_COMMAND_PREFIX'")

        sys.exit(1)



if __name__ == "__main__":
    # PPRM
    main()
    