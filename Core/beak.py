from typing import (
    Dict, List, Optional
)

import asyncio
import discord

from discord import Embed, FFmpegPCMAudio
from discord.voice_client import VoiceClient
from discord.ext.commands.context import Context, Message

from Class.superclass import *

from Admin.DSC.dsc import DSC, Logger

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.storage import Storage
from Core.Cache.Queue.queue import AsyncQueue

from Core.Errors.error import BeakError, AsyncQueueError

from Tools.Functions.function import BeakNotification, CommandNotification

from Utils.extractor import (
    ContextExtractor,
    YoutubeDlExtractor,
)

from Data.Paraments.settings import (
    PLAYLIST_NOTICE_EMBED_COLOR, 
    DEFAULT_DELAY,
    SLEEP_TIME,
    FFMPEG_OPTION
)


class BeakInspector(Block.Instanctiating):
    @staticmethod
    def coro_commander_inspection():
        def _decof(func):
            async def wrapper(*args, **kwargs):
                ctx: Context
                
                if "ctx" in kwargs.keys():
                    ctx = kwargs.get("ctx")
                else:
                    ctx = args.__getitem__(1)
                    
                if ContextExtractor.is_author_joined_voice_channel(ctx):
                    if ContextExtractor.is_beak_joined_voice_channel(ctx):
                        if ContextExtractor.is_beak_and_author_same_voice_channel(ctx):
                            await func(*args, **kwargs)
                            
                        else:
                            await BeakNotification.Error.notice_not_same_channel(ctx)
                        
                    else:
                        await BeakNotification.Error.notice_beak_not_entered_channel(ctx)

                else:
                    await BeakNotification.Error.notice_author_not_entered_channel(ctx)
            
            return wrapper
        return _decof
    


class Beak(metaclass=Singleton):
    __slots__ = (
        "player_pool",
    )


    def __init__(self) -> None:
        self.player_pool: PlayerPool = PlayerPool()


    def __alloc_pool__(self, guild_id: int, voice_client: VoiceClient) -> None:
        if guild_id in self.player_pool:
            # deprcated 2023-02-23 
            #
            # player: Player = self.player_pool.__getitem__(guild_id)
            #
            # raise BeakErrors.AlreadyAllocatedGuildId(
            #     guild_id = guild_id,
            #     is_connected = player.is_connected,
            #     is_activated = player.is_activated,
            #     is_msg_saved = player.is_message_saved
            # )

            raise BeakError.AllocatedIdentificationError

        
        _player = Player(
            voice_client = voice_client,
            message_storage = Storage.Message(guild_id=guild_id),
            queue = AsyncQueue.Queue(),
            over_queue = AsyncQueue.OverQueue()
        )
        
        self.player_pool.__setitem__(guild_id=guild_id, player=_player)
        

    def __discard_pool__(self, guild_id) -> None:
        self.player_pool.__delitem__(guild_id)


    def __get_guild_player(self, guild_id: int) -> Player:
        try:
            return self.player_pool.__getitem__(guild_id)
        
        except ValueError:
            raise BeakError.UnallocatedIdentificationError
        
    
    async def __discard_player(self, ctx: Context, guild_id: int, guild_player: Player) -> None:
        await BeakNotification.Playlist.discard(metadata=ctx, player=guild_player)

        self.__discard_pool__(guild_id=guild_id)

    
    def DSC_get_guild_player(self, guild_id) ->Optional[Player]:
        raise NotImplementedError


    # deprecated 2023-02-24
    #
    # def is_beak_already_entered_channel(self, guild_id: int) -> bool:
    #     return guild_id in self.player_pool


    async def __ytdl_executor(self, URL: str, Debug=False) -> List[Dict[str, str]]:
        data = await YoutubeDlExtractor.extract(URL=URL, DEBUG=Debug)
        
        return data


    async def extract(self, ctx: Context, URL: str) -> List[Dict[str, str]]:
        __em: Optional[Message] = None
        
        if "playlist" in URL:
            _embed = Embed(
                title = "플레이리스트 추출 및 변환 중...", 
                color = PLAYLIST_NOTICE_EMBED_COLOR
            )

            _embed.set_footer(text="Beak by Qbean")

            __em = await ctx.send(embed=_embed)

        audios = await self.__ytdl_executor(URL=URL)

        if __em is not None:
            message = "추출 및 변환 완료.\n"
            message += f"플레이리스트 제목: {audios.__getitem__(-1).get('playlist_title')} | "
            message += f"음원 수: {len(audios)}"

            _embed = Embed(
                title = "추출 및 변환 완료", 
                color = PLAYLIST_NOTICE_EMBED_COLOR
            )

            _embed.add_field(name="플레이리스트 제목", value=f"{audios.__getitem__(-1).get('playlist_title')}", inline=True)
            _embed.add_field(name="음원 수", value=f"{len(audios)}개", inline=True)
        
            _embed.set_footer(text="Beak by Qbean")

            await __em.edit(embed=_embed, delete_after=DEFAULT_DELAY * 2)

        return audios


    async def beak_enter(self, ctx: Context) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx=ctx)
        voice_channel = ContextExtractor.get_author_entered_voice_channel(ctx=ctx)
    
        try:
            voice_client = await voice_channel.connect(self_deaf=True)

            self.__alloc_pool__(guild_id=guild_id, voice_client=voice_client)

        except discord.errors.ClientException:
            await CommandNotification.Error.notice_already_connected(ctx=ctx)
            
        except BeakError.AllocatedIdentificationError:
            await DSC.Controller.dismantle_player(
                identification=guild_id, 
                player=self.player_pool.__getitem__(guild_id=guild_id)
            )

            DSC.Controller.allocate_player(identification=guild_id, voice_client=voice_client)        
 

    async def beak_exit(self, ctx: Context) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx)

        guild_player = self.__get_guild_player(guild_id)

        if guild_player.is_connected:
            await guild_player.voice_client.disconnect()

        await self.__discard_player(ctx=ctx, guild_id=guild_id, guild_player=guild_player)


    async def beak_play(self, ctx: Context, URL: str) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx)

        if ContextExtractor.is_beak_joined_voice_channel(ctx=ctx):
            if not ContextExtractor.is_beak_and_author_same_voice_channel(ctx=ctx):
                await BeakNotification.Error.notice_not_same_channel(metadata=ctx)

                return
            
        else:
            if not ContextExtractor.is_author_joined_voice_channel(ctx=ctx):
                await BeakNotification.Error.notice_author_not_entered_channel(metadata=ctx)

                return
                
            await self.beak_enter(ctx=ctx)

        try:
            audios = await self.extract(ctx=ctx, URL=URL)

            guild_player = self.__get_guild_player(guild_id)
            guild_player.enqueue(audios=audios)

            await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

        except BeakError.UnallocatedIdentificationError as e:
            # TODO: Handling this section
            await Logger.EmbedNotification.notice_unallocated_guild_id(metadata=ctx, ero=e)

        except AsyncQueueError.SaturatedQueueError:
            # TODO: Handling this section
            await BeakNotification.Playlist.notice_saturated_queue(metadata=ctx)

        except Exception as e:
            print(e)

        if guild_player.is_playing or guild_player.is_paused: return

        while not guild_player.is_queue_empty:
            try:
                audio_source_url = guild_player.seek_queue.get("audio_url")

                guild_player.voice_client.play(FFmpegPCMAudio(audio_source_url, **FFMPEG_OPTION))

                await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

            except discord.errors.ClientException:
                await BeakNotification.Playlist.notice_playlist_is_ended(metadata=ctx)

                return

            while guild_player.is_playing or guild_player.is_paused:
                if not guild_player.is_connected:
                    await self.__discard_player(ctx=ctx, guild_id=guild_id, guild_player=guild_player)
                    
                    return

                await asyncio.sleep(SLEEP_TIME)

            else:
                if guild_player.is_connected:
                    if guild_player.is_voice_channel_empty:
                        await self.beak_exit(ctx=ctx)
                        
                        return

                    if not guild_player.is_repeat_mode:
                        try:
                            guild_player.dequeue()

                            if guild_player.is_loop_mode and guild_player.is_queue_empty:
                                guild_player.looping()

                                await BeakNotification.Playlist.notice_looping(metadata=ctx)

                            if not guild_player.is_queue_empty:
                                await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

                        except AsyncQueueError.SaturatedOverQueueError:
                            # TODO: Handling this section
                            await BeakNotification.Playlist.notice_saturated_overqueue(metadata=ctx)

        else:
            await BeakNotification.Playlist.notice_playlist_is_ended(metadata=ctx) 
            await self.beak_exit(ctx=ctx)    


    @BeakInspector.coro_commander_inspection()
    async def beak_player_reset(self, ctx: Context) -> None:
        guild_id: int = ContextExtractor.get_guild_id(ctx=ctx)
        guild_player: Player = self.player_pool.get(guild_id=guild_id)

        if guild_player.is_connected:
            guild_player.reset()

            await BeakNotification.Playlist.deploy(player=guild_player)
            await BeakNotification.Playlist.notice_reset_playlist(metadata=ctx)