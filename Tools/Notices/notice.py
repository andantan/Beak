import datetime
from typing import Dict, Union, Optional

from discord import Embed, ButtonStyle
from discord.ui import View, Button
from discord.ext.commands.context import Context, Interaction

from Class.superclass import Block

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.Queue.Errors.queue_error import AsyncQueueErrors

# from Tools.Decorators.decorator import BeakInspector
from Utils.extractor import InteractionExtractor

# from Utils.Functions.callbacks import Callback

from Data.Paraments.settings import (
    DEFAULT_DELAY, 
    COMMANDER_NOTICE_EMBED_COLOR,
    NOTICE_EMBED_COLOR,
    ATTACHED_PLAYLIST_EMBED_COLOR,
    ENDED_PLAYLIST_NOTICE_COLOR
)



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
            values = {
                "title" : "Beak-play 명령어 오류", 
                "description" : "음원 주소를 함께 입력해주세요",
                "color" : COMMANDER_NOTICE_EMBED_COLOR
            }

            await CommandNotification.Default.notice_default_embed(ctx=ctx, **values)


        @staticmethod
        async def notice_unvalid_url(ctx: Context) -> None:
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
        async def notice_default_embed(metadata: Union[Context, Interaction], **kwargs) -> None:
            _embed = Embed(**kwargs)

            _embed.set_footer(text="Beak by Qbean")

            if isinstance(metadata, Context):
                await metadata.send(embed=_embed, delete_after=DEFAULT_DELAY)
            
            elif isinstance(metadata, Interaction):
                await metadata.response.send_message(embed=_embed, delete_after=DEFAULT_DELAY)



    class Error(Block.Instanctiating):
        @staticmethod
        async def notice_already_beak_enterenced(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "봇이 이미 입장한 상태입니다.", 
                "description" : "만약 봇이 입장하지 않은 상태이면서, 이 오류가 발생한다면 ~리셋 명령어를 입력해주세요.", 
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)

            
        @staticmethod
        async def notice_author_not_entered_channel(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "음성 채널에 입장 후 명령어를 입력해주세요.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_beak_not_entered_channel(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "봇이 음성 채널에 입장한 상태가 아닙니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)

        
        @staticmethod
        async def notice_not_same_channel(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "봇과 동일한 채널에 입장 후 명령어를 입력해주세요.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_last_audio(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "마지막 음원입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_first_audio(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "첫 번째 음원입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_already_paused(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "이미 일시정지된 상태입니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_already_playing(metadata: Union[Context, Interaction]) -> None:
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

                if player.is_ended:
                    _embed = Embed(
                        title = "음원이 모두 재생되었습니다.", 
                        description = f"재생된 음원 수: {len(player.reference_overqueue)}개",
                        color = ATTACHED_PLAYLIST_EMBED_COLOR
                    )

                    _embed.set_author(name=f"🤩 \"{player.channel_name}\"에서 재생 완료 🤩")

                    _embed.add_field(name="재생 상태", value="재생 종료", inline=False)


                    prev_audio_value = "음원을 추가해주세요." \
                                        if player.is_overqueue_empty \
                                        else player.seek_overqueue.get("title")


                    _embed.add_field(name="이전 음원", value=prev_audio_value, inline=False)
                    _embed.add_field(name="다음 음원", value="음원을 추가해주세요.", inline=False)

                    _embed.set_footer(text="Beak by Qbean")

                    return _embed

                else:
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

                    _embed.set_thumbnail(
                        url = guild_now_playing.get("thumbnail")
                    )

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

                if player.is_paused:
                    button = Button(
                        label = "▶️",
                        style = ButtonStyle.secondary
                    )

                    button.callback = Callback.Button.callback_replay

                    _view.add_item(button)

                else:
                    button = Button(
                        label = "⏸️",
                        style = ButtonStyle.secondary
                    )

                    button.callback = Callback.Button.callback_pause

                    _view.add_item(button)

                return _view



        @staticmethod
        async def notice_player_discarded_embed(ctx: Context):
            values = {
                "title" : "플레이어가 종료되었습니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(ctx=ctx, **values)


        @staticmethod
        async def notice_playlist_is_ended(ctx: Context):
            values = {
                "title" : "플레이리스트가 모두 재생되었습니다.", 
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(ctx=ctx, **values)


        @staticmethod
        async def notice_looping(ctx: Context):
            values = {
                "title" : "전체 반복 재생 모드로 이전 재생 목록을 재생 대기열로 옮깁니다.", 
                "color" : ENDED_PLAYLIST_NOTICE_COLOR
            }

            await BeakNotification.Default.notice_default_embed(ctx=ctx, **values)
        

        @staticmethod
        async def notice_impossible_shuffling(metadata: Union[Context, Interaction]) -> None:
            values = {
                "title" : "추가된 음원이나 재생된 음원이 없습니다.",
                "color" : NOTICE_EMBED_COLOR
            }

            await BeakNotification.Default.notice_default_embed(metadata=metadata, **values)


        @staticmethod
        async def notice_playlist(metadata: Union[Context, Interaction], player: Player):
            _embed = BeakNotification.Playlist.PlaylistEmbedGenerator.get_playlist_embed(player=player)

            if isinstance(metadata, Context):
                await metadata.send(embed=_embed, delete_after=DEFAULT_DELAY)

            elif isinstance(metadata, Interaction):
                await metadata.response.send_message(embed=_embed, delete_after=DEFAULT_DELAY)


        @staticmethod
        async def deploy(player: Player, ctx: Optional[Context]=None, interaction: Optional[Interaction]=None) -> None:
            _embed = BeakNotification.Playlist.PlaylistEmbedGenerator.get_player_embed(player=player)
            _view = BeakNotification.Playlist.PlaylistViewGenerator.get_player_view(player=player)

            if player.is_message_saved:
                player.message = await player.message.edit(embed=_embed, view=_view)

            else:
                player.message = await ctx.send(embed=_embed, view=_view)


        @staticmethod
        async def discard(ctx: Context, player: Player) -> None:
            if player.is_message_saved:
                await player.message.delete()
            
            await BeakNotification.Playlist.notice_player_discarded_embed(ctx=ctx)

            

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
                    if guild_player.is_repeat_mode:
                        guild_player.forced_skip()
                        
                    else:
                        guild_player.skip()

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

            else:
                BeakNotification.Error.notice_last_audio(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_prev(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if not guild_player.is_overqueue_empty:
                if guild_player.is_connected:
                    guild_player.prev()

                    await interaction.response.defer()
                    await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

            else:
                await BeakNotification.Error.notice_first_audio(metadata=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_loop(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                guild_player.change_loop_mode()

                await interaction.response.defer()
                await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_haevy_playlist(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                await interaction.response.defer()
                await BeakNotification.Playlist.notice_playlist(metadata=interaction, player=guild_player)


        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_loop(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if guild_player.is_connected:
                guild_player.change_loop_mode()

                await interaction.response.defer()
                await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)


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
                        await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

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
                        guild_player.remove()

                        await interaction.response.defer()
                        await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)
                    
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
                    await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

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
                    await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

            else:
                await BeakNotification.Error.notice_already_paused(metadata=interaction)
