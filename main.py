import sys

from typing import Optional

import discord
import validators
import youtubesearchpython

from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context

from Admin.Private.manager import Manager
from Admin.DSC.dsc import DSC
from Admin.DSC.debugger import Debugger

from Tools.Functions.function import (
    CommandNotification,
    BeakNotification
)

from Core.Cache.storage import Storage
from Core.Utils.utils import Selection
from Core.beak import Beak





LOGGING = True
PATCHING = False

__version__ = "v3.2.4.02"
__patch_version__ = "v3.2.5"

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

    if PATCHING:
        await bot.change_presence(
            activity = discord.Game(
            name = f"업데이트(버전: {__patch_version__})"
            )
        )
    else:
        await bot.change_presence(
            activity = discord.Activity(
                type = discord.ActivityType.listening,
                name = f"{DEFAULT_COMMAND_PREFIX}도움"
            )
        )

    Storage.Identification().set_beak_id(bot.user.id)
    Storage.Identification().set_admin_ids(administrator_identifications)



# deprecated 2023-02-24
#
# @bot.event
# async def on_command_error(ctx: Context, e: Exception):
#     if isinstance(e, commands.errors.MissingRequiredArgument):
#         command_name: str = ctx.command.name

#         if command_name.__eq__("bplay"):
#             await CommandNotification.Error.notice_missing_required_arguments(ctx=ctx)



@bot.command(aliases=["play", "p", "P", "재생", "제로"])
async def bplay(ctx: Context, *args) -> None:
    await ctx.message.delete()

    if PATCHING:
        if not Storage.Identification().is_admin(ctx.author.id):
            await beak.beak_patching(
                ctx=ctx, 
                prev_version=__version__, 
                updated_version=__patch_version__
            )

            return

    if len(args) == 0:
        await CommandNotification.Error.notice_missing_required_arguments(ctx=ctx)

        return

    if validators.url(args.__getitem__(0)):
        URL = args.__getitem__(0)

    else:
        # deprecated 2023-02-09
        # await CommandNotification.Error.notice_unvalid_url(ctx=ctx)

        query: str = " ".join(args)

        video = youtubesearchpython.VideosSearch(query=query, limit=1)
        result: list = video.result().get("result")
        component: dict = result.__getitem__(0)
        URL: str = component.get("link")
        title: str = component.get("title")

        await BeakNotification.Playlist.notice_video_founded(metadata=ctx, title=title)

    await beak.beak_play(ctx=ctx, URL=URL)


@bot.command(aliases=["reset", "리셋", "초기화"])
async def breset(ctx: Context) -> None:
    await ctx.message.delete()

    if PATCHING:
        if not Storage.Identification().is_admin(ctx.author.id):
            await beak.beak_patching(
                ctx=ctx, 
                prev_version=__version__, 
                updated_version=__patch_version__
            )

            return

    await beak.beak_player_reset(ctx=ctx)


@bot.command(aliases=["exit", "퇴장"])
async def bexit(ctx: Context) -> None:
    await ctx.message.delete()

    if PATCHING:
        if not Storage.Identification().is_admin(ctx.author.id):
            await beak.beak_patching(
                ctx=ctx, 
                prev_version=__version__, 
                updated_version=__patch_version__
            )

            return

    await beak.beak_player_exit(ctx=ctx)




# Utility Section
@bot.command(aliases=["팀짜기"])
async def bteaming(ctx: Context) -> None:
    await Selection.random_teaming(ctx=ctx)


@bot.command(aliases=["사다리", "몰가"])
async def bladder(ctx: Context, *args) -> None:
    await Selection.random_ladder(ctx=ctx, options=args)




@bot.command(aliases=["명령어", "도움"])
async def bhelp(ctx: Context) -> None:
    await ctx.message.delete()

    if PATCHING:
        if not Storage.Identification().is_admin(ctx.author.id):
            await beak.beak_patching(
                ctx=ctx, 
                prev_version=__version__, 
                updated_version=__patch_version__
            )

            return

    embed = discord.Embed(
        title="🐼 재생 명령어 🐼", 
        description = f"{DEFAULT_COMMAND_PREFIX}p (음원주소 또는 검색어)",
        color = 0x6b82f5
    )

    embed.add_field(
        name = "퇴장 명령어: ~exit 또는 ~퇴장",
        value = "Beak를 강제로 퇴장시킵니다.",
        inline = False
    )

    embed.add_field(
        name = "리셋 명령어: ~reset 또는 ~리셋",
        value = "현재 재생 중인 음원을 제외한 모든 대기열을 초기화합니다.",
        inline = False
    )

    embed.add_field(
        name = "팀짜기 명령여: ~teaming 또는 ~팀짜기",
        value = "현재 유저가 입장한 음성 채널을 기준으로 두 팀으로 랜덤하게 나눕니다.",
        inline = False
    )

    # deprecated 2023-02-24
    #
    # embed.add_field(
    #     name = "버튼:  🔄️",
    #     value = "현재 재생 중인 음원을 제외한 모든 대기열을 초기화합니다.",
    #     inline = False
    # )

    # embed.add_field(
    #     name = "버튼:  🗑️",
    #     value = "다음 대기 중인 음원 1개를 삭제합니다.",
    #     inline = False
    # )

    # embed.add_field(
    #     name = "버튼:  📜",
    #     value = "현재 재생 중인 음원을 기준으로 재생 완료된 음원 2개, 대기 중인 음원 2개를 출력합니다.",
    #     inline = False
    # )

    # embed.add_field(
    #     name = "버튼:  🛠️  ( 버그 발견 및 해결 중 → 버튼 임시 비활성화 )",
    #     value = "플레이어가 버그에 걸리거나 오류 발생 시 현상을 해결한 후 재입장시킵니다.",
    #     inline = False
    # )

    embed.set_footer(
        text = "Beak By Qbean"
    )

    await ctx.send(embed=embed)


@bot.command(aliases=["extract"])
async def bextract(ctx: Context, url: str) -> None:
    await ctx.message.delete()

    await Debugger.debug_youtube_dl_extractor(URL=url)



@bot.command(aliases=[f"{ADMINISTRATOR_COMMAND_PREFIX}sudo"])
async def execute_DSC(ctx: Context, *args):
    if Storage.Identification().is_admin(ctx.author.id):
        commands: str = args.__getitem__(0)

        if commands == "-n" or commands == "--notice":
            try:
                channel = bot.get_channel(int(args.__getitem__(1)))

                await channel.send(f"{' '.join(args[2:])}")

            except Exception as e:
                print(e)
                print(e.__doc__)
        
        elif commands == "-c" or commands == "--context-extractor":
            Debugger.debug_context_extractor(ctx=ctx)

        elif commands == "diagnose" or commands == "--diagnose-self":
            # print(ctx.)
            ...

        elif commands == "-m" or commands == "--get-members":
            members = ctx.author.voice.channel.members

            for member in members:
                print(f"{member.name}: {member.id}")

    else:
        await DSC.Supervisor.notice_not_authorized_user(metadata=ctx)


def main():
    if DEFAULT_COMMAND_PREFIX is not None and ADMINISTRATOR_COMMAND_PREFIX is not None:
        bot.run(configuration.get("TOKEN"))

    else:
        sys.stderr.write("Missing value in config\n")
        sys.stderr.write("Configuration must have values 'TOKEN', \
                         'DEFAULT_COMMAND_PREFIX' and 'ADMINISTTRATOR_COMMAND_PREFIX'")

        sys.exit(1)



if __name__ == "__main__":
    try:
        patch_argv: str = sys.argv[1]

        if patch_argv.__eq__("patch"):
            PATCHING = True
    except IndexError:
        ...
    finally:
        # PPRM
        main()