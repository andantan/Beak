# -*- coding: utf-8 -*-


from Types import (
    Tuple,
    Dict,
    List
)

from Data.permission import Permission

class Beak:
    __T_module: Tuple[str] = (
        "__main__",
    )
    
    __slots__ = (
        
    )
    
    __commands__: Tuple[str] = (
        "beak_play",
        "beak_next",
        "beak_prev",
        "beak_pause",
        "beak_resume",
        "beak_stop",
        "beak_drop",
        "beak_exit",
        "beak_drop",
        "beak_shuffle",
        "beak_compell",
        "beak_swap",
        "beak_playlist",
        "beak_update_loop_mode",
    )
    
    
    __callable__: Tuple[str] = (
        "<coroutine-method integrated_allocation(self, ctx: Context) -> None>",
        "<method is_allocated(self, __SI: int) -> bool>",
        "<coroutine-method integrated_exhalation(self, __SI: int) -> None>",
        "<coroutine-method beak_play(self, ctx: Context, url: str) -> None>",
        "<coroutine-method beak_next(self, ctx: Context) -> None>",
        "<coroutine-method beak_prev(self, ctx: Context) -> None>",
        "<coroutine-method beak_pause(self, ctx: Context) -> None>",
        "<coroutine-method beak_resume(self, ctx: Context) -> None>",
        "<coroutine-method beak_stop(self, ctx: Context) -> None>",
        "<coroutine-method beak_drop(self, ctx: Context, _element: int) -> None>",
        "<coroutine-method beak_shuffle(self, ctx: Context) -> None>",
        "<coroutine-method beak_compell(self, ctx: Context, element: int) -> None>",
        "<coroutine-method beak_swap(self, ctx: Context, element: int, element_ano: int) -> None>",
        "<coroutine-method send_message(self, ctx: Context, message: str) -> None>",
        "<coroutine-emthod beak_exit(self, ctx: Context) -> None>",
        "<coroutine-method beak_playlist(self, ctx: Context) -> None>",
        "<coroutine-method beak_update_loop_mode(self, ctx: Context, mode: Optional[bool])>",
    )
           
    
    __decorater_callable__: Tuple[str] = (
        "<decorator @BeakInspector.coro_commanderInspection()>",
    )
    
    
    __throwable__: Tuple[str] = (
        
    )


    def __init__(self, __N_module: str, **kwargs) -> None:
        if __N_module in self.__T_module:
            Permission.allocate(**kwargs)
        else:
            raise 