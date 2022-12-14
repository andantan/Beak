# -*- coding: utf-8 -*-

import sys

import validators

import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context

from Data.Cache.settings import PREFIX as pf


intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=pf.__getitem__(0),
    intents=Intents.all()
)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=None)
    await bot.change_presence(activity=discord.Game(name="TB"))

    _info = {
        "__id__": bot.user.id,
        "__name__": bot.user.name
    }

    fmsg = f"(id: {_info.get('__id__')}, name: {_info.get('__name__')})"


    print("=" * 80 + f"\nBooting Beak...")
    print(f"Allocation beak {fmsg}")

    
    



if __name__ == "__main__":
    from Tools.Extractor.file_extractor import read_token

    __token: str = read_token()

    if __token:
        bot.run(__token)
    else:
        sys.exit(0)