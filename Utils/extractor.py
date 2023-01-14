from typing import (
    Dict, List,
    Any, 
    Optional, Union
)

import asyncio

import youtube_dl
import discord

from discord.channel import VoiceChannel, StageChannel
from discord.ext.commands.context import Context, Interaction

from Class.superclass import Block

from Data.Paraments.settings import YTDL_OPTION

from Core.Cache.storage import Storage


class YoutubeDlExtractor(Block.Instanctiating):
    @staticmethod
    async def extract(URL: str, DEBUG=False) -> Union[List[Dict[str, str]], Dict[str, Any], None]:
        __ytdl = youtube_dl.YoutubeDL(YTDL_OPTION)
        __ytdl.cache.remove()

        try:
            loop = asyncio.get_event_loop()

            extracted_data = await loop.run_in_executor(None, lambda: __ytdl.extract_info(URL, download=False))
            
        except Exception as ERO:
            print(ERO)
            loop.close()

        if DEBUG:
            return extracted_data

        return YoutubeDlExtractor.summarize(extracted_data, URL)


    def summarize(extracted_data: Dict[str, Any], URL: str) -> List[Dict[str, str]]:

        def entity_summarize(extracted_data: Dict[str, Any], URL: str) -> Dict[str, str]:
            summrized_audio_info = {
                "title": extracted_data.get("title"),
                "uploader": extracted_data.get("uploader").replace("- Topic", ""),
                "original_url": URL,
                "audio_url": extracted_data.get("url"),
                "duration": extracted_data.get("duration"),
                "thumbnail": extracted_data.get("thumbnail")
                
            }
            
            return summrized_audio_info

        if "playlist" in URL:
            playlist = list()

            playlist_entities: List[Any] = extracted_data.get("entries")
            playlist_title: str = playlist_entities.__getitem__(0).get("playlist_title")
            
            for i in range(0, len(playlist_entities)):
                entity = entity_summarize(playlist_entities.__getitem__(i), URL)

                entity.__setitem__("playlist_title", playlist_title)
                
                playlist.append(entity)

            else:
                return playlist
                
        else:
            entity = list()

            entity.append(entity_summarize(extracted_data, URL))

            return entity



class ContextExtractor(Block.Instanctiating):
    @staticmethod
    def summarize(ctx: Context) -> Dict[str, Optional[str]]:
        guild: discord.Guild = ctx.guild
        author: discord.Member = ctx.author
        channel: discord.abc.Messageable = ctx.channel
        
        beak: discord.Member = ContextExtractor.get_beak_member(ctx)
        
        author_voice_state: Optional[discord.VoiceState] = author.voice
        beak_voice_state: Optional[discord.VoiceState] = beak.voice
        
        summarized: Dict[str, Optional[str]] = {  
            # guild_name                                # 서버 이름
            "GN": guild.name,      

            # guild_id                                  # 서버 ID
            "GI": guild.id,             

            # author_name                               # 명령어 입력한 유저 이름   
            "AN": author.name,                              
            
            # author_id                                 # 명령어 입력한 유저 ID
            "AI": author.id,                                 
            
            # commander_executed_chatting_channel_name  # 명령어 입력한 텍스트 채털 이름
            "CECCN": channel.name,              
            
            # commander_executed_chatting_channel_id    # 명령어 입력한 텍스트 채널 ID
            "CECCI": channel.id,                
            
            # commander_entered_voice_channel_name      # 명령어 입력한 유저가 입장한 채널 이름 (없으면 None)
            "CEVCN": None,                   
            
            # commander_entered_voice_channel_id        # 명령어 입력한 유저가 입장한 채널 ID (없으면 None) 
            "CEVCI": None,                     
            
            # bot_entered_voice_channel_name            # 봇이 입장한 채널 이름 (없으면 None)
            "BEVCN": None,                         
            
            # bot_entered_voice_channel_id              # 봇이 입장한 채널 ID (없으면 None)
            "BEVCI": None,                           
        }

        if author_voice_state is not None:
            summarized["CEVCN"] = author_voice_state.channel.name
            summarized["CEVCI"] = author_voice_state.channel.id
            
        if beak_voice_state is not None:
            summarized["BEVCN"] = beak_voice_state.channel.name
            summarized["BEVCI"] = beak_voice_state.channel.id

        return summarized

    
    @staticmethod
    def get_beak_member(ctx: Context) -> discord.Member:
        return ctx.guild.get_member(Storage.Identification().get_beak_id())


    @staticmethod
    def get_author_entered_voice_channel(ctx: Context) -> Union[VoiceChannel, StageChannel, None]:
        '''
        Get author entered channel from Context.\n
        Returns the VoiceGuildChannel if the author has entered the voice channel, otherwise returns None.\n
        A Shortcut method to ctx.author.voice.channel
        '''
        if ContextExtractor.get_author_entered_channel_id(ctx) is None:
            return None

        return ctx.author.voice.channel
    

    @staticmethod
    def get_guild_name(ctx: Context) -> str:
        '''
        Get guild name from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("GN")
        '''

        return ctx.guild.name


    @staticmethod   
    def get_guild_id(ctx: Context) -> int:
        '''
        Get guild identification from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("GI")
        '''
        
        return ctx.guild.id

    
    @staticmethod
    def get_author_name(ctx: Context) -> str:
        '''
        Get author name from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("AN")
        '''
        
        return ctx.author.name
    
    
    @staticmethod
    def get_author_id(ctx: Context) -> int:
        '''
        Get author identification from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("AI")
        '''
        
        return ctx.author.id


    @staticmethod
    def get_channel_name(ctx: Context) -> str:
        '''
        Get channel name from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("CECCN")
        '''

        return ctx.channel.name


    @staticmethod
    def get_channel_id(ctx: Context) -> str:
        '''
        Get channel identification from Context.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("CECCI")
        '''

        return ctx.channel.id


    @staticmethod
    def get_author_entered_channel_name(ctx: Context) -> Optional[str]:
        '''
        Get author entered channel name from Context.\n
        Returns the voice channel name if the author has entered the voice channel, otherwise returns None.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("CEVCN")
        '''
        
        author_voice_state: Optional[discord.VoiceState] = ctx.author.voice
        
        if author_voice_state is None:
            return author_voice_state
        
        return author_voice_state.channel.name


    @staticmethod
    def get_author_entered_channel_id(ctx: Context) -> Optional[int]:
        '''
        Get author entered channel identification from Context.\n
        Returns the voice channel identification if the author has entered the voice channel, otherwise returns None.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("CEVCI")
        '''

        author_voice_state: Optional[discord.VoiceState] = ctx.author.voice
        if author_voice_state is None:
            return None

        id = author_voice_state.channel.id

        return id


    @staticmethod
    def get_beak_entered_channel_name(ctx: Context) -> Optional[str]:
        '''
        Get beak entered channel name from Context.\n
        Returns the voice channel name if Beak has entered the voice channel, otherwise returns None.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("BEVCN")
        '''

        beak_voice_state: Optional[discord.VoiceState] = ContextExtractor.get_beak_member(ctx).voice

        if beak_voice_state is None:
            return None
        
        return beak_voice_state.channel.name


    @staticmethod
    def get_beak_entered_channel_id(ctx: Context) -> Optional[int]:
        '''
        Get beak entered channel identification from Context.\n
        Returns the voice channel identification if Beak has entered the voice channel, otherwise returns None.\n
        A Shortcut method to ContextExtractor.summarize(ctx).get("BEVCI")
        '''

        beak_voice_state: Optional[discord.VoiceState] = ContextExtractor.get_beak_member(ctx).voice

        if beak_voice_state is None:
            return beak_voice_state

        id = beak_voice_state.channel.id

        return id

    
    @staticmethod
    def is_beak_joined_voice_channel(ctx: Context) -> bool:
        return bool(ContextExtractor.get_beak_entered_channel_id(ctx))
    
    
    @staticmethod
    def is_author_joined_voice_channel(ctx: Context) -> bool:
        return bool(ContextExtractor.get_author_entered_channel_id(ctx))
    

    @staticmethod
    def is_beak_and_author_same_voice_channel(ctx: Context) -> bool:
        if not ContextExtractor.is_beak_joined_voice_channel(ctx):
            return False
            
        if not ContextExtractor.is_author_joined_voice_channel(ctx):
            return False

        return ContextExtractor.get_author_entered_channel_id(ctx) == ContextExtractor.get_beak_entered_channel_id(ctx)



class InteractionExtractor(Block.Instanctiating):
    @staticmethod
    def summarize(interaction: Interaction) -> Dict[str, Optional[str]]:
        guild: discord.Guild = interaction.guild
        user: discord.Member = interaction.user
        
        beak: discord.Member = InteractionExtractor.get_beak_member(interaction=interaction)
        
        author_voice_state: Optional[discord.VoiceState] = user.voice
        beak_voice_state: Optional[discord.VoiceState] = beak.voice
        
        summarized: Dict[str, Optional[str]] = {  
            # guild_name                                # 서버 이름
            "GN": guild.name,      

            # guild_id                                  # 서버 ID
            "GI": guild.id,             

            # user_name                                 # 버튼을 클릭한 유저 이름   
            "UN": user.name,                              
            
            # user_id                                   # 버튼을 클릭한 유저 ID
            "UI": user.id,                                 

            # commander_entered_voice_channel_name      # 버튼을 클릭한 유저가 입장한 채널 이름 (없으면 None)
            "CEVCN": None,                   
            
            # commander_entered_voice_channel_id        # 버튼을 클릭한 유저가 입장한 채널 ID (없으면 None) 
            "CEVCI": None,                     
            
            # beak_entered_voice_channel_name            # 봇이 입장한 채널 이름 (없으면 None)
            "BEVCN": None,                         
            
            # beak_entered_voice_channel_id              # 봇이 입장한 채널 ID (없으면 None)
            "BEVCI": None,                           
        }

        if author_voice_state is not None:
            summarized["CEVCN"] = author_voice_state.channel.name
            summarized["CEVCI"] = author_voice_state.channel.id
            
        if beak_voice_state is not None:
            summarized["BEVCN"] = beak_voice_state.channel.name
            summarized["BEVCI"] = beak_voice_state.channel.id

        return summarized

    
    @staticmethod
    def get_beak_member(interaction: Interaction) -> discord.Member:
        return interaction.guild.get_member(Storage.Identification().get_beak_id())


    @staticmethod
    def get_user_entered_voice_channel(interaction: Interaction) -> Union[VoiceChannel, StageChannel, None]:
        '''
        Get author entered channel from Interaction.\n
        Returns the VoiceGuildChannel if the author has entered the voice channel, otherwise returns None.\n
        A Shortcut method to interaction.author.voice.channel
        '''
        if InteractionExtractor.get_user_entered_channel_id(interaction) is None:
            return None

        return interaction.user.voice.channel
    

    @staticmethod
    def get_guild_name(interaction: Interaction) -> str:
        '''
        Get guild name from Interaction.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("GN")
        '''

        return interaction.guild.name


    @staticmethod   
    def get_guild_id(interaction: Interaction) -> int:
        '''
        Get guild identification from Interaction.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("GI")
        '''
        
        return interaction.guild.id

    
    @staticmethod
    def get_user_name(interaction: Interaction) -> str:
        '''
        Get user name from Interaction.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("UN")
        '''
        
        return interaction.user.name
    
    
    @staticmethod
    def get_user_id(interaction: Interaction) -> int:
        '''
        Get user identification from Interaction.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("UI")
        '''
        
        return interaction.user.id


    @staticmethod
    def get_user_entered_channel_name(interaction: Interaction) -> Optional[str]:
        '''
        Get user entered channel name from Interacion.\n
        Returns the voice channel name if the user has entered the voice channel, otherwise returns None.\n
        A Shortcut method to Interaction.summarize(interaction).get("CEVCN")
        '''
        
        user_voice_state: Optional[discord.VoiceState] = interaction.user.voice
        
        if user_voice_state is None:
            return user_voice_state
        
        return user_voice_state.channel.name


    @staticmethod
    def get_user_entered_channel_id(interaction: Interaction) -> Optional[int]:
        '''
        Get user entered channel identification from Interaction.\n
        Returns the voice channel identification if the user has entered the voice channel, otherwise returns None.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("CEVCI")
        '''

        user_voice_state: Optional[discord.VoiceState] = interaction.user.voice

        if user_voice_state is None:
            return None

        id = user_voice_state.channel.id

        return id


    @staticmethod
    def get_beak_entered_channel_name(ctx: Context) -> Optional[str]:
        '''
        Get beak entered channel name from Interaction.\n
        Returns the voice channel name if Beak has entered the voice channel, otherwise returns None.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("BEVCN")
        '''

        beak_voice_state: Optional[discord.VoiceState] = InteractionExtractor.get_beak_member(ctx).voice

        if beak_voice_state is None:
            return None
        
        return beak_voice_state.channel.name


    @staticmethod
    def get_beak_entered_channel_id(interaction: Interaction) -> Optional[int]:
        '''
        Get beak entered channel identification from Interaction.\n
        Returns the voice channel identification if Beak has entered the voice channel, otherwise returns None.\n
        A Shortcut method to InteractionExtractor.summarize(interaction).get("BEVCI")
        '''

        beak_voice_state: Optional[discord.VoiceState] = InteractionExtractor.get_beak_member(interaction).voice

        if beak_voice_state is None:
            return beak_voice_state

        id = beak_voice_state.channel.id

        return id

    
    @staticmethod
    def is_beak_joined_voice_channel(interaction: Interaction) -> bool:
        return bool(InteractionExtractor.get_beak_entered_channel_id(interaction))

    
    @staticmethod
    def is_user_joined_voice_channel(interaction: Interaction) -> bool:
        return bool(InteractionExtractor.get_user_entered_channel_id(interaction))
    

    @staticmethod
    def is_beak_and_user_same_voice_channel(interaction: Interaction) -> bool:
        if not InteractionExtractor.is_beak_joined_voice_channel(interaction):
            return False
            
        if not InteractionExtractor.is_user_joined_voice_channel(interaction):
            return False

        user_entered_channel_id = InteractionExtractor.get_user_entered_channel_id(interaction)
        beak_entered_channel_id = InteractionExtractor.get_beak_entered_channel_id(interaction)

        return user_entered_channel_id == beak_entered_channel_id
