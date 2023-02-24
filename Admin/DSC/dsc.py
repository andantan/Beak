from typing import Union

from discord import Embed
from discord.voice_client import VoiceClient

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.storage import Storage
from Core.Cache.Queue.queue import AsyncQueue

from Class.superclass import Block


class DSC(Block.Instanctiating):
    class Debugger(Block.Instanctiating):
        ...


    
    class Supervisor(Block.Instanctiating):
        ...


    
    class Controller(Block.Instanctiating):
        @staticmethod
        async def dismantle_player(identification: int, player: Player) -> None:
            """ |coroutine|
            
            Disconnects voice client and clear Asyncqueue & MessageStorage\n
            and then, free player from PlayerPool
            
            e.g. :meth:`Controller.dismantle_player`

            Attributes
            -----------
            identification: :class:`int`
                The guild id
            player: :class:`Player`
                The guild player           
            """

            async def __vacate_player(pl: Player) -> None:
                if pl.is_connected:
                    await pl.voice_client.disconnect()

                pl.queue.clear(on_air=False)
                pl.overqueue_length.clear()
                pl.message_storage.clear()
            
            if not isinstance(identification, int):
                raise ValueError

            if not isinstance(player, Player):
                raise TypeError
            
            await __vacate_player(pl=player)

            PlayerPool().__delitem__(guild_id=identification)


        @staticmethod
        def allocate_player(identification: int, voice_client: VoiceClient) -> None:
            """ 
            Attributes
            -----------
            identification: :class:`int`
                The guild id
            voice_client: :class:`VoiceClient`
                the voice client connected to voice channel          
            """
            _player = Player(
                voice_client = voice_client,
                message_storage = Storage.Message(guild_id=identification),
                queue = AsyncQueue.Queue(),
                over_queue = AsyncQueue.OverQueue()
            )
            
            PlayerPool().__setitem__(guild_id=identification, player=_player)