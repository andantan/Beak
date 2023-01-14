from typing import (
    Dict, List, Optional
)

import asyncio

from discord import Embed, FFmpegPCMAudio, ButtonStyle
from discord.ui import View, Button
from discord.voice_client import VoiceClient
from discord.ext.commands.context import Context, Message, Interaction

from Class.superclass import Singleton, Block

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.storage import Storage
from Core.Cache.Queue.queue import AsyncQueue
from Core.Cache.Queue.Errors.queue_error import AsyncQueueErrors

from Core.Errors.beak_error import BeakErrors

# from Tools.Decorators.decorator import BeakInspector
from Tools.Notices.notice import BeakNotification

from Utils.extractor import (
    ContextExtractor,
    YoutubeDlExtractor,
    InteractionExtractor
)

from Data.Paraments.settings import (
    PLAYLIST_NOTICE_EMBED_COLOR, 
    DEFAULT_DELAY,
    SLEEP_TIME
)


class Inspector(Block.Instanctiating):
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


    def __alloc_pool__(self, ctx: Context, voice_client: VoiceClient) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx)

        if guild_id in self.player_pool:
            player: Player = self.player_pool.__getitem__(guild_id)

            raise BeakErrors.AlreadyAllocatedGuildId(
                guild_id = guild_id,
                is_connected = player.is_connected,
                is_activated = player.is_activated
            )

        player = Player(
            voice_client = voice_client,
            message_storage = Storage.Message(),
            queue = AsyncQueue.Queue(),
            over_queue = AsyncQueue.OverQueue()
        )

        self.player_pool.__setitem__(guild_id, player)


    def __discard_pool__(self, guild_id) -> None:
        self.player_pool.__delitem__(guild_id)


    def __get_guild_player(self, guild_id: int) -> Player:
        return self.player_pool.__getitem__(guild_id)

    
    def DSC_get_guild_player(self, guild_id) ->Optional[Player]:
        raise NotImplementedError


    def is_beak_already_entered_channel(self, guild_id: int) -> bool:
        return guild_id in self.player_pool


    async def __ytdl_executor(self, URL: str, Debug=False) -> List[Dict[str, str]]:
        data = await YoutubeDlExtractor.extract(URL=URL, DEBUG=Debug)
        
        return data

    
    async def beak_enter(self, ctx: Context) -> None:
        voice_channel = ContextExtractor.get_author_entered_voice_channel(ctx)
        
        voice_client = await voice_channel.connect(self_deaf=True)

        try:
            self.__alloc_pool__(ctx=ctx, voice_client=voice_client)

        except BeakErrors.AlreadyAllocatedGuildId as e:
            print(f"{e.__doc__}\n{e}\n")


    async def beak_exit(self, ctx: Context) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx)

        guild_player = self.__get_guild_player(guild_id)

        if guild_player.is_connected:
            await guild_player.voice_client.disconnect()
        
        await BeakNotification.Playlist.discard(ctx=ctx, player=guild_player)

        self.__discard_pool__(guild_id=guild_id)


    async def beak_play(self, ctx: Context, URL: str) -> None:
        guild_id = ContextExtractor.get_guild_id(ctx)

        if ContextExtractor.is_beak_joined_voice_channel(ctx=ctx):
            if not ContextExtractor.is_beak_and_author_same_voice_channel(ctx=ctx):
                await BeakNotification.Error.notice_not_same_channel(ctx=ctx)

                return
            
        else:
            await self.beak_enter(ctx=ctx)

        guild_player = self.__get_guild_player(guild_id)
        
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

        try:
            guild_player.enqueue(audios=audios)
        
        except AsyncQueueErrors.QueueSaturatedErorr:
            # TODO: Handling this section
            pass

        await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)
    
        if guild_player.is_playing or guild_player.is_paused:
            return

        while not guild_player.is_queue_empty:
            audio_source_url = guild_player.seek_queue.get("audio_url")
            
            guild_player.voice_client.play(FFmpegPCMAudio(audio_source_url))

            await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

            while guild_player.is_playing or guild_player.is_paused:
                if not guild_player.is_connected:
                    await BeakNotification.Playlist.discard(ctx=ctx, player=guild_player)

                    self.__discard_pool__(guild_id=guild_id)
                    
                    return

                await asyncio.sleep(SLEEP_TIME)

            else:
                if guild_player.is_connected:
                    if guild_player.is_repeat_mode:
                        pass

                    else:
                        try:
                            guild_player.dequeue()

                        except AsyncQueueErrors.OverQueueSaturatedErorr:
                            # TODO: Handling this section
                            pass

                        if guild_player.is_loop_mode and guild_player.is_queue_empty:
                            guild_player.looping()

                            await BeakNotification.Playlist.notice_looping(ctx=ctx)

                    await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

        else:
            await BeakNotification.Playlist.notice_playlist_is_ended(ctx=ctx)


    @Inspector.coro_commander_inspection()
    async def beak_skip(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if guild_player.is_queue_two_or_more or guild_player.is_loop_mode:
            if guild_player.is_connected:
                if guild_player.is_repeat_mode:
                    guild_player.forced_skip()
                    
                else:
                    guild_player.skip()

        else:
            await BeakNotification.Error.notice_last_audio(ctx=ctx)


    @Inspector.coro_commander_inspection()
    async def beak_prev(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if not guild_player.is_overqueue_empty:
            if guild_player.is_connected:
                guild_player.prev()

        else:
            await BeakNotification.Error.notice_first_audio(ctx=ctx)


    @Inspector.coro_commander_inspection()
    async def beak_pause(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if not guild_player.is_paused:
            if guild_player.is_connected:
                guild_player.pause()

                await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

        else:
            await BeakNotification.Error.notice_already_paused(ctx=ctx)

        
    @Inspector.coro_commander_inspection()
    async def beak_replay(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if not guild_player.is_playing:
            if guild_player.is_connected:
                guild_player.resume()

                await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

        else:
            await BeakNotification.Error.notice_already_playing(ctx=ctx)


    @Inspector.coro_commander_inspection()
    async def beak_loop(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if guild_player.is_connected:
            guild_player.change_loop_mode()

            await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)
            

    @Inspector.coro_commander_inspection()
    async def beak_heavy_playlist(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if guild_player.is_connected:
            await BeakNotification.Playlist.notice_playlist(metadata=ctx, player=guild_player)


    @Inspector.coro_commander_inspection()
    async def beak_shuffle(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if guild_player.is_queue_single and guild_player.is_overqueue_empty:
            await BeakNotification.Playlist.notice_impossible_shuffling(ctx=ctx)
        
        else:
            if guild_player.is_connected:
                try:
                    guild_player.shuffle()

                    await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)

                except AsyncQueueErrors.QueueSaturatedErorr:
                    # TODO: Handling this section
                    pass

                    
    @Inspector.coro_commander_inspection()
    async def beak_remove(self, ctx: Context) -> None:
        guild_player = self.__get_guild_player(ContextExtractor.get_guild_id(ctx))

        if guild_player.is_queue_two_or_more:
            if guild_player.is_connected:
                try:
                    guild_player.remove()

                    await BeakNotification.Playlist.deploy(ctx=ctx, player=guild_player)
                
                except IndexError:
                    #TODO: Handling this section
                    pass

        else:
            await BeakNotification.Error.notice_last_audio(ctx=ctx)     
