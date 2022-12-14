# -*- coding: utf-8 -*-

from typing import Dict, Union

from Data.permission import Permission

from discord.ext.commands.context import Context


Dictx = Dict[str, Union[str, int, None]]


class ContextExtractor:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is ContextExtractor:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    

    @staticmethod
    def summarize(ctx: Context) -> Dictx:
        beak = ctx.guild.get_member(Permission.get_beak_id())
        
        summarized: Dictx = {                      
            # server_id                                 # 서버 ID
            "SI": ctx.guild.id,                                      
            
            # server_name                               # 서버 이름
            "SN": ctx.guild.name,      
                             
            # commander_name                            # 명령어 입력한 유저 이름   
            "CN": ctx.author.name,                              
            
            # commander_id                              # 명령어 입력한 유저 ID
            "CI": ctx.author.id,                                 
            
            # commander_executed_text_channel_name      # 명령어 입력한 텍스트 채털 이름
            "CETCN": ctx.channel.name,              
            
            # commander_executed_text_channel_id        # 명령어 입력한 텍스트 채널 ID
            "CETCI": ctx.channel.id,                
            
            # commander_entered_voice_channel_name      # 명령어 입력한 유저가 입장한 채널 이름 (없으면 None)
            "CEVCN": None,                   
            
            # commander_entered_voice_channel_id        # 명령어 입력한 유저가 입장한 채널 ID (없으면 None) 
            "CEVCI": None,                     
            
            # bot_entered_voice_channel_name            # 봇이 입장한 채널 이름 (없으면 None)
            "BEVCN": None,                         
            
            # bot_entered_voice_channel_id              # 봇이 입장한 채널 ID (없으면 None)
            "BEVCI": None,                           
            
        }
        
        if ctx.author.voice:
            summarized["CEVCN"] = ctx.author.voice.channel.name
            summarized["CEVCI"] = ctx.author.voice.channel.id
            
        if beak.voice:
            summarized["BEVCN"] = f"{beak.voice.channel}"
            summarized["BEVCI"] = beak.voice.channel.id

        return summarized
    
    
    @staticmethod
    def get_guild_id(ctx: Context) -> int:
        return ctx.guild.id
    
    
    @staticmethod
    def get_author_id(ctx: Context) -> int:
        return ctx.author.id
    
    
    @staticmethod
    def is_bot_joined_voice_channel(ctx: Context) -> bool:
        return bool(ctx.guild.get_member(Permission.get_beak_id()).voice)
    
    
    @staticmethod
    def is_commander_joined_voice_channel(ctx: Context) -> bool:
        return bool(ctx.author.voice)
    

    @staticmethod
    def is_same_voice_channel(ctx: Context) -> bool:
        if not ContextExtractor.is_bot_joined_voice_channel(ctx):
            return False
        if not ContextExtractor.is_commander_joined_voice_channel(ctx):
            return False
        
        summrized = ContextExtractor.summarize(ctx)
        
        return summrized.get("CEVCI") == summrized.get("BEVCI")