from typing import Tuple

import telegram

# from telegram.utils.helpers import escape_markdown


def menu() -> str:
    text = (
        "List of available commands:\n"
        "/bluetooth {off, on} - enable or disable bluetooth\n"
        "/discoverable - Toggle discoverable\n"
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


def enable_bluetooth() -> Tuple[str, telegram.InlineKeyboardMarkup]:
    text = "Do you want to enable bluetooth?"
    reply_markup = telegram.InlineKeyboardMarkup(
        [
            [
                telegram.InlineKeyboardButton(
                    "✅Yes",
                    callback_data="bluetooth_yes",
                ),
                telegram.InlineKeyboardButton(
                    "❌No",
                    callback_data="bluetooth_no",
                ),
            ]
        ]
    )
    return text, reply_markup


def answered() -> str:
    text = "Processing"
    return text


def successful() -> str:
    text = "Successful!"
    return text
