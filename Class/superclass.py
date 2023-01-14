from typing import (
    List, Dict, Tuple,
    Any
)

from abc import ABCMeta, abstractmethod

class Singleton(type):
    _instance = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            
        return cls._instance[cls]


class Block:
    class Instanctiating:
        def __new__(cls: type[object], *args, **kwargs) -> type[object]:
            raise TypeError(f"{cls.__name__} can not be instanctiated")



class ABC:
    class AbstractQueue(metaclass=ABCMeta):
        @abstractmethod
        def enqueue(self, audios: List[Dict[str, str]]) -> None:
            pass


        @abstractmethod
        def dequeue(self) -> Dict[str, str]:
            pass


        @abstractmethod
        def insert(self, index: int, audio: Dict[str, str]) -> None:
            pass
            

        @abstractmethod
        def remove(self, index: int) -> None:
            pass


        @abstractmethod
        def seek(self, index: int) -> Dict[str, str]:
            pass
        

        @abstractmethod
        def reference(self) -> Tuple[Dict[str, str]]:
            pass


        @abstractmethod
        def get_length(self) -> int:
            pass


        @abstractmethod
        def is_empty(self) -> bool:
            pass


        @abstractmethod
        def is_single(self) -> bool:
            pass

        
        @abstractmethod
        def is_two_or_more(self) -> bool:
            pass
    

