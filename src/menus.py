from typing import Tuple

import telegram

from .bus import adapter
from .redis_client import set_current_user, delete_current_user


def menu() -> str:
    text = (
        "List of available commands:\n"
        "/bluetooth [off] - Enable or Disable bluetooth\n"
        "/discoverable [off] - Toggle discoverable\n"
        "/status - Get status of interface"
    )
    return text


def bluetooth_on() -> str:
    adapter.powered = True
    text = "Bluetooth enabled"
    return text


def bluetooth_off() -> str:
    adapter.powered = False
    text = "Bluetooth disabled"
    return text


def discoverable_on(chat_id: int) -> str:
    set_current_user(chat_id)
    adapter.discoverable = True
    text = "Discoverable enabled"
    return text


def discoverable_off() -> str:
    adapter.discoverable = False
    delete_current_user()
    text = "Discoverable disabled"
    return text


def get_status() -> str:
    text = (
        "Device status:\n"
        f"Name: {adapter.alias}\n"
        f"Powered: {bool(adapter.powered)}\n"
        f"Discoverable: {bool(adapter.discoverable)}\n"
        f"Discoverable timeout: {adapter.discoverable_timeout} sec"
    )
    return text


def approve(name: str) -> Tuple[str, telegram.InlineKeyboardMarkup]:
    text = f"Do you want to approve connection from {name}?"
    reply_markup = telegram.InlineKeyboardMarkup(
        [
            [
                telegram.InlineKeyboardButton(
                    "✅Yes",
                    callback_data="approve_yes",
                ),
                telegram.InlineKeyboardButton(
                    "❌No",
                    callback_data="approve_no",
                ),
            ]
        ]
    )
    return text, reply_markup


def start() -> str:
    text = "Bluez telegram client"
    return text


def answered() -> str:
    text = "Processing"
    return text


def successful(device) -> str:
    adapter.discoverable = False
    delete_current_user()
    text = f"{device} connected successfully!"
    return text


def rejected(device) -> str:
    text = f"{device} rejected!"
    return text


def timeout() -> str:
    text = "Timeout"
    return text
