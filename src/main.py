# -*- coding: utf-8 -*-

import sys

import validators

import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context

from Data.Cache.settings import PREFIX
from Data.permission import Permission
from Data.pool import AllocatedPool

from Core.beak import Beak

from Tools.Utils import printer

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=PREFIX.__getitem__(0),
    intents=Intents.all()
)

beak: Beak


def booting(info: dict):
    from Core.Errors.errors import BeakErrors

    print("=" * 80 + f"\nBooting Beak...")

    try:
        global beak

        beak = Beak(__name__, **info)
        fmsg = f"(Bot_id: {info.get('__id__')}, name: {info.get('__name__')})"

        print(f"Allocated beak {fmsg}")

    except BeakErrors.UnAuthorizedModuleException as ERO:
        printer.print_ERO(ERO)
        
        sys.exit(0)


def registring():
    from Data.Errors.exceptions import PermissionExceptions

    print(f"----- On permission beak now -----")

    try:
        Permission.register()

        print(f"Permission granted (Admin_ID: {Permission.get_admin_id()})")
        print(f"----------------------------------")
    except (
        PermissionExceptions.ReRegistrationException, 
        PermissionExceptions.RequiredAllocationException
    ) as ERO:
        # TODO: Handling exception
        printer.print_ERO(ERO)

        sys.exit(0)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    await bot.change_presence(activity=discord.Game(name="TB"))

    _info = {
        "__id__": bot.user.id,
        "__name__": bot.user.name
    }
    
    booting(_info)
    registring()

    AllocatedPool()






if __name__ == "__main__":
    from Tools.Extractor.file_extractor import read_token

    __token: str = read_token()

    if __token:
        bot.run(__token)
    else:
        sys.exit(0)