from typing import Tuple

import telegram
from telegram.utils.helpers import escape_markdown

from . import config, utils


def menu() -> str:
    text = (
        "List of available commands:\n"
        "/torrents - List all torrents\n"
        "/memory - Available memory\n"
        "/add - Add torrent"
    )
    return text


def add_torrent() -> str:
    text = "Just send torrent file or magnet url to the bot"
    return text

def started_menu(torrent_id: str) -> Tuple[str, telegram.InlineKeyboardMarkup]:

    return text, reply_markup
