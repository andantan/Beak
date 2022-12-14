from typing import Dict

from Types.Classes.metaclass import Singleton


class AllocatedPool(metaclass=Singleton):
    __slots__ = (
        "__pool",
    )
    
    
    def __init__(self) -> None:
        self.__pool: Dict[int, bool] = { }
        
        
    def run(self, __SI: int) -> None:
        if not __SI in self.__pool:
            self.__pool.__setitem__(__SI, True)
    
    
    def inturrupt(self, __SI: int) -> None:
        if __SI in self.__pool:
            self.__pool.__setitem__(__SI, False)
            
            
    def flag(self, __SI: int) -> bool:
        if __SI in self.__pool:
            return self.__pool.__getitem__(__SI)
            
            
    def exhale(self, __SI: int) -> None:
        if __SI in self.__pool and not self.__pool.__getitem__(__SI):
            del self.__pool[__SI]