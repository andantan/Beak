from typing import Dict

from Class.superclass import Singleton

from Core.Cache.player import Player


class PlayerPool(metaclass=Singleton):
    def __init__(self) -> None:
        self.player_pool: Dict[int, Player] = dict()


    def __contains__(self, guild_id: int) -> bool:
        return guild_id in self.player_pool

    
    def __setitem__(self, guild_id: int, player: Player) -> None:
        self.player_pool.__setitem__(guild_id, player)


    def __getitem__(self, guild_id: int) -> Player:
        return self.player_pool.__getitem__(guild_id)


    def __delitem__(self, guild_id: int) -> None:
        self.player_pool.__delitem__(guild_id)


    def set(self, guild_id: int, player: Player) -> None:
        self.__setitem__(guild_id=guild_id, player=player)


    def get(self, guild_id: int) -> Player:
        return self.__getitem__(guild_id=guild_id)

    
    def get_guild_player(self, guild_id: int) -> Player:
        return self.__getitem__(guild_id=guild_id)


    def reference_players(self) -> Dict[int, Player]:
        return self.player_pool 
    
    