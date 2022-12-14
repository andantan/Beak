from typing import Dict, Optional

from discord.ext.commands.context import Context

from Data.Errors.exceptions import ContextStorageExceptions

from Types.Classes.metaclass import Singleton


class ContextStorage(metaclass=Singleton):
    __slots__ = (
        "__contexts",
    )
    
    
    def __init__(self) -> None:
        self.__contexts: Dict[int, Optional[Context]] = { }
        
    
    def allocate(self, __SI: int) -> None:
        if self.is_allocated(__SI):
            raise ContextStorageExceptions.ReallocationException
        
        self.__contexts.__setitem__(__SI, None)
        
    
    def is_allocated(self, __SI: int) -> None:
        return __SI in self.__contexts 
    
    
    def updatectx(self, __SI: int, ctx: Optional[Context]=None) -> None:
        if not self.is_allocated(__SI):
            raise ContextStorageExceptions.RequiredAllocationException
            
        self.__contexts.__setitem__(__SI, ctx)
            
            
    def conditctx(self, __SI: int) -> Optional[Context]:
        if not self.is_allocated(__SI):
            raise ContextStorageExceptions.RequiredAllocationException

        return self.__contexts.get(__SI)
    
    
    def exhale(self, __SI: int) -> None:
        if self.is_allocated(__SI):
            del self.__contexts[__SI]
