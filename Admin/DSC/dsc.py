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
        async def dismantle_player(identification: int, player: Union[Player, PlayerPool]) -> None:

            async def vacate_player(pl: Player) -> None:
                if pl.is_connected:
                    await pl.voice_client.disconnect()

                pl.queue.clear(on_air=False)
                pl.overqueue_length.clear()
                pl.message_storage.clear()
                
            
            if not isinstance(identification, int):
                raise ValueError

            if isinstance(player, Player):
                await vacate_player(pl=player)

            elif isinstance(player, PlayerPool):
                ...

            else:
                raise TypeError