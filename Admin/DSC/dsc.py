from typing import Dict, List, Union, Optional

from discord import Embed
from discord.voice_client import VoiceClient
from discord.ext.commands.context import Context, Interaction

from Core.Cache.pool import PlayerPool
from Core.Cache.player import Player
from Core.Cache.storage import Storage
from Core.Cache.Queue.queue import AsyncQueue

from Class.superclass import Block

from Data.Paraments.settings import (
    DSC_NOTICE_EMBED_COLOR,
    DSC_DEFAULT_DELAY
)


Metadata = Union[Context, Interaction]
EmbedFields = List[Dict[str, str]]
EmbedValues = Dict[str, str]

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



class Logger(Block.Instanctiating):
    class EmbedNotification(Block.Instanctiating):
        @staticmethod
        async def embed_wrapper(metadata: Metadata, values: EmbedValues, fields: Optional[EmbedFields]=None) -> None:
            _embed = Embed(**values)

            if not fields is None:
                _k = ["name", "value", "inline"]

                for field in fields:
                    for key in _k:
                        if not key in field:
                            break

                    _embed.add_field(**field)

            _embed.set_footer(text="Beak-DSC by Qbean")

            if isinstance(metadata, Context):
                await metadata.send(embed=_embed, delete_after=DSC_DEFAULT_DELAY)

            if isinstance(metadata, Interaction):
                await metadata.response.send_message(embed=_embed, delete_after=DSC_DEFAULT_DELAY)


        @staticmethod
        async def notice_unallocated_guild_id(metadata: Metadata, ero: Exception) -> None:
            values = {
                "title" : "Player allocation Warning", 
                "description" : f"Unallocated guild id({metadata.guild.id})",
                "color" : DSC_NOTICE_EMBED_COLOR
            }

            fields = {
                "name": "ValueError",
                "value": f"{ero}",
                "inline": False
            }

            await Logger.EmbedNotification.embed_wrapper(metadata=metadata, values=values, fields=fields)