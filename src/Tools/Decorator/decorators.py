from typing import Callable



class QueueInspector:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is QueueInspector:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    def allocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    
    
    @staticmethod
    def unallocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if not __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    


class PLStatusInspector:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is PLStatusInspector:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    def allocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    
    
    @staticmethod
    def unallocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if not __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    
    
    
class VCStatusInspector:
    def __new__(cls: type[object], *args, **kwargs) -> type[object]:
        if cls is VCStatusInspector:
            raise TypeError(f"{cls.__name__} can not be instanctiated")
        
        return object.__new__(cls, *args, **kwargs)
    
    
    @staticmethod
    def allocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    

    @staticmethod
    def coro_allocationinspection(ero: Exception):
        def _decof(func: Callable):
            async def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        await func(*args, **kwargs)
                    else:
                        return await func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    
    
    @staticmethod
    def unallocationinspection(ero: Exception):
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if not __self.is_allocated(__SI):   
                    if func.__annotations__.get("return") == None:
                        func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                else:
                    raise ero(__self.__class__.__name__, func.__name__, __SI)
            return wrapper
        return _decof
    
    
    @staticmethod
    def VCupdate():
        def _decof(func: Callable):
            def wrapper(*args, **kwargs):
                __self = args.__getitem__(0)
                
                if "__SI" in kwargs.keys():
                    __SI: int = kwargs.get("__SI")
                else:
                    __SI: int = args[1]
                    
                if func.__annotations__.get("return") == None:
                    func(*args, **kwargs)
                    
                    _dvc = __self.vcs.get(__SI)
                    __vc = _dvc.get("VC")
                    
                    _AC = __vc.is_playing() or __vc.is_paused()
                    _SC = __vc.is_connected()
                    
                    _dvc.__setitem__("AC", _AC)
                    _dvc.__setitem__("SC", _SC)
                else:
                    raise NotImplementedError("Return something")
            return wrapper
        return _decof
    
    
    
# class AQStatusInspector:
#     def __new__(cls: type[object], *args, **kwargs) -> type[object]:
#         if cls is AQStatusInspector:
#             raise TypeError(f"{cls.__name__} can not be instanctiated")
        
#         return object.__new__(cls, *args, **kwargs)
    
    
#     @staticmethod
#     def allocationinspection(ero: Exception):
#         def _decof(func: Callable):
#             def wrapper(*args, **kwargs):
#                 from Core.Player.AsyncQueue.prefix import PrefixQueue
#                 from Core.Player.AsyncQueue.infix import InfixQueue
#                 from Core.Player.AsyncQueue.postfix import PostfixQueue
                
                
#                 if "__SI" in kwargs.keys():
#                     __SI: int = kwargs.get("__SI")
#                 else:
#                     __SI: int = args[0]
                    
#                 __queues = (
#                     PrefixQueue(),
#                     InfixQueue(),
#                     PostfixQueue()
#                 )
                    
#                 __all = [ __queue.is_allocated(__SI) for __queue in __queues ]
                    
#                 __alloc = all(__all)
                    
#                 if __alloc:   
#                     if func.__annotations__.get("return") == None:
#                         func(*args, **kwargs)
#                     else:
#                         return func(*args, **kwargs)
#                 else:
#                     for _pos, __q in enumerate(__all):
#                         if not __q:
#                             raise ero(
#                                 __queues.__getitem__(_pos).__class__.__name__, 
#                                 func.__name__, 
#                                 __SI
#                             )
#             return wrapper
#         return _decof
    
    

# class CallbackInspector:
#     @staticmethod
#     def commanderinspection():
#         def _decof(func):
#             async def wrapper(*args, **kwargs):
#                 from Tools.Extractor.iact_extractor import Interaction, InteractionExtractor
#                 from Data.Cache.settings import DEFAULT_DELAY
                
#                 iact: Interaction
                
#                 if "interaction" in kwargs.keys():
#                     iact = kwargs.get("interaction")
#                 else:
#                     iact = args[0]
                
#                 if InteractionExtractor.is_bot_joined_voice_channel(iact):
#                     if InteractionExtractor.is_same_voice_channel(iact):
#                         await func(*args, **kwargs)
                        
#                     else:
#                         __m = await iact.response.send_message("봇과 같은 채널에 입장 후 명령어를 입력해주세요")
                        
#                         await __m.delete_original_message(delay=DEFAULT_DELAY)
                    
#                 else:
#                     __m = await iact.response.send_message("현재 봇이 입장한 채널이 존재하지 않습니다")
                    
#                     await __m.delete_original_message(delay=DEFAULT_DELAY)
            
#             return wrapper
#         return _decof
    
    
    
# class BorderCollieInspector:
#     @staticmethod
#     def coro_commanderInspection():
#         def _decof(func):
#             async def wrapper(*args, **kwargs):
#                 from Tools.Extractor.ctx_extractor import Context, ContextExtractor
#                 from Data.Cache.settings import DEFAULT_DELAY
                
#                 ctx: Context
                
#                 if "ctx" in kwargs.keys():
#                     ctx = kwargs.get("ctx")
#                 else:
#                     ctx = args[1]
                    
#                 if ContextExtractor.is_commander_joined_voice_channel(ctx):
#                     if ContextExtractor.is_bot_joined_voice_channel(ctx):
#                         if ContextExtractor.is_same_voice_channel(ctx):
#                             await func(*args, **kwargs)
                            
#                         else:
#                             __m = await ctx.send("봇과 같은 채널에 입장 후 명령어를 입력해주세요")
                            
#                             await __m.delete(delay=DEFAULT_DELAY)
                        
#                     else:
#                         __m = await ctx.send("현재 봇이 입장한 채널이 존재하지 않습니다")
                        
#                         await __m.delete(delay=DEFAULT_DELAY)

#                 else:
#                     __m = await ctx.send("채널에 입장 후 명령어를 입력해주세요")
                    
#                     await __m.delete(delay=DEFAULT_DELAY)
            
#             return wrapper
#         return _decof