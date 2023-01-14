from typing import Any

from Class.superclass import Block


class PlayerErrors(Block.Instanctiating):
    class TypeError(Exception):
        '''
Unvalid type has detected as a parameter
    {
        @dataclass
        class PL_status:
            ...
            @property
            def %property%(self) -> bool:
                return self.FM


            @%property%.setter
            def %property%(self, %argument%: T) -> None:
                if isinstance(%argument%, T):
                    self.%property% = %argument%
                ...

                else
------------------> raise PlStatusErrors.TypeError(...)
        }
    }
Raised TypeError on PL_status::%property%.setter(...)
        '''

        def __init__(self, types: type, arg_type: type, arg_value: Any) -> None:
            message: str = f"Only {types} types are allowed, but {arg_type}: ({arg_value}) types were detected."
            
            super().__init__(message)

    

    class NoneTypeError(Exception):
        '''
NoneType has detected as a parameter
    {
        @dataclass
        class PL_status:
            ...
            @property
            def %property%(self) -> bool:
                return self.FM


            @%property%.setter
            def %property%(self, %argument%: T) -> None:
                if isinstance(%argument%, T):
                    self.%property% = %argument%

                elif isinstance(updated_FM, type(None)):
------------------> raise PlStatusErrors.NoneTypeError

                ...
        }
    }
Raised TypeError on PL_status::%property%.setter(...)
        '''

        def __init__(self, types: type) -> None:
            message: str = f"Only {types} types are allowed, but NoneType was detected."
            
            super().__init__(*message)