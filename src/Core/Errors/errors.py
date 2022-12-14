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
                class BorderCollie:
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