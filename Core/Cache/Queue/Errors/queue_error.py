from typing import Any

from Class.superclass import Block


class AsyncQueueErrors(Block.Instanctiating):
    class QueueSaturatedErorr(Exception):
        """
The length of the queue has reached a threshold
    {
        class Queue:
            ...
            def enqueue(self, audios: List[Dict[str, str]]) -> None:
                for audio in audios:
                    if len(self.playlist) == QUEUE_THRESHOLD:
---------------------> raise AsyncQueueErrors.QueueSaturatedErorr(...)
    }
Raised QueueSaturatedErorr on Queue::enqueue(...)
        """

        def __init__(self, THRESHOLD: int, queue_length: int) -> None:
            message: str = f"The queue threshold has been reached\n"
            message += f"[ THRESHOLD: {THRESHOLD}, Queue length: {queue_length} ]"

            super().__init__(message)



    class OverQueueSaturatedErorr(Exception):
        """
The length of the queue has reached a threshold
    {
        class OverQueue:
            ...
            def enqueue(self, overplayed_audios: List[Dict[str, str]]) -> None:
                for overplayed_audio in overplayed_audios:
                    if len(self.overplayed_playlist) == OVER_QUEUE_THRESHOLD:
---------------------> raise AsyncQueueErrors.OverQueueSaturatedErorr(...)
    }
Raised QueueSaturatedErorr on OverQueue::enqueue(...)
        """

        def __init__(self, THRESHOLD: int, queue_length: int) -> None:
            message: str = f"The overplayed queue threshold has been reached\n"
            message += f"[ THRESHOLD: {THRESHOLD}, OverQueue length: {queue_length} ]"

            super().__init__(message)