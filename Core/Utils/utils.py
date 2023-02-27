from typing import Tuple, Dict, List, Optional

import random
import math

from discord import Guild, Member
from discord import Embed, ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from discord.ext.commands.context import Context, Interaction

from Class.superclass import Block

from Core.Cache.storage import Storage

from Utils.extractor import ContextExtractor, InteractionExtractor

from Data.Paraments.settings import (
    DEFAULT_DELAY,
    NOTICE_EMBED_COLOR
)

from Types.Generic.vars import (
    Metadata as Metadata,
    EmbedValues as EmbedValues,
    EmbedField as EmbedField,
    EmbedFields as EmbedFields,
    MemberId as MemberId
)


class Messenger(Block.Instanctiating):
    class Default(Block.Instanctiating):
        @staticmethod
        async def embed_wrapper(metadata: Metadata, 
                                values: EmbedValues, 
                                fields: Optional[EmbedFields]=None
                                ) -> None:
            _embed = Embed(**values)

            if not fields is None:
                _k = ["name", "value", "inline"]

                for field in fields:
                    
                    for key in _k:
                        if not key in field:
                            break

                    _embed.add_field(
                        name=field.get(_k.__getitem__(0)),
                        value=field.get(_k.__getitem__(1)),
                        inline=field.get(_k.__getitem__(2))
                    )

            _embed.set_footer(text="Beak-Utils by Qbean")

            if isinstance(metadata, Context):
                await metadata.send(embed=_embed)

            if isinstance(metadata, Interaction):
                await metadata.response.send_message(embed=_embed)

            
        @staticmethod
        async def notice_author_not_entered_channel(metadata: Metadata) -> None:
            values: EmbedValues = {
                "title" : "음성 채널에 입장 후 명령어를 입력해주세요.",
                "color" : NOTICE_EMBED_COLOR
            }

            await Messenger.Default.embed_wrapper(metadata=metadata, values=values)



    class _Selection(Block.Instanctiating):
        @staticmethod
        async def notice_teaming_result(metadata: Metadata, 
                                        team_one: List[Member], 
                                        team_two: List[Member]
                                        ) -> None:
            values: EmbedValues = {
                "title": "팀 짜기 결과",
                "description": f"총 인원: {len(team_one) + len(team_two)}명",
                "color": NOTICE_EMBED_COLOR
            }

            team_one_str: str = ""
            team_two_str: str = ""

            for member in team_one: team_one_str += f"{member.mention} "
            for member in team_two: team_two_str += f"{member.mention} "

            field1: EmbedField = {
                "name": f"1팀 ({len(team_one)}명)",
                "value": team_one_str,
                "inline": False
            }

            field2: EmbedField = {
                "name": f"2팀 ({len(team_one)}명)",
                "value": team_two_str,
                "inline": False
            }

            fields: EmbedFields = [
                field1, field2
            ]

            await Messenger.Default.embed_wrapper(metadata=metadata, values=values, fields=fields)



class Selection(Block.Instanctiating):
    @staticmethod
    async def random_teaming(ctx: Context) -> None:
        if not ContextExtractor.is_author_joined_voice_channel(ctx=ctx):
            await Messenger.Default.notice_author_not_entered_channel(metadata=ctx)

            return
            
        _bi: MemberId = Storage.Identification().get_beak_id()

        members: List[Member] = ContextExtractor.get_voice_channel_member(ctx=ctx)
        filtered_members: List[Member] = [member for member in members if not member.id == _bi]

        random.shuffle(filtered_members)

        member_number = len(filtered_members)

        pivot = int(member_number / 2) if member_number % 2 == 0 else math.floor(member_number / 2)
        print(pivot)

        team_one: List[Member] = filtered_members[:pivot]
        team_two: List[Member] = filtered_members[pivot:]

        await Messenger._Selection.notice_teaming_result(
            metadata = ctx,
            team_one = team_one,
            team_two = team_two
        )
