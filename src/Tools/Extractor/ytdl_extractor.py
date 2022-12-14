# -*- coding: utf-8 -*-

import asyncio

from typing import (
    Any, List, Dict
)

import youtube_dl

from Tools.Utils.printer import print_ERO

from Data.Cache.settings import YTDL_OPTION



class YtdlExtractor:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is YtdlExtractor:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    async def extract(url: str) -> List[Dict[str, str]]:
        __ytdl = youtube_dl.YoutubeDL(YTDL_OPTION)
        __ytdl.cache.remove()
        
        try:        # Section 1
            loop = asyncio.get_event_loop()
            
            e_data = await loop.run_in_executor(None, lambda: __ytdl.extract_info(url, download=False))
        except Exception as ERO:
            print_ERO(ERO, f"{__class__.__name__}::extractor() in Section 1")
            

        try:        # Section 2
            return YtdlExtractor.summarize(e_data, url)
        except Exception as ERO:
            print_ERO(ERO, f"{YtdlExtractor.__name__}::extractor() in Section 2")
        
        
    @staticmethod
    def __summarize(__data: Dict[str, Any]) -> Dict[str, str]:
        t_data: Dict[str, str] = {
            "title": __data["title"],
            "uploader": __data["uploader"].replace("- Topic", ""),
            "thumbnail": __data["thumbnails"][0]["url"],
            "audio_url": __data["url"]
        }
        
        return t_data
        
        
    @staticmethod
    def summarize(__data: Dict[str, Any], url: str) -> List[Dict[str, str]]:
        s_data: List[Dict[str, str]] = []
        
        if "playlist" in url:
            e_entity = __data["entries"]
            length = len(e_entity)
            
            for i in range(length):
                t_data = YtdlExtractor.__summarize(e_entity[i])
                t_data["youtube_url"] = url
                
                s_data.append(t_data)
                
        else:
            t_data = YtdlExtractor.__summarize(__data)
            t_data["youtube_url"] = url

            s_data.append(t_data)
        
        return s_data