from typing import (
    Dict, Tuple, List,
    Union, Optional,
)

from final_class import final

from Tools.Extractor.file_extractor import id_reader

from Data.Errors.exceptions import PermissionExceptions


Un_TVN = Union[str, int, None]


@final
class Permission:
    __slots__ = ( )

    __config__: Tuple[str] = (
        "__id__",
        "__name__",
    )
    
    __required__: Tuple[str] = (
        "__adminId",
    )

    __info: Dict[str, Union[str, int, None]] = {
        __config__.__getitem__(0) : None,
        __config__.__getitem__(1) : None
    }
    
    __allocated: Optional[bool] = None
    __adminId: Optional[int] = None


    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is Permission:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)

    
    @classmethod
    def __str__(cls) -> str:
        message: str = f"{cls.__name__}" + " = {\n"

        for _k in cls.__config__:
            message += f"   {_k}: {cls.__info.get(_k)}\n"
            
        for _k in cls.__required__:
            message += f"   {_k}: {getattr(cls, f'_{cls.__name__}{cls.__required__.__getitem__(0)}')}\n"
        else:
            message += "}"
            
        return message


    @classmethod
    def allocate(cls, **kwargs) -> None:
        _alloc: List[bool] = [False, False]
        
        if cls.__info.get(cls.__config__.__getitem__(0)) == None and cls.__info.get(cls.__config__.__getitem__(1)) == None:
            for _k in kwargs.keys():
                if _k in cls.__config__:
                    _KV = kwargs.__getitem__(_k)
                    _i = cls.__config__.index(_k)
                    
                    if ((type(_KV) == int) and (_i == 0)) or ((type(_KV) == str) and (_i == 1)):
                        cls.__info.__setitem__(_k, _KV)
                        _alloc[_i] = True
        else:            
           raise PermissionExceptions.ReallocationException(
               cls.__info.get(cls.__config__.__getitem__(0)), 
               cls.__info.get(cls.__config__.__getitem__(1))
            )
       
        cls.__allocated = all(_alloc)


    @classmethod
    def is_allocated(cls) -> bool:
        return cls.__allocated


    @classmethod
    def register(cls) -> None:
        if cls.__allocated:
            __h_attr = "_" + cls.__name__ + cls.__required__.__getitem__(0)
            
            if getattr(cls, __h_attr) == None:
                setattr(cls, __h_attr, id_reader())
                    
            else:
                raise PermissionExceptions.ReRegistrationException(
                    getattr(cls, __h_attr)
                )
        else:
            raise PermissionExceptions.RequiredAllocationException


    @classmethod
    def get_admin_id(cls) -> Optional[int]:
        return cls.__adminId
    
    
    @classmethod
    def get_beak_id(cls) -> Optional[int]:
        if not cls.__allocated:
            return None
        
        return cls.__info.get(cls.__config__.__getitem__(0))
    
    
    @classmethod
    def get_beak_name(cls) -> Optional[str]:
        if not cls.__allocated:
            return None
        
        return cls.__info.get(cls.__config__.__getitem__(1))