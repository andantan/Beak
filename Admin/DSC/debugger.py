from typing import (
    Dict, List,
    Any
)

from discord.ext.commands.context import Context

from Core.beak import Beak

from Class.superclass import Block

from Utils.extractor import ContextExtractor, YoutubeDlExtractor


class Debugger(Block.Instanctiating):
    @staticmethod
    async def debug_youtube_dl_extractor(URL: str, document: bool=False) -> None:
        from pprint import pprint

        debugging_data = await YoutubeDlExtractor.extract(URL=URL, DEBUG=True)

        if document:
            from datetime import datetime

            import os

            __PATH_RAW_JSON = os.path.join(
                os.getcwd(),
                "DATA",
                "Log",
                "YTDL_LOG",
                "Raw",
                f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
            )

            __PATH_EXTRACTED_JSON = os.path.join(
                os.getcwd(),
                "DATA",
                "Log",
                "YTDL_LOG",
                "Extracted",
                f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
            )

            try:
                with open(__PATH_RAW_JSON, mode="w", encoding="utf-8") as handler:
                    pprint(
                        debugging_data, 
                        indent=4,
                        width=100, 
                        stream=handler
                    )

                with open(__PATH_EXTRACTED_JSON, mode="w", encoding="utf-8") as handler:
                    pprint(
                        YoutubeDlExtractor.summarize(debugging_data, URL), 
                        indent=4, 
                        width=100, 
                        stream=handler
                    )
                
            except Exception as ERO:
                print(ERO)

        else:
            pprint(YoutubeDlExtractor.summarize(debugging_data, URL), indent=4)

    
    @staticmethod
    def debug_context_extractor(ctx: Context) -> None:
        document = \
'''
ContextExtractor debugger has been executed
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

***       ContextExtractor summarized data value documents       ***

    GN:     Guild_name                                  # str
    GI:     Guild_id                                    # int
    AN:     Author_name                                 # str
    AI:     Author_id                                   # int
    CECCN:  Commander_executed_chatting_channel_name    # str
    CECCI:  Commander_executed_chatting_channel_id      # int
    CEVCN:  Commander_entered_voice_channel_name        # str | None
    CEVCI:  Commander_entered_voice_channel_id          # int | None
    BEVCN:  Bot_entered_voice_channel_name              # str | None
    BEVCI:  Bot_entered_voice_channel_id                # int | None

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
        print(document)

        print("Summarized Context data = {")
        
        for k, v in ContextExtractor.summarize(ctx).items():
            print(f"    {k:<6}: {v}")
        else:
            print("}\n")
        
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    

    @staticmethod
    def debug_player_status(ctx: Context) -> None:
        beak_debugger: Beak = Beak()

        guild_player = beak_debugger.DSC_get_guild_player(ctx=ctx)

        
