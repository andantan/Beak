from typing import (
    Tuple, Dict
)

PREFIX: Tuple[str] = ("#", "/>")

FFMPEG_OPTION: Dict[str] = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}

YTDL_OPTION: Dict[str] = {
    'outtmpl': '%(title)s.%(uploader)s',
    "format": "bestaudio/best"
}


PREFIX_QUEUE_MAX_LENGTHL: int = 50
POSTFIX_QUEUE_MAX_LENGTH: int = 50
THRESHOLD: int = 1
REQUESTS_SC: int = 403
DEFAULT_DELAY: int = 5