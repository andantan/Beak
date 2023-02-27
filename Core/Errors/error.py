from Class.superclass import Block


class Error(Exception): ...
class Warning(Exception): ...

class BeakError(Block.Instanctiating):
    class AllocatedIdentificationError(Error): ...
    class UnallocatedIdentificationError(Error): ...
class BeakWarning(Block.Instanctiating): 
    ...
class AsyncQueueError(Block.Instanctiating):
    class SaturatedQueueError(Error): ...
    class SaturatedOverQueueError(Error): ...

class SelectionError(Block.Instanctiating):
    # deprecated 2023-02-28    
    #
    # raise not NotImplementedError

    class NotEqualLengthError(Error): ...



# deprecated 2023-02-24
# 
# class BeakErrors(Block.Instanctiating):
# # deprecated 2023-02-23
# #
# #     class AlreadyAllocatedGuildId(Exception):
# #         '''
# # Player has been already allocated
# #     {
# #         @dataclass
# #         class Beak(metaclass=Singleton):
# #             ...
# #             def __alloc_status__(self, ctx: Context, voice_client: VoiceClient) -> int:
# #                     guild_id = ContextExtractor.get_guild_id(ctx)
# #
# #             if guild_id in self.player_pool:
# #                 player: Player = self.player_pool.__getitem__(guild_id)
# #
# # --------------> raise BeakErrors.AlreadyAllocatedGuildId
# #         }
# #     }
# # Raised AlreadyAllocatedGuildId on Beak::__alloc_status__(...)
# #         '''
# #
# #         def __init__(self, guild_id: int, is_connected: bool, is_activated: bool, is_msg_saved: bool) -> None:
# #             message = f"Player({guild_id}) has been already allocated\n"
# #             message += f"[ Connection: {is_connected}, Activation: {is_activated} ]"
# #             message += f"[ Message Stored: {is_msg_saved} ]"
# #
# #             super().__init__(message)


