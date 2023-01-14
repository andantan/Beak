from Class.superclass import Block


class BeakErrors(Block.Instanctiating):
    class AlreadyAllocatedGuildId(Exception):
        '''
Guild id has been already allocated
    {
        @dataclass
        class Beak(metaclass=Singleton):
            ...
            def __alloc_status__(self, ctx: Context, voice_client: VoiceClient) -> int:
                    guild_id = ContextExtractor.get_guild_id(ctx)

                if guild_id in self.vc_status_pool or guild_id in self.pl_status_pool:
------------------> raise BeakErrors.AlreadyAllocatedGuildId
        }
    }
Raised AlreadyAllocatedGuildId on Beak::__alloc_status__(...)
        '''

        def __init__(self, guild_id: int, is_connected: bool, is_activated: bool) -> None:
            message = f"Guild id({guild_id}) has been already allocated\n"
            message += f"[ Connection: {is_connected}, Activation: {is_activated} ]"

            super().__init__(message)