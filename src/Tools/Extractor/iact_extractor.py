# -*- coding: utf-8 -*-

from typing import Dict, Union

from discord import Interaction

from Data.permission import Permission


Dictx = Dict[str, Union[str, int, None]]


class InteractionExtractor:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is InteractionExtractor:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    def summarize(interaction: Interaction) -> Dictx:
        beak = interaction.guild.get_member(Permission.get_beak_id())
        
        summarized: Dictx = {                      
            # server_id                                 # 서버 ID
            "SI": interaction.guild.id,                                      
            
            # server_name                               # 서버 이름
            "SN": interaction.guild.name,      
                             
            # commander_name                            # 명령어 입력한 유저 이름   
            "CN": interaction.user.name,                              
            
            # commander_id                              # 명령어 입력한 유저 ID
            "CI": interaction.user.id,                                 
            
            # commander_executed_text_channel_name      # 명령어 입력한 텍스트 채털 이름
            "CETCN": interaction.channel.name,              
            
            # commander_executed_text_channel_id        # 명령어 입력한 텍스트 채널 ID
            "CETCI": interaction.channel.id,                
            
            # commander_entered_voice_channel_name      # 명령어 입력한 유저가 입장한 채널 이름 (없으면 None)
            "CEVCN": None,                   
            
            # commander_entered_voice_channel_id        # 명령어 입력한 유저가 입장한 채널 ID (없으면 None) 
            "CEVCI": None,                     
            
            # bot_entered_voice_channel_name            # 봇이 입장한 채널 이름 (없으면 None)
            "BEVCN": None,                         
            
            # bot_entered_voice_channel_id              # 봇이 입장한 채널 ID (없으면 None)
            "BEVCI": None,                           
        }
        
        if interaction.user.voice:
            summarized["CEVCN"] = interaction.user.voice.channel.name
            summarized["CEVCI"] = interaction.user.voice.channel.id
            
        if beak.voice:
            summarized["BEVCN"] = beak.voice.channel.name
            summarized["BEVCI"] = beak.voice.channel.id

        return summarized
    
    
    @staticmethod
    def get_guild_id(interaction: Interaction) -> int:
        return interaction.guild.id
    
    
    @staticmethod
    def get_author_id(interaction: Interaction) -> int:
        return interaction.user.id
    
    
    @staticmethod
    def is_bot_joined_voice_channel(interaction: Interaction) -> bool:
        return bool(interaction.guild.get_member(Permission.get_beak_id()).voice)
    
    
    @staticmethod
    def is_commander_joined_voice_channel(interaction: Interaction) -> bool:
        return bool(interaction.user.voice)
    
    
    @staticmethod
    def is_same_voice_channel(interaction: Interaction) -> bool:
        if not InteractionExtractor.is_bot_joined_voice_channel(interaction):
            return False
        if not InteractionExtractor.is_commander_joined_voice_channel(interaction):
            return False
        
        summrized = InteractionExtractor.summarize(interaction)
        
        return summrized.get("CEVCI") == summrized.get("BEVCI")