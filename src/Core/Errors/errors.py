# -*- coding: utf-8 -*-

class Request(Exception):
    # Request directly re-processing to supervisor
    def __init__(self, msg) -> None:
        super().__init__(msg)


class BeakErrors:
    class UnAuthorizedModuleException(Exception):
        '''
        Beak class can only be instantiated from "__main__" module
            {
                class Beak:
                    ...
                    
                    def __init__(self, __N_module: str, **kwargs) -> None:
                        if __N_module in self.__T_module:
                            Permission.allocate(**kwargs)
                        else:
        ------------------> raise UnAuthorizedModuleException
            }
        Raising UnAuthorizedModuleException on Beak::__init__(...)
        '''

        def __init__(self, __N_module: str) -> None:
            message = f"Module \"{__N_module}\" is an unauthorized module Beak instanticating"
                
            super().__init__(message)



class InfixQueueErrors:
    class InfixQueueAbnormalStatusError(Exception):
        '''
    Two or more object(like Audio) has been loaded in queue (THRESHOLD == 1)
        {
            @DecofInfixQueue.allocationinspection(ero=CommonQueueExceptions.RequiredAllocationException)
            def enqueue(self, __SI: int, _audio: Audio) -> None:
                __queue = self.queue.__getitem__(__SI)
                
                if len(__queue) == 0:
                    ...
                elif len(__queue) == THRESHOLD:
                    ...
                else:
    --------------> raise InfixQueueErrors.InfixQueueAbnormalStatusError
        }
    Raised InfixQueueAbnormalStatusError on InfixQueue::enqueue(...)
        '''
        
        
        def __init__(self, _c_name: str, _f_name, __SI: int, _l: int) -> None:
            message = f"(__SI: {__SI} executed on {_c_name}::{_f_name}) -> Queue length = {_l}" + \
                      "Queue corresponding to __SI has abnormal status"
                      
                
            super().__init__(message)
            
            

class VCStatusErrors:
    class DetectedWandererVC(Exception):
        # Handling error
        pass
    
    

class PLStatusErrors:
    class AllocationIncongruityError(Exception):
        '''
    Allocation Incongruity: Allocated to PLStatus but Unallocated to the other
        {
            @PLStatusInspector.allocationinspection()
            def %function%(self, ...) -> Any | None:
                try:
                    [ AQStatus, PrefixQueue, InfixQueue, Postfix Queue ] processing
                    
                except AQStatusExceptions.NotAllocatedException:
    --------------> raise PlStatusErrors.AllocationIncongruityError
        }
    Raised AllocationIncongruityError on PLStatus::%function%(...)
        '''
        

        def __init__(self, _c_name: str, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI}) executed on PLStatus::{_f_name}\n" + \
                      f"Allocation incongruity with PLStatus and {_c_name} about __SI={__SI}"
                
            super().__init__(message)
            
            
    
    class RequestExhalation(Request):
        '''
    Allocation Incongruity with PLStatus and VCStatus
        {
            @PLStatusInspector.allocationinspection()
            def %function%(self, ...) -> Any | None:
                try:
                    [ VCStatus ] processing
                    
                except VCStatusExceptions.NotAllocatedException:
    --------------> raise PlStatusErrors.RequestExhalation
        }
    Requested RequestExhalation to supervisor
        '''
        
        
        def __init__(self, _f_name, __SI: int) -> None:
            message = f"(__SI: {__SI}) executed on PLStatus::{_f_name}\n" + \
                      f"Allocation incongruity with PLStatus and VCStatus about __SI={__SI}\n" + \
                      "Requested integrated exhalation to supervisor"
                
            super().__init__(message)