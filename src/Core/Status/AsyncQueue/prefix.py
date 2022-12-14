# -*- coding: utf-8 -*-

from typing import List, Dict, Tuple, Optional

from Core.Errors.exceptions import CommonQueueExceptions, PrefixQueueExceptions

from Tools.Decorator.decorators import QueueInspector

from Data.Cache.settings import PREFIX_QUEUE_MAX_LENGTH

from Types.Classes import *


class PrefixQueue(metaclass=Singleton):
    __slots__ = (
        "queue",
    )
    
    __callable__: Tuple[str] = (
        "<method allocate(self, __SI: int) -> None>",
        "<method is_allocated(self, __SI: int) -> bool>",
        "<method enqueue(self, __SI: int, audioizated: List[Audio]) -> None>",
        "<method dequeue(self, __SI: int) -> Audio>",
        "<method reset(self, __SI: int) -> List[Audio]>",
        "<method refresh(self, __SI: int) -> None>",
        "<method insert(self, __SI: int, index: int, audio: Audio) -> None>",
        "<method pickout(self, __SI: int, index: int) -> Audio>",
        "<method remove(self, __SI: int, index: int) -> None>",
        "<method get_queue(self, __SI: int) -> List[Audio]>",
        "<method get_count(self, __SI: int) -> int>",
        "<method overview(self, __SI: Optional[int]=None) -> None>",
        "<method exhale(self, __SI: int) -> None>"
    )
    
    __decorater_callable__: Tuple[str] = (
        "<decorator @QueueInspector.unallocationinspection>",
        "<decorator @QueueInspector.allocationinspection>",
    )
    
    __throwable__: Tuple[str] = (
        "<exception CommonQueueExceptions.ReallocationException>",
        "<exception CommonQueueExceptions.RequiredAllocationException>",
        "<exception CommonQueueExceptions.NotAllocatedException>",
        "<exception CommonQueueExceptions.OutofQueueRangeException>"
        "<exception CommonQueueExceptions.EndOfQueueException>",
        "<exception PrefixQueueExceptions.SaturationOfQueueException>",
    )
        
    
    def __init__(self) -> None:
        self.queue: Dict[int, List[Audio]] = {}
        
    
    @classmethod
    def __callable_cell__(cls) -> Dict[str, Tuple[str]]:
        __kv = {
            "Callable": tuple([ __km for __km in cls.__callable__ ]),
            "Decorator_Callable": tuple([ __km for __km in cls.__decorater_callable__ ])
        }
        
        return __kv
    
    
    @classmethod
    def __throwable_cell__(cls) -> Tuple[str]:
        return tuple([ __km for __km in cls.__throwable__ ])
    
    
    @QueueInspector.unallocationinspection(ero=CommonQueueExceptions.ReallocationException)
    def allocate(self, __SI: int) -> None:
        self.queue.__setitem__(__SI, [ ])
        
        
    def is_allocated(self, __SI: int) -> bool:
        return __SI in self.queue
 
 
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)
    def enqueue(self, __SI: int, _audioizated: List[Audio]) -> None:
        for audio in _audioizated:
            __queue = self.queue.__getitem__(__SI)
            
            if len(__queue) < PREFIX_QUEUE_MAX_LENGTH:
                __queue.append(audio)
            else:
                raise PrefixQueueExceptions.SaturationOfQueueException
    
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)
    def dequeue(self, __SI: int) -> Audio:
        if self.queue.get(__SI):
            return self.queue.__getitem__(__SI).pop(0)
        
        else:
            raise CommonQueueExceptions.EndOfQueueException

        
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)     
    def reset(self, __SI: int) -> List[Audio]:
        _alist: List[Audio] = [ ]
            
        while self.queue.__getitem__(__SI):
            _alist.append(self.dequeue(__SI))
            
        return _alist
    
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)     
    def refresh(self, __SI: int) -> None:
        self.enqueue(__SI, self.reset(__SI))
        
        if PREFIX_QUEUE_MAX_LENGTH < len(self.queue.__getitem__(__SI)):
            self.remove(__SI, 0)
    
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)
    def insert(self, __SI: int, index: int, audio: Audio) -> None:
        __queue = self.queue.__getitem__(__SI)
        
        # if index < 0 or len(__queue) - 1 < index:
        #     raise CommonQueueExceptions.OutofQueueRangeException(
        #         self.__class__.__name__, 
        #         self.insert.__name__,
        #         __SI
        #     )
        
        if len(__queue) < PREFIX_QUEUE_MAX_LENGTH:
            __queue.insert(index, audio)
        else:
            raise PrefixQueueExceptions.SaturationOfQueueException
        
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)
    def pickout(self, __SI: int, index: int) -> Audio:
        # __queue = self.queue.__getitem__(__SI)

        # if index < -1 * len(__queue) or len(__queue) - 1 < index:
        #     raise CommonQueueExceptions.OutofQueueRangeException(
        #         self.__class__.__name__, 
        #         self.pickout.__name__,
        #         __SI
        #     )
            
        return self.queue.__getitem__(__SI).pop(index)
        
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)   
    def remove(self, __SI: int, index: int) -> None:
        # __queue = self.queue.__getitem__(__SI)

        # if index < 0 or len(__queue) - 1 < index:
        #     raise CommonQueueExceptions.OutofQueueRangeException(
        #         self.__class__.__name__, 
        #         self.remove.__name__,
        #         __SI
        #     )
            
        self.queue.__getitem__(__SI).pop(index)
        
        
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.NotAllocatedException)   
    def get_queue(self, __SI: int) -> List[Audio]:
        return self.queue.__getitem__(__SI)
    
    
    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.NotAllocatedException)
    def get_count(self, __SI: int) -> int:
        return len(self.queue.__getitem__(__SI))
    

    @QueueInspector.allocationinspection(ero=CommonQueueExceptions.NotAllocatedException)
    def overview(self, __SI: Optional[int]=None) -> None:
        print(f"{self.__class__.__name__}" + " = {\n" + f"\t{__SI}: [")
        
        if __SI == None:
            raise NotImplementedError
            # for __ID, audios in self.queue.items():
            #     for audio in audios:
            #         print(f"\t\t{str(audio)}")   
                
        else:
            for audio in self.queue.__getitem__(__SI)[::-1]:
                print(f"\t\t{str(audio)}") 
                
        print("\t]\n}")
    

    def exhale(self, __SI: int) -> None:
        if self.is_allocated(__SI):
            del self.queue[__SI]

