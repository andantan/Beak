from typing import (
    List, Dict, Tuple,
    Optional
)

import random

from Core.Cache.Queue.Errors.queue_error import AsyncQueueErrors

from Class.superclass import Block

from Data.Paraments.settings import QUEUE_THRESHOLD, OVER_QUEUE_THRESHOLD



class AsyncQueue(Block.Instanctiating):
    class OverQueue:
        __slots__ = (
            "overplayed_playlist"
        )


        def __init__(self) -> None:
            self.overplayed_playlist: List[Dict[str, str]] = list()


        def enqueue(self, overplayed_audios: List[Dict[str, str]]) -> None:
            for overplayed_audio in overplayed_audios:
                if len(self.overplayed_playlist) == OVER_QUEUE_THRESHOLD:
                    raise AsyncQueueErrors.OverQueueSaturatedErorr(
                        THRESHOLD = OVER_QUEUE_THRESHOLD,
                        queue_length = len(self.overplayed_playlist)
                    )

                self.overplayed_playlist.append(overplayed_audio)


        def dequeue(self) -> Dict[str, str]:
            self.overplayed_playlist.pop(0)

        
        def pop(self, index: int=-1) -> Dict[str, str]:
            return self.overplayed_playlist.pop(index)


        def insert(self, index: int, audio: Dict[str, str]) -> None:
            self.overplayed_playlist.insert(index, audio)

        
        def clear(self) -> None:
            if not self.is_empty():
                self.overplayed_playlist = list()

            
        def remove(self, index: int=1) -> None:
            try:
                self.overplayed_playlist.pop(index)
            
            except IndexError as throwable:
                raise throwable


        def seek(self, index: int=-1) -> Optional[Dict[str, str]]:
            if self.is_empty():
                return None

            return self.overplayed_playlist.__getitem__(index)


        def reference(self) -> Tuple[Dict[str, str]]:
            return tuple(self.overplayed_playlist)


        def get_length(self) -> int:
            return len(self.overplayed_playlist)


        def is_empty(self) -> bool:
            return not bool(self.overplayed_playlist)


        def is_single(self) -> bool:
            return len(self.overplayed_playlist) == 1

        
        def is_two_or_more(self) -> bool:
            return len(self.overplayed_playlist) >= 2

        def is_two_or_less(self) -> bool:
            return len(self.overplayed_playlist) <= 2


    
    class Queue:
        __slots__ = (
            "playlist"
        )


        def __init__(self) -> None:
            self.playlist: List[Dict[str, str]] = list()


        def enqueue(self, audios: List[Dict[str, str]]) -> None:
            for audio in audios:
                if len(self.playlist) == QUEUE_THRESHOLD:
                    raise AsyncQueueErrors.QueueSaturatedErorr(
                        THRESHOLD = QUEUE_THRESHOLD,
                        queue_length = len(self.playlist)
                    )

                self.playlist.append(audio)


        def dequeue(self) -> Dict[str, str]:
            return self.playlist.pop(0)

    
        def pop(self, index: int=-1) -> Dict[str, str]:
            return self.playlist.pop(index)


        def insert(self, index: int, audio: Dict[str, str]) -> None:
            self.playlist.insert(index, audio)


        def clear(self, on_air: bool=True) -> None:
            if not self.is_empty():
                if on_air:
                    self.playlist = self.playlist[:1]
                else:
                    self.playlist = list()


        def remove(self, index: int=1) -> None:
            try:
                self.playlist.pop(index)
            
            except IndexError as throwable:
                raise throwable


        def seek(self, index: int=0) -> Optional[Dict[str, str]]:
            if self.is_empty():
                return None

            return self.playlist.__getitem__(index)


        def reference(self) -> Tuple[Dict[str, str]]:
            return tuple(self.playlist)


        def get_length(self) -> int:
            return len(self.playlist)

        
        def is_empty(self) -> bool:
            return not bool(self.playlist)


        def is_single(self) -> bool:
            return len(self.playlist) == 1

        
        def is_two_or_more(self) -> bool:
            return len(self.playlist) >= 2


        def is_two_or_less(self) -> bool:
            return len(self.playlist) <= 2
    

        def shuffle(self) -> None:
            now_playing = self.dequeue()

            random.shuffle(self.playlist)

            self.playlist.insert(0, now_playing)
