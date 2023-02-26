from typing import Dict, List, Union, Optional, Any

from discord import Embed
from discord.voice_client import VoiceClient
from discord.channel import VoiceChannel, StageChannel
from discord.ext.commands.context import Context, Interaction


Version = str

Metadata = Union[Context, Interaction]
EmbedField = Dict[str, Union[str, Any]]
EmbedFields = List[Dict[str, Union[str, Any]]]
EmbedValues = Dict[str, str]
VoiceStreamChannel = Union[VoiceChannel, StageChannel, None]