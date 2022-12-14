# -*- coding: utf-8 -*-

import requests

from typing import Dict, Optional

from Data.Cache.settings import REQUESTS_SC



class Audio:
    __slots__ = (
        "title",                # str
        "uploader",             # str
        "thumbnail",            # str
        "audio_url",            # str
        "youtube_url",          # str
        "forbidden",            # bool
        "__fetch",              # Dict[str, bool]
    )
    
    
    def __init__(self, **kwargs) -> None:
        self.__fetch: Dict[str, bool] = { 
                info: False 
                for info in self.__slots__ 
                if not info == "__fetch" and not info == "forbidden" 
            }
        
        self.forbidden = False
        
        for _k in kwargs.keys():
            if _k in self.__slots__:
                self.__setattr__(_k, kwargs.__getitem__(_k))
                self.__fetch.__setitem__(_k, True)
                
        if self.youtube_url == "dummy":  
            self.title = "Dummy"
            self.uploader = "Qbean"
        # else:      
            # TODO: Handling 403 Exception
            # self.inspection()
        
                
                
    def __str__(self) -> str:
        if self.forbidden:
            return f"[403] {self.title} - {self.uploader}"
        
        if self.is_fetched():
            return f"[Fetched] {self.title} - {self.uploader}"
        else:
            return f"[Unfetched] {self.title} - {self.uploader}"
        
        
    def to_string(self) -> str:
        return f"{self.title} - {self.uploader}"
    
    
    def is_fetched(self) -> bool:
        return all(self.__fetch.values())
        
                
    def inspection(self) -> None:
        ERO = (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout)        

        try:
            r = requests.get(self.youtube_url, timeout=0.2)
            
            if r.status_code == REQUESTS_SC:
                self.forbidden = True
                
        except ERO:
            self.forbidden = False
    
    
    def get_info(self) -> Dict[str, Optional[str]]:
        if not self.is_fetched():
            _t = { }
            
            for k in self.__fetch.keys():
                if self.__fetch.get(k):
                    _t.__setitem__(k, self.__getattribute__(k))
                else:
                    _t.__setitem__(k, None)
                    
            return _t
        
        return { _k: self.__getattribute__(_k) for _k in self.__fetch.keys() }
    
    
    def get_url(self) -> str:
        return self.audio_url

    
    def get_original_url(self) -> str:
        return self.youtube_url