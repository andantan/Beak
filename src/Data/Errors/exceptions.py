# -*- coding: utf-8 -*-


class PermissionExceptions:
    class ReallocationException(Exception):
        '''
    Permission has been already allocated but reallocation has been executed
        {
            @classmethod
            def allocate(cls, **kwargs) -> None:
                _alloc: List[bool] = [False, False]
            
                if cls.__info.get(cls.__config__.__getitem__(0)) == None and \
                    cls.__info.get(cls.__config__.__getitem__(1)) == None:
                    ...
                else
    --------------> raise PermissionExceptions.ReallocationException(...)
        }
    Raised ReallocationException on Permission::allocate(...)
        '''
            
                    
        def __init__(self, _id: int, _name: str) -> None:
            message = f"Already allocated(__id__: {_id}, __name__: {_name})"
                
            super().__init__(message)
            
            
            
    class ReRegistrationException(Exception):
        '''
    Permission has been already registered but re-registration has been executed
        {
            @classmethod
            def register(cls) -> None:
                if cls.__allocated:
                    if getattr(cls, cls.__required__.__getitem__(0)) == None:
                        ...
                    else:
    -------------------> raise PermissionExceptions.ReRegistrationException
                else:
                    ...
        }
    Raised ReRegistrationException on Permission::register(...)
        '''
                
                    
        def __init__(self, _id: int) -> None:
            private = list(str(_id))
            
            private[-5: -1] = "****"
            private[-10: -8] = "**"
            private[-17: -14] = "***"
            
            fmsg = "".join(private)
            
            message = f"Already registered admin-id(__adminId: {fmsg})"
                
            super().__init__(message)
            
            

    class RequiredAllocationException(Exception):
        '''
    Permission does not allocated but registration admin-id has been executed
        {
            @classmethod
            def register(cls) -> None:
                if cls.__allocated:
                    ...
                else:
    ---------------> raise PermissionExceptions.RequiredAllocationException
        }
    Raised RequiredAllocationException on Permission::register(...)
        '''
            
                    
        def __init__(self) -> None:
            super().__init__("ColliePermission does not allocated")
            


class MessageStorageExceptions:
    class ReallocationException(Exception):
        # Handling Exception
        pass
    
    
    
    class RequiredAllocationException(Exception):
        # Handling Exception
        pass
    
    
    
    class NotAllocatedException(Exception):
        # Handling Exception
        pass
    
    
    
class ContextStorageExceptions:
    class ReallocationException(Exception):
        # Handling Exception
        pass
    
    
    
    class RequiredAllocationException(Exception):
        # Handling Exception
        pass
    
    
    
    class NotAllocatedException(Exception):
        # Handling Exception
        pass
