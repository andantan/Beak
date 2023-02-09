import os

from typing import Dict


PATH: Dict[str, str] = {
    "configuration_json_path": os.path.join(os.getcwd(), "Admin", "Data", "configuration.json"),
    "administrator_json_path": os.path.join(os.getcwd(), "Admin", "Data", "administrator.json"),
    # deprecated 2023-01-07
    # "user_json_path": os.path.join(os.getcwd(), "Admin", "Data", "user.json"),
}


YTDL_OPTION: Dict[str, str] = {
    'outtmpl': '%(title)s.%(uploader)s',
    "format": "bestaudio/best"
}

FFMPEG_OPTION = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}


DEFAULT_DELAY = 15
SLEEP_TIME = 2

NOTICE_EMBED_COLOR = 0xfb1313
COMMANDER_NOTICE_EMBED_COLOR = 0x6cfe90
PLAYLIST_NOTICE_EMBED_COLOR = 0x91eede
ATTACHED_PLAYLIST_EMBED_COLOR = 0x0cc0ed
ENDED_PLAYLIST_NOTICE_COLOR = 0xff0000

QUEUE_THRESHOLD = 200
OVER_QUEUE_THRESHOLD = 300

SELECT_MENU_THRESHOLD = 20
