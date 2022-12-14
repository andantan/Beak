# -*- coding: utf-8 -*-

from typing import List

from Types.Classes.audio import Audio


class AudioGenerator:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is AudioGenerator:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    def audioization(*args):
        _audioizated: List[Audio] = []
        
        for audio in args:
            _audioizated.append(Audio(**audio))
        else:
            return _audioizated    
    