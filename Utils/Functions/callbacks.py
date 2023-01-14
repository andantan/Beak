from discord.ext.commands.context import Interaction

from Class.superclass import Block

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.Queue.queue import AsyncQueue

from Tools.Functions.function import BeakNotification

from Utils.extractor import InteractionExtractor


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
    __slots__ = ()

    class Button(Block.Instanctiating):
        @staticmethod
        @CallbackInspector.coro_interaction_inspection()
        async def callback_pause(interaction: Interaction) -> None:
            guild_player: Player = PlayerPool().get(InteractionExtractor.get_guild_id(interaction))

            if not guild_player.is_paused:
                if guild_player.is_connected:
                    guild_player.pause()

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

                    await BeakNotification.Playlist.deploy(player=guild_player, interaction=interaction)

            else:
                BeakNotification.Error.notice_already_paused(metadata=interaction)
