from typing import Tuple, Optional
from dataclasses import dataclass

from discord.ext.commands.context import Message

from Class.superclass import Block, Singleton


class Storage(Block.Instanctiating):
    class Message:
        __slots__ = (
            "message",
        )

        def __init__(self) -> None:
            self.message: Optional[Message] = None

        
        def is_saved(self) -> bool:
            return self.message is not None

        
        def clear(self) -> None:
            self.message = None


        def get_message(self) -> Optional[Message]:
            return self.message


        def set_message(self, message: Message) -> None:
            self.message = message
        


    class Identification(metaclass=Singleton):
        __slots__ = (
            "administrator_identifications",
            "beak_identification"
        )


        def __init__(self) -> None:
            self.administrator_identifications: Optional[Tuple[int]] = None
            self.beak_identification: Optional[Tuple[int]] = None

        
        def set_admin_ids(self, administrator_identifications: Tuple[int]) -> None:
            self.administrator_identifications = administrator_identifications


        def get_admin_ids(self) -> Tuple[int]:
            return self.administrator_identifications

        
        @property
        def is_admin(self, identification: int) -> bool: return identification in self.administrator_identifications

        
        def set_beak_id(self, beak_identification: int) -> None:
            if self.beak_identification is None:
                self.beak_identification = (beak_identification, )

            else:
                #TODO: Handling exception
                print("catched")
        
        def get_beak_id(self) -> int:
            return self.beak_identification.__getitem__(0)
