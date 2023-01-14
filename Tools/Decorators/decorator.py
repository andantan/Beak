
from discord.ext.commands.context import Context, Interaction

from Utils.extractor import ContextExtractor, InteractionExtractor

from Class.superclass import Block

from Tools.Functions.function import BeakNotification


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