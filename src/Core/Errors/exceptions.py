# -*- coding: utf-8 -*-

class CommonQueueExceptions:
    class ReallocationException(Exception):
        '''
    Queue corresponding to __SI has been already allocated but reallocation has been executed
        {
            @QueueInspector.allocationinspection(...)
            def allocate(self, __SI: int) -> None:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise CommonQueueExceptions.ReallocationException
        }
    Raised ReallocationException on %position%Queue::allocate(...)
        '''
            
                    
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      f"{_c_name} corresponding to {__SI} has been already allocated"       
                               
            super().__init__(message)
            
            
    
    class RequiredAllocationException(Exception):
        '''
    Queue corresponding to __SI does not allocated but processing/control has been executed
        {
            @QueueInspector.allocationinspection(...)
            def %function%(self, __SI: int, ...) -> ...:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise CommonQueueExceptions.RequiredAllocationException
        }
    Raised RequiredAllocationException on %position%Queue::%funcion%(...)
        '''
            
                    
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      "Allocation required for data processing and control"
            
            super().__init__(message)
            
            

    class NotAllocatedException(Exception):
        '''
    Queue corresponding to __SI does not allocated but data-access has been executed
        {
            @QueueInspector.allocationinspection(...)
            def %function%(self, __SI: int, ...) -> ...:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise CommonQueueExceptions.NotAllocatedException
        }
    Raised NotAllocatedException on %position%Queue::%funcion%(...)
        '''
        
        
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      "Detected access to unallocated queue"
                
            super().__init__(message)
            
            
            
    class OutofQueueRangeException(Exception):
        '''
    Element in parameter(int) does over length of Queue corresponding to __SI
        {
            @QueueInspector.allocationinspection(...)
            def %function%(self, __SI: int, element: int ...) -> ...:
                if {% element validator %}:
    --------------> raise CommonQueueExceptions.OutofQueueRangeException
                ...
        }
    Raised OutofQueueRangeException on %position%Queue::remove(...)
        '''
            
            
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      f"element is out of Queue corresponding to __SI range"
                
            super().__init__(message) 
        
            
            
    class EndOfQueueException(Exception):
        # Handling Exception
        pass
    
    

class PrefixQueueExceptions:
    class SaturationOfQueueException(Exception):
        #Handling Exception
        pass
    
    

class InfixQueueExceptions:
    class StillLinedUpInQueueException(Exception):
        '''
    Some object(like Audio) remains in InfixQueue.queue (THRESHOLD == 1)
        {
            @QueueInspector.allocationinspection(...)
            def enqueue(self, __SI: int, _audio: Audio) -> None:
            __queue = self.queue.__getitem__(__SI)
                
                if length == 0:
                    ...
                elif length == THRESHOLD:
    --------------> raise InfixQueueExceptions.StillLinedUpInQueueException
                else:
                    ...
        }
    Raised StillLinedUpInQueueException on InfixQueue::enqueue(...)
        '''
        
        
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI} executed on {_c_name}::{_f_name})\n" + \
                      "Queue corresponding to __SI still staging or does not dequeued"
                      
                
            super().__init__(message)
            
        
    class EnteredObjectWhileRefreshing(Exception):
        '''
    Some object(like Audio) enqueued or inserted while refreshing (THRESHOLD == 1)
        {
            @QueueInspector.allocationinspection(...)     
            def refresh(self, __SI: int) -> None:
                self.enqueue(__SI, self.reset(__SI))
                
                if THRESHOLD < len(self.queue.__getitem__(__SI)):
    --------------> raise InfixQueueExceptions.EnteredObjectWhileRefreshing
        }
    Raised EnteredObjectWhileRefreshing on InfixQueue::refresh(...)
        '''
        

        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = "Queue corresponding to __SI refreshing detected THRESHOLD break\n" + \
                      f"(__SI: {__SI} executed on {_c_name}::{_f_name})"
                
            super().__init__(message)
    


class PostfixQueueExceptions:
    class SaturationOfQueueException(Exception):
        #Handling Exception
        pass
    
    
    
class AQStatusExceptions:
    class NotAllocatedException(Exception):
        '''
    Queue corresponding to __SI does not allocated but data-access through AQStatus has been executed
        {
            @staticmethod
            def allocationinspection(ero: Exception):
                def _decof(func: Callable):
                    def wrapper(*args, **kwargs):
                        ...
                            
                        __all = [ __queue.is_allocated(__SI) for __queue in __queues ]
                            
                        __alloc = all(__all)
                            
                        if __alloc:   
                            ...
                        else:
                            for _pos, __q in enumerate(__all):
                                if not __q:
    ----------------------------------> raise AQStatusExceptions.NotAllocatedException
    
                    return wrapper
                return _decof
        }
    Raised NotAllocatedException on StatusInspector::@allocationinspection(...)
        '''
        
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed through AQStatus::{_f_name}\n" + \
                      "Detected access through AQStatus to unallocated queue\n"
                
            super().__init__(message)
            
            
            
class VCStatusExceptions:
    class ReallocationException(Exception):
        '''
    Dvc corresponding to __SI has been already allocated but reallocation has been executed
        {
           @VCStatusInspector.unallocationinspection(...)
            def allocate(self, __SI: int) -> None:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise VCStatusExceptions.ReallocationException
        }
    Raised ReallocationException on VCStatus::allocate(...)
        '''
            
                    
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(Queue: {_c_name}, __SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      f"Dvc corresponding to {__SI} has been already allocated"       
                               
            super().__init__(message)
            
            

    class NotAllocatedException(Exception):
        '''
    Dvc corresponding to __SI does not allocated but data-access has been executed
        {
            @VCStatusInspector.allocationinspection(...)
            def %function%(self, __SI: int, ...) -> ...:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise VCStatusExceptions.NotAllocatedException
        }
    Raised NotAllocatedException on %position%Queue::%funcion%(...)
        '''
        
        
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      "Detected access to unallocated queue\n"
                
            super().__init__(message)
            
            

class PLStatusExceptions:
    class ReallocationException(Exception):
        '''
    Status corresponding to __SI has been already allocated but reallocation has been executed
        {
           @PLtatusInspector.unallocationinspection(...)
            def allocate(self, __SI: int) -> None:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise PLStatusExceptions.ReallocationException
        }
    Raised ReallocationException on PLStatus::allocate(...)
        '''
    
    
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      "Detected access to unallocated queue\n"
                
            super().__init__(message)
    
    
    class NotAllocatedException(Exception):
        '''
    Status corresponding to __SI does not allocated but data-access has been executed
        {
            @PLStatusInspector.allocationinspection(...)
            def %function%(self, __SI: int, ...) -> ...:
                if self.is_allocated(__SI):
                    ...
                else:
    --------------> raise PLStatusExceptions.NotAllocatedException
        }
    Raised NotAllocatedException on PLStatus::%funcion%(...)
        '''

    
        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      "Detected access to unallocated queue"
                
            super().__init__(message)


    class NothingInRequiredException(Exception):
        '''
    At least one of the elements in __required__ must be present in kwargs.keys()
        {
            @PLStatusInspector.allocationinspection(...)
                def update_manually(self, __SI:int, **kwargs) -> None:
                    fulfilled = [__r in kwargs.keys() for __r in self.__required__]
                    
                    if not any(fulfilled):
    -----------------> raise PLStatusExceptions.NothingInRequiredException
        }
    Raised NothingInRequiredException on PLStatus::update_manually(...)
        '''
        
        
        def __init__(self, _c_name: str, _f_name, __SI: int, required: tuple, keys: tuple) -> None:
            message = f"(__SI: {__SI}) executed on {_c_name}::{_f_name}\n" + \
                      f"Must have at least one of {required} as a key" + \
                      f", But kwargs.key() is {keys}"
                
            super().__init__(message)