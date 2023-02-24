from typing import (
    List, Dict, Tuple,
    Optional
)

from dataclasses import dataclass

import random

from discord import (
    VoiceClient, 
    Guild, 
    VoiceChannel,
    Member
)

from discord.ext.commands.context import Message

from Core.Cache.storage import Storage
from Core.Cache.Queue.queue import AsyncQueue
from Core.Cache.Queue.Errors.queue_error import AsyncQueueErrors

# deprecated 2023-01-10
# from Core.Cache.Errors.status_error import PlayerErrors


@dataclass
class Player:
    VOICECLIENT: VoiceClient
    MESSAGESTORAGE: Storage.Message
    QUEUE: AsyncQueue.Queue
    OVERQUEUE: AsyncQueue.OverQueue

    # mode == 0: Normal mode
    # mode == 1: Loop mode
    # mode == 2: Repeat mode
    LOOP_MODE: int
        

    def __init__(self, voice_client: VoiceClient, message_storage: Storage.Message,
            queue: AsyncQueue.Queue, over_queue: AsyncQueue.OverQueue) -> None:
        self.VOICECLIENT = voice_client
        self.MESSAGESTORAGE = message_storage
        self.QUEUE = queue
        self.OVERQUEUE = over_queue
        self.LOOP_MODE = 0


    @property
    def queue(self) -> AsyncQueue.Queue: return self.QUEUE
    @property
    def over_queue(self) -> AsyncQueue.OverQueue: return self.OVERQUEUE
    @property
    def message_storage(self) -> Storage.Message: return self.MESSAGESTORAGE
    @property
    def voice_client(self) -> VoiceClient: return self.VOICECLIENT
    @property
    def voice_client_guild(self) -> Guild: return self.VOICECLIENT.guild
    @property
    def voice_client_channel(self) -> VoiceChannel: return self.VOICECLIENT.channel
    @property
    def voice_channel_members(self) -> List[Member]: return self.VOICECLIENT.channel.members
    @property
    def is_voice_channel_empty(self) -> bool: return len(self.VOICECLIENT.channel.members) == 1
    @property
    def server_name(self) -> str: return self.VOICECLIENT.guild.name
    @property
    def channel_name(self) -> str: return self.VOICECLIENT.channel.name
    @property
    def channel_id(self) -> int: return self.VOICECLIENT.channel.id
    @property
    def ip_address(self) -> str: return self.VOICECLIENT.ip
    @property
    def is_connected(self) -> bool: return self.VOICECLIENT.is_connected()
    @property
    def is_activated(self) -> bool: return self.VOICECLIENT.is_connected() and self.VOICECLIENT.is_playing()
    @property
    def is_queued(self) -> bool: return self.VOICECLIENT.is_paused() or self.VOICECLIENT.is_playing()
    @property
    def is_first_audio(self) -> bool: return self.OVERQUEUE.is_empty()
    @property
    def is_last_audio(self) -> bool: return self.QUEUE.is_single()
    @property
    def is_queue_single(self) -> bool: return self.QUEUE.is_single()
    @property
    def is_overqueue_single(self) -> bool: return self.OVERQUEUE.is_single()
    @property
    def is_queue_two_or_more(self) -> bool: return self.QUEUE.is_two_or_more()
    @property
    def is_overqueue_two_or_more(self) -> bool: return self.OVERQUEUE.is_two_or_more()
    @property
    def is_queue_two_or_less(self) -> bool: return self.QUEUE.is_two_or_less()
    @property
    def is_overqueue_two_or_less(self) -> bool: return self.OVERQUEUE.is_two_or_less()
    @property
    def is_playing(self) -> Optional[bool]: return self.VOICECLIENT.is_playing()
    @property
    def is_paused(self) -> Optional[bool]: return self.VOICECLIENT.is_paused()
    @property
    def is_ended(self) -> Optional[bool]: return self.VOICECLIENT.is_connected() and self.QUEUE.is_empty()
    @property
    def is_queue_empty(self) -> bool: return self.QUEUE.is_empty()
    @property
    def is_overqueue_empty(self) -> bool: return self.OVERQUEUE.is_empty()
    @property
    def seek_queue(self) -> Optional[Dict[str, str]]: return self.QUEUE.seek()
    @property
    def seek_overqueue(self) -> Optional[Dict[str, str]]: return self.OVERQUEUE.seek()
    @property
    def seek_next_queue(self) -> Optional[Dict[str, str]]: return self.QUEUE.reference().__getitem__(1)
    @property
    def reference_queue(self) -> Tuple[Dict[str, str]]: return self.QUEUE.reference()
    @property
    def reference_overqueue(self) -> Tuple[Dict[str, str]]: return self.OVERQUEUE.reference()
    @property
    def queue_length(self) -> int: return self.QUEUE.get_length()
    @property
    def overqueue_length(self) -> int: return self.OVERQUEUE.get_length()
    @property
    def loop_mode(self) -> int: return self.LOOP_MODE
    @property
    def is_normal_mode(self) -> bool: return self.LOOP_MODE == 0
    @property
    def is_loop_mode(self) -> bool: return self.LOOP_MODE == 1 
    @property
    def is_repeat_mode(self) -> bool: return self.LOOP_MODE == 2
    @property
    def message(self) -> Optional[Message]: return self.MESSAGESTORAGE.get_message()
    @message.setter
    def message(self, message: Message) -> None: self.MESSAGESTORAGE.set_message(message=message)
    @property
    def guild_id(self) -> int: return self.MESSAGESTORAGE.get_guild_id()
    @property
    def channel_id(self) -> Optional[int]: return self.MESSAGESTORAGE.get_channel_id()
    @channel_id.setter
    def channel_id(self, channel_id: int) -> None: self.MESSAGESTORAGE.set_channel_id(channel_id=channel_id)
    @property
    def is_message_saved(self) -> bool: return self.MESSAGESTORAGE.is_message_saved()
    @property
    def is_channel_id_saved(self) -> bool: return self.MESSAGESTORAGE.is_channel_id_saved()


    def enqueue(self, audios: List[Dict[str, str]]) -> None:
        try:
            self.QUEUE.enqueue(audios)
        
        except AsyncQueueErrors.QueueSaturatedErorr as throwable:
            raise throwable


    def dequeue(self) -> None:
        try:
            played_audio = self.QUEUE.dequeue()

            if played_audio.get("title") is not None:
                self.OVERQUEUE.enqueue([played_audio])
        
        except AsyncQueueErrors.OverQueueSaturatedErorr as throwable:
            raise throwable


    def stop(self) -> None:
        self.VOICECLIENT.stop()


    def prev(self, forced: bool=False) -> None:
        DUMMY = { "title": None }

        self.QUEUE.insert(0, self.OVERQUEUE.pop())
        self.QUEUE.insert(0, DUMMY)

        if forced:
            self.dequeue()

        self.VOICECLIENT.stop()


    def skip(self, forced: bool=False) -> None:
        if forced:
            self.dequeue()

        self.VOICECLIENT.stop()

    def forced_play(self, value: int, forced: bool=False) -> Dict[str, str]:
        if value > self.queue_length:
            raise ValueError

        selected_audio = self.QUEUE.pop(index=value)

        self.QUEUE.insert(index=1, audio=selected_audio)

        if forced:
            self.dequeue()

        self.VOICECLIENT.stop()

        return selected_audio


    def forced_prev(self, value: int, forced: bool=False) -> Dict[str, str]:
        if value > self.overqueue_length:
            raise ValueError

        selected_audio = self.OVERQUEUE.pop(index=value)

        self.QUEUE.insert(index=1, audio=selected_audio)

        if forced:
            self.dequeue()

        self.VOICECLIENT.stop()

        return selected_audio

    
    def pause(self) -> None:
        self.VOICECLIENT.pause()


    def resume(self) -> None:
        self.VOICECLIENT.resume()


    def change_loop_mode(self) -> None:
        self.LOOP_MODE = (self.LOOP_MODE + 1) % 3


    def looping(self) -> None:
        overplayed_queue = list(self.OVERQUEUE.reference())
        self.QUEUE.enqueue(overplayed_queue)

        self.OVERQUEUE.clear()


    def shuffle(self) -> None:
        play_queue = self.QUEUE.reference()[1:]
        overplayed_queue = self.OVERQUEUE.reference()

        self.QUEUE.clear()
        self.OVERQUEUE.clear()

        attached_queue = list(play_queue + overplayed_queue)

        random.shuffle(attached_queue)

        try:
            self.QUEUE.enqueue(attached_queue)
        
        except AsyncQueueErrors.QueueSaturatedErorr as throwable:
            raise throwable

    
    def remove(self) -> None:
        try:
            self.QUEUE.remove()
        
        except IndexError as throwable:
            raise throwable


    def reset(self) -> None:
        self.QUEUE.clear()
        self.OVERQUEUE.clear()


