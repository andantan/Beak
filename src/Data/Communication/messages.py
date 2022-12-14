# -*- coding: utf-8 -*-

from typing import Dict, Optional

from discord import Message

from Data.Errors.exceptions import MessageStorageExceptions

from Types.Classes.metaclass import Singleton


class MessageStorage(metaclass=Singleton):
    __slots__ = (
        "__messages",
    )
    
    
    def __init__(self) -> None:
        self.__messages: Dict[int, Optional[Message]] = { }
        
    
    def allocate(self, __SI: int) -> None:
        if self.is_allocated(__SI):
            raise MessageStorageExceptions.ReallocationException
        
        self.__messages.__setitem__(__SI, None)
        
    
    def is_allocated(self, __SI: int) -> None:
        return __SI in self.__messages 
    
    
    def updatemsg(self, __SI: int, msg: Optional[Message]=None) -> None:
        if not self.is_allocated(__SI):
            raise MessageStorageExceptions.RequiredAllocationException
            
        self.__messages.__setitem__(__SI, msg)
            
            
    def conditmsg(self, __SI: int) -> Optional[Message]:
        if not self.is_allocated(__SI):
            raise MessageStorageExceptions.RequiredAllocationException

        return self.__messages.get(__SI)
    
    
    def exhale(self, __SI: int) -> None:
        if self.is_allocated(__SI):
            del self.__messages[__SI]
