import datetime
import asyncio
from typing import Dict, List, Tuple, Union, Optional, NewType, Callable, Coroutine, TypeVar

import discord

from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from discord.ext.commands.context import Context, Interaction

from Class.superclass import Block

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.Queue.Errors.queue_error import AsyncQueueErrors

from Utils.extractor import InteractionExtractor, ContextExtractor


from Data.Paraments.settings import (
    DEFAULT_DELAY,
    SELECT_MENU_THRESHOLD,
    COMMANDER_NOTICE_EMBED_COLOR,
    NOTICE_EMBED_COLOR,
    ATTACHED_PLAYLIST_EMBED_COLOR,
    ENDED_PLAYLIST_NOTICE_COLOR,
    QUEUE_THRESHOLD,
    OVER_QUEUE_THRESHOLD
)


A = TypeVar("A")                # Arguments type
R = TypeVar("R")                # return type

stat = Union[int, bool]
Function = Callable[[A], R]
O_all = Union[bool, str, int, Function, None]
Metadata = Union[Context, Interaction]

BtnStat = NewType("BtnStat", Dict[str, O_all[Interaction, Coroutine]])
BtnAttr = NewType("BtnAttr", Dict[stat, BtnStat])



class CallbackInspector(Block.Instanctiating):
    @staticmethod
    def coro_interaction_inspection():
        def _decof(func):
            async def wrapper(*args, **kwargs):
                interaction: Interaction

                if "interaction" in kwargs.keys():
                    interaction = kwargs.get("interaction")

                else:
                    interaction = args.__getitem__(0)
                
                if InteractionExtractor.is_user_joined_voice_channel(interaction):
                    if InteractionExtractor.is_beak_joined_voice_channel(interaction):
                        if InteractionExtractor.is_beak_and_user_same_voice_channel(interaction):
                            await func(*args, **kwargs)

                        else:
                            await BeakNotification.Error.notice_not_same_channel(metadata=interaction)
                    
                    else:
                        await BeakNotification.Error.notice_beak_not_entered_channel(metadata=interaction)
                
                else:
                    await BeakNotification.Error.notice_author_not_entered_channel(metadata=interaction)

            return wrapper
        return _decof



class Callback(Block.Instanctiating):
    class Button(Block.Instanctiating):
        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_skip(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_queue_two_or_more or guild_player.is_loop_mode:
                if guild_player.is_connected:
                    guild_player.skip(forced=guild_player.is_repeat_mode)

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player)

            else:
                await BeakNotification.Error.notice_last_audio(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_prev(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if not guild_player.is_overqueue_empty:
                if guild_player.is_connected:
                    guild_player.prev(forced=guild_player.is_repeat_mode)

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player)

            else:
                await BeakNotification.Error.notice_first_audio(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_loop(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                guild_player.change_loop_mode()

                await interaction.response.defer()
                await BeakNotification.Playlist.deploy(player=guild_player)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_haevy_playlist(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                await BeakNotification.Playlist.notice_playlist(metadata=interaction, player=guild_player)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_loop(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                guild_player.change_loop_mode()

                await interaction.response.defer()
                await BeakNotification.Playlist.deploy(player=guild_player)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_shuffle(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_queue_single and guild_player.is_overqueue_empty:
                await BeakNotification.Playlist.notice_impossible_shuffling(metadata=interaction)
            
            else:
                if guild_player.is_connected:
                    try:
                        guild_player.shuffle()

                        await interaction.response.defer()
                        await BeakNotification.Playlist.deploy(player=guild_player)

                    except AsyncQueueErrors.QueueSaturatedErorr:
                        # TODO: Handling this section
                        pass
          
        
        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_remove(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_queue_two_or_more:
                if guild_player.is_connected:
                    try:
                        removed_audio_title = guild_player.seek_next_queue.get("title")

                        guild_player.remove()

                        await BeakNotification.Playlist.notice_removed(metadata=interaction, title=removed_audio_title)
                        await BeakNotification.Playlist.deploy(player=guild_player)
                    
                    except IndexError:
                        #TODO: Handling this section
                        pass

            else:
                await BeakNotification.Error.notice_last_audio(metadata=interaction)     


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_pause(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if not guild_player.is_paused:
                if guild_player.is_connected:
                    guild_player.pause()

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player)

            else:
                BeakNotification.Error.notice_already_playing(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_replay(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if not guild_player.is_playing:
                if guild_player.is_connected:
                    guild_player.resume()

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player)

            else:
                await BeakNotification.Error.notice_already_paused(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_exit(interaction: Interaction) -> None:
            guild_id = InteractionExtractor.get_guild_id(interaction)
            guild_player: Player = PlayerPool().get(guild_id)

            if guild_player.is_connected:
                await guild_player.voice_client.disconnect()

                PlayerPool().__delitem__(guild_id)
                
                await BeakNotification.Playlist.discard(metadata=interaction, player=guild_player)

        
        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_refresh(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                await BeakNotification.Playlist.deploy(player=guild_player)

                await interaction.response.defer()


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_reset(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                guild_player.reset()

                await BeakNotification.Playlist.deploy(player=guild_player)
                await BeakNotification.Playlist.notice_reset_playlist(metadata=interaction, player=guild_player)



    class SelectMenu(Block.Instanctiating):
        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_force_play(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                index = int(interaction.data.get("values").__getitem__(0))

                selected_audio = guild_player.forced_play(value=index, forced=guild_player.is_repeat_mode)

                await BeakNotification.Playlist.notice_forced_play(metadata=interaction, audio=selected_audio)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_force_prev_play(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                index = int(interaction.data.get("values").__getitem__(0))

                selected_audio = guild_player.forced_prev(value=index, forced=guild_player.is_repeat_mode)

                await BeakNotification.Playlist.notice_forced_play(metadata=interaction, audio=selected_audio)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_defer(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                await interaction.response.defer()
                


class CommandNotification(Block.Instanctiating):
    class Default(Block.Instanctiating):
        @staticmethod
        async def notice_default_embed(ctx: Context, **kwargs) -> None:
            _embed = Embed(**kwargs)

            _embed.set_footer(text="Beak by Qbean")

            await ctx.send(embed=_embed, delete_after=DEFAULT_DELAY)



    class Error(Block.Instanctiating):
        @staticmethod
        async def notice_missing_required_arguments(ctx: Context) -> None:
            # TODO: Type change :: Context to Metadata
            values = {
                "title" : "Beak-play 명령어 오류", 
                "description" : "음원 주소를 함께 입력해주세요",
                "color" : COMMANDER_NOTICE_EMBED_COLOR
            }

            await CommandNotification.Default.notice_default_embed(ctx=ctx, **values)


        @staticmethod
        async def notice_unvalid_url(ctx: Context) -> None:
            # TODO: Type change :: Context to Metadata
            values = {
                "title" : "Beak-play 주소 오류", 
                "description" : "주소가 옳바르지 않습니다.",
                "color" : COMMANDER_NOTICE_EMBED_COLOR
            }

            await CommandNotification.Default.notice_default_embed(ctx=ctx, **values)





class AdminNotification(Block.Instanctiating):
    class Default(Block.Instanctiating):
        @staticmethod
        async def notice_default_embed(ctx: Context, **kwargs) -> None:
            _embed = Embed(**kwargs)

            _embed.set_footer(text="Beak-DSC by Qbean")

            await ctx.send(embed=_embed, delete_after=DEFAULT_DELAY)



    class Admin(Block.Instanctiating):
        @staticmethod
        async def notice_not_authorized_user(ctx: Context) -> None:
            values = {
                "title": "Beak Debugger, Supervisor & Controller",
                "description": "어드민 권한이 없습니다.",
                "color": COMMANDER_NOTICE_EMBED_COLOR
            }

            await AdminNotification.Default.notice_default_embed(ctx=ctx, **values)



class BeakNotification(Block.Instanctiating):
    class Default(Block.Instanctiating):
        @staticmethod
        async def notice_default_embed(metadata: Metadata, delay: int=DEFAULT_DELAY,**kwargs) -> None:
            try:
                _embed = Embed(**kwargs)

                _embed.set_footer(text="Beak by Qbean")

                if isinstance(metadata, Context):
                    await metadata.send(embed=_embed, delete_after=delay)
                
                elif isinstance(metadata, Interaction):
                    await metadata.response.send_message(embed=_embed, delete_after=delay)
            except Exception as e:
                print(e)



    class Error(Block.Instanctiating):
        @staticmethod
        async def notice_already_beak_enterenced(metadata: Metadata) -> None:
            values = {
                "title" : "봇이 이미 입장한 상태입니다.", 
                "description" : "만약 봇이 입장하지 않은 상태이면서, 이 오류가 발생한다면 ~리셋 명령어를 입력해주세요.", 
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)

            
        @staticmethod
        async def notice_author_not_entered_channel(metadata: Metadata) -> None:
            values = {
                "title" : "음성 채널에 입장 후 명령어를 입력해주세요.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_beak_not_entered_channel(metadata: Metadata) -> None:
            values = {
                "title" : "봇이 음성 채널에 입장한 상태가 아닙니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)

        
        @staticmethod
        async def notice_not_same_channel(metadata: Metadata) -> None:
            values = {
                "title" : "봇과 동일한 채널에 입장 후 명령어를 입력해주세요.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_last_audio(metadata: Metadata) -> None:
            values = {
                "title" : "마지막 음원입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_first_audio(metadata: Metadata) -> None:
            values = {
                "title" : "첫 번째 음원입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_already_paused(metadata: Metadata) -> None:
            values = {
                "title" : "이미 일시정지된 상태입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_already_playing(metadata: Metadata) -> None:
            values = {
                "title" : "이미 재생 중인 상태입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)



    class Playlist(Block.Instanctiating):
        class PlaylistEmbedGenerator(Block.Instanctiating):
            @staticmethod
            def get_player_embed(player: Player) -> Embed:
                mode_value: Dict[bool, str] = {
                    True: "일시 정지",
                    False: "재생 중"
                }

                loop_value: Dict[int, str] = {
                    0: "일반 재생",
                    1: "전체 반복",
                    2: "한곡 반복"
                }

                # deprecatd 2023-02-24
                
                # if player.is_ended:
                #     deprecated 2023-02-24
                #     Releases: v3.1.18-alpha
                #     Notes: No more waiting until enqueuing audio
                    
                #     _embed = Embed(
                #         title = "음원이 모두 재생되었습니다.", 
                #         description = f"재생된 음원 수: {len(player.reference_overqueue)}개",
                #         color = ATTACHED_PLAYLIST_EMBED_COLOR
                #     )

                #     _embed.set_author(name=f"🤩 \"{player.channel_name}\"에서 재생 완료 🤩")

                #     _embed.add_field(name="재생 상태", value="재생 종료", inline=False)


                #     prev_audio_value = "음원을 추가해주세요." \
                #                         if player.is_overqueue_empty \
                #                         else player.seek_overqueue.get("title")


                #     _embed.add_field(name="이전 음원", value=prev_audio_value, inline=False)
                #     _embed.add_field(name="다음 음원", value="음원을 추가해주세요.", inline=False)

                #     _embed.set_footer(text="Beak by Qbean")

                #     return _embed

                # else:

                guild_now_playing: Dict[str, str] = player.reference_queue.__getitem__(0)

                timedelta_message = f"{datetime.timedelta(seconds=guild_now_playing.get('duration'))}"

                prev_audio_value = "첫 번째 음원입니다." \
                                    if player.is_overqueue_empty \
                                    else player.seek_overqueue.get("title")

                next_audio_value = player.reference_queue.__getitem__(1).get("title") \
                                    if player.is_queue_two_or_more \
                                    else "마지막 음원입니다."

                waiting_value = "∞" if player.is_loop_mode else f"{len(player.reference_queue) - 1}개"


                _embed = Embed(
                    title = guild_now_playing.get("title"),
                    url = guild_now_playing.get("original_url"),
                    description = guild_now_playing.get("uploader"),
                    color = ATTACHED_PLAYLIST_EMBED_COLOR
                )

                _embed.set_author(name=f"🤩 \"{player.channel_name}\"에서 재생 중 🤩")
                _embed.set_thumbnail(url = guild_now_playing.get("thumbnail"))
                _embed.add_field(name="음원 길이", value=timedelta_message, inline=True)
                _embed.add_field(name="재생 상태", value=mode_value.get(player.is_paused), inline=True)
                _embed.add_field(name="재생 모드", value=loop_value.get(player.loop_mode), inline=True)
                _embed.add_field(name="이전 음원", value=prev_audio_value, inline=False)
                _embed.add_field(name="다음 음원", value=next_audio_value, inline=False)
                _embed.add_field(name="대기 중인 음원 수", value=waiting_value, inline=False)
                
                _embed.set_footer(text="Beak by Qbean")

                return _embed


            @staticmethod
            def get_playlist_embed(player: Player) -> Embed:
                playlist = player.reference_queue
                over_played = player.reference_overqueue
                over_played_length = player.overqueue_length
                counts = 5

                _embed = Embed( color=0x6b82f5 )

                if player.is_queue_two_or_less:
                    overplayed_counts = 5 if over_played_length > 5 else over_played_length

                else:
                    overplayed_counts = 2 if over_played_length > 2 else over_played_length


                for i in range(overplayed_counts, 0, -1):
                    _embed.add_field(
                        name = f"이전 음원 - {i}", 
                        value = over_played.__getitem__(-1 * i).get("title"),
                        inline = False
                    )

                else:
                    counts -= overplayed_counts

                    if counts == 0:
                        _embed.set_footer(text="Beak by Qbean")

                        return _embed

                _embed.add_field(
                    name = f"재생 중인 음원",
                    value = playlist.__getitem__(0).get("title"),
                    inline = False
                )

                counts -= 1

                if counts == 0:
                    _embed.set_footer(text="Beak by Qbean")

                    return _embed

                for i in range(1, counts + 1):
                    if i == player.queue_length:
                        break

                    _embed.add_field(
                        name = f"다음 음원 - {i}", 
                        value = playlist.__getitem__(i).get("title"),
                        inline = False
                    )

                _embed.set_footer(text="Beak by Qbean")

                return _embed


        
        class PlaylistViewGenerator(Block.Instanctiating):
            @staticmethod
            def get_player_view(player: Player) -> View:
                _view = View(timeout=None)
                


                overqueue_options: List[SelectOption] = list()
                
                guild_overqueue: Tuple[Dict[str, str]] = player.reference_overqueue

                for index, audio in enumerate(guild_overqueue):
                    if index == SELECT_MENU_THRESHOLD:
                        break

                    option = SelectOption(
                        label = f"{index + 1} - {audio.get('title')[:100]}",
                        description = f"{audio.get('uploader')[:100]}",
                        value = f"{index}"
                    )

                    overqueue_options.append(option)

                if overqueue_options:
                    overqueue_menu = Select(
                        placeholder = "재생완료된 음원 중 재생할 음원을 선택해주세요.",
                        options = overqueue_options,
                        row = 0
                    )

                    overqueue_menu.callback = Callback.SelectMenu.callback_force_prev_play
                else:
                    overqueue_menu = Select(
                        placeholder = "첫번째 음원입니다.",
                        options = [ SelectOption(label="재생완료된 음원이 존재하지 않습니다.") ],
                        row = 0
                    )

                    overqueue_menu.callback = Callback.SelectMenu.callback_defer

                _view.add_item(overqueue_menu)



                queue_options: List[SelectOption] = list()
                
                guild_queue: Tuple[Dict[str, str]] = player.reference_queue[1:]

                for index, audio in enumerate(guild_queue):
                    if index == SELECT_MENU_THRESHOLD:
                        break

                    option = SelectOption(
                        label = f"{index + 1} - {audio.get('title')[:100]}",
                        description = f"{audio.get('uploader')[:100]}",
                        value = f"{index + 1}"
                    )

                    queue_options.append(option)

                if queue_options:
                    queue_menu = Select(
                        placeholder = "대기 중인 음원 중 재생할 음원을 선택해주세요.",
                        options = queue_options,
                        row = 1
                    )

                    queue_menu.callback = Callback.SelectMenu.callback_force_play
                else:
                    queue_menu = Select(
                        placeholder = "마지막 음원입니다.",
                        options = [ SelectOption(label="음원을 추가해주세요.") ],
                        row = 1
                    )

                    queue_menu.callback = Callback.SelectMenu.callback_defer

                _view.add_item(queue_menu)



                buttons = Generator.Button.get_buttons(player=player)

                for element in buttons:
                    button = Button(
                        label = element.get("label"),
                        style = element.get("style"),
                        disabled = element.get("disabled"),
                        row = element.get("row") + 2
                    )

                    button.callback = element.get("callback")

                    _view.add_item(button)

                return _view



        @staticmethod
        async def notice_player_discarded_embed(metadata: Metadata):
            values = {
                "title" : "플레이어가 종료되었습니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_playlist_is_ended(metadata: Metadata):
            values = {
                "title" : "플레이리스트가 모두 재생되었습니다.", 
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_looping(metadata: Metadata):
            values = {
                "title" : "전체 반복 재생 모드로 이전 재생 목록을 재생 대기열로 옮깁니다.", 
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_removed(metadata: Metadata, title: str):
            values = {
                "title" : "음원 삭제가 완료되었습니다.",
                "description": f"삭제된 음원: {title}",
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, delay=3, **values)
        

        @staticmethod
        async def notice_impossible_shuffling(metadata: Metadata) -> None:
            values = {
                "title" : "추가된 음원이나 재생된 음원이 없습니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_playlist(metadata: Metadata, player: Player) -> None:
            _embed = BeakNotification.Playlist.PlaylistEmbedGenerator.get_playlist_embed(player=player)

            if isinstance(metadata, Context):
                await metadata.send(embed=_embed, delete_after=DEFAULT_DELAY)

            elif isinstance(metadata, Interaction):
                await metadata.response.send_message(embed=_embed, delete_after=DEFAULT_DELAY)


        @staticmethod
        async def notice_forced_play(metadata: Metadata, audio: Dict[str, str]) -> None:
            values = {
                "title" : f"{audio.get('title')}을(를) 먼저 재생합니다.",
                "description": f"{audio.get('uploader')}",
                "color" : ATTACHED_PLAYLIST_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_reset_playlist(metadata: Metadata) -> None:
            values = {
                "title" : "플레이리스트가 초기화되었습니다.",
                "color" : ATTACHED_PLAYLIST_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_video_founded(metadata: Metadata, title: str) -> None:
            values = {
                "title" : "🎵 음원을 찾았습니다. 🎵",
                "description": f"검색된 음원: {title}",
                "color" : ATTACHED_PLAYLIST_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_empty_voice_channel(metadata: Metadata) -> None:
            values = {
                "title" : "빈 음성 채널이 감지되었습니다.",
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_saturated_queue(metadata: Metadata) -> None:
            values = {
                "title" : f"대기열이 가득찼습니다. (최대 대기가능 음원 수: {QUEUE_THRESHOLD})",
                "description": f"{QUEUE_THRESHOLD}번 째 다음 음원은 모두 자동 삭제됩니다.",
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)



        @staticmethod
        async def deploy(player: Player, ctx: Optional[Context]=None) -> None:
            _embed = BeakNotification.Playlist.PlaylistEmbedGenerator.get_player_embed(player=player)
            _view = BeakNotification.Playlist.PlaylistViewGenerator.get_player_view(player=player)

            if player.is_message_saved:
                try:
                    player.message = await player.message.edit(embed=_embed, view=_view)
                
                except discord.errors.NotFound:
                    player.message = await player.message.channel.send(embed=_embed, view=_view)

            else:
                try:
                    player.message = await ctx.send(embed=_embed, view=_view)
                    player.channel_id = int(ContextExtractor.get_channel_id(ctx=ctx))

                except Exception as e:
                    print(e)
                    print(e.__doc__)


        @staticmethod
        async def discard(metadata: Metadata, player: Player) -> None:
            if player.is_message_saved:
                await player.message.delete()
            
            await BeakNotification.Playlist.notice_player_discarded_embed(metadata=metadata)


class Generator(Block.Instanctiating):
    class Button(Block.Instanctiating):
        # 셔플 이전 일정 다음 반복
        # 초기화 삭제 플리 퇴장 초기

        shuffle_btn: BtnAttr = {
            True: {
                "label": "🔀",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_shuffle,
                "row": 0
            },
            False: {
                "label": "🔀",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_shuffle,
                "row": 0
            }
        }

        prev_btn: BtnAttr = {
            True: {
                "label": "⏮",
                "style": ButtonStyle.secondary,
                "disabled": True,
                "callback": None,
                "row": 0
            },
            False: {
                "label": "⏮️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_prev,
                "row": 0
            }
        }

        pause_and_play_btn: BtnAttr = {
            True: {
                "label": "▶️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_replay,
                "row": 0
            },
            False: {
                "label": "⏸️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_pause,
                "row": 0
            }
        }  

        skip_btn: BtnAttr = {
            True: {
                "label": "⏭️",
                "style": ButtonStyle.secondary,
                "disabled": True,
                "callback": None,
                "row": 0
            },
            False: {
                "label": "⏭️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_skip,
                "row": 0
            }
        }

        loop_btn: BtnAttr = {
            0: {
                "label": "➡️",      # Linear playing mode
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_loop,
                "row": 0
            },
            1: {
                "label": "🔁",      # Loop playing mode
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_loop,
                "row": 0
            },
            2: {
                "label": "🔂",      # Repeat playing mode
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_loop,
                "row": 0
            }
        }

        refresh_btn: BtnAttr = {
            True: {
                "label": "🛠️",
                "style": ButtonStyle.secondary,
                "disabled": True,
                "callback": Callback.Button.callback_refresh,
                "row": 1
            },
            False: {
                "label": "🛠️",
                "style": ButtonStyle.secondary,
                "disabled": True,
                "callback": Callback.Button.callback_refresh,
                "row": 1
            }
        }

        remove_btn: BtnAttr = {
            True: {
                "label": "🗑️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_remove,
                "row": 1
            },
            False: {
                "label": "🗑️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_remove,
                "row": 1
            }
        }

        playlist_btn: BtnAttr = {
            True: {
                "label": "📜",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_haevy_playlist,
                "row": 1
            },
            False: {
                "label": "📜",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_haevy_playlist,
                "row": 1
            }
        }        

        exit_btn: BtnAttr = {
            True: {
                "label": "⏹️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_exit,
                "row": 1
            },
            False: {
                "label": "⏹️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_exit,
                "row": 1
            }
        }

        reset_btn: BtnAttr = {
            True: {
                "label": "🔄️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_reset,
                "row": 1
            },
            False: {
                "label": "🔄️",
                "style": ButtonStyle.secondary,
                "disabled": False,
                "callback": Callback.Button.callback_reset,
                "row": 1
            }
        }


        @classmethod
        def get_buttons(cls, player: Player) -> Tuple[BtnStat]:
            buttons: List[BtnStat] = list()

            buttons.append(cls.shuffle_btn.get(True))
            buttons.append(cls.prev_btn.get(player.is_first_audio))
            buttons.append(cls.pause_and_play_btn.get(player.is_paused))
            buttons.append(cls.skip_btn.get(player.is_last_audio))
            buttons.append(cls.loop_btn.get(player.loop_mode))
            
            buttons.append(cls.reset_btn.get(True))
            buttons.append(cls.remove_btn.get(True))
            buttons.append(cls.playlist_btn.get(True))
            buttons.append(cls.exit_btn.get(True))
            buttons.append(cls.refresh_btn.get(True))

            return tuple(buttons)
 

    class SelectMenu(Block.Instanctiating):
        @staticmethod
        def get_select_options(player: Player) -> List[SelectOption]:
            options: List[SelectOption] = list()

            if player.is_queue_single:
                return options
            
            guild_queue: Tuple[Dict[str, str]] = player.reference_queue[1:]

            try:
                for index, audio in enumerate(guild_queue):
                    option = SelectOption(
                        label = f"{index + 1} - {audio.get('title')}",
                        description = f"{audio.get('uploader')}",
                        value = f"{index + 1}"
                    )

                    options.append(option)

            except ValueError:
                pass

            except Exception as e:
                import traceback

                print(e)
                print(e.__doc__)
                print(traceback.format_exc())