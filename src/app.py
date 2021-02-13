import atexit
import logging

import telegram
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater

from . import config, menus, redis_client, utils
from .bus import agent
from .notify import Notify


@utils.whitelist
def start(update: telegram.Update, context: CallbackContext):
    text = menus.start()
    update.message.reply_text(text, reply_markup=telegram.ReplyKeyboardRemove())


@utils.whitelist
def menu(update: telegram.Update, context: CallbackContext):
    text = menus.menu()
    update.message.reply_text(text, reply_markup=telegram.ReplyKeyboardRemove())


@utils.whitelist
def approve_action(update: telegram.Update, context: CallbackContext):
    query = update.callback_query
    callback = query.data.split("_")
    query.answer(text="")
    if callback[1] == "yes":
        redis_client.set_answer(update.effective_user.id, True)
    else:
        redis_client.set_answer(update.effective_user.id, False)
    text = menus.answered()
    query.edit_message_text(text=text)


@utils.whitelist
def bluetooth(update: telegram.Update, context: CallbackContext):
    if context.args and context.args[0] == "off":
        text = menus.bluetooth_off()
    else:
        text = menus.bluetooth_on()
    update.message.reply_text(text)


@utils.whitelist
def discoverable(update: telegram.Update, context: CallbackContext):
    if context.args and context.args[0] == "off":
        text = menus.discoverable_off()
    else:
        text = menus.discoverable_on(update.effective_user.id)
    update.message.reply_text(text)


@utils.whitelist
def status(update: telegram.Update, context: CallbackContext):
    text = menus.get_status()
    update.message.reply_text(text)


@utils.whitelist
def error_handler(update: telegram.Update, context: CallbackContext):
    text = "Something went wrong"
    if update.callback_query:
        query = update.callback_query
        query.edit_message_text(text=text, parse_mode="MarkdownV2")
    else:
        update.message.reply_text(text)


def run():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    updater = Updater(token=config.TOKEN)
    utils.setup_updater(updater)
    updater.dispatcher.add_error_handler(error_handler)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("menu", menu))
    updater.dispatcher.add_handler(CommandHandler("bluetooth", bluetooth))
    updater.dispatcher.add_handler(CommandHandler("discoverable", discoverable))
    updater.dispatcher.add_handler(CommandHandler("status", status))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(approve_action, pattern="approve\\_*")
    )
    updater.bot.set_my_commands(
        [
            ("start", "Open menu with commands"),
            ("menu", "Open menu with commands"),
            ("status", "Get status of interface"),
            ("discoverable", "[off] - Toggle discoverable"),
            ("bluetooth", "[off] - Enable or Disable bluetooth"),
        ]
    )
    user = updater.bot.get_me()
    notifier = Notify(updater.bot)
    agent.start(notifier)
    atexit.register(agent.stop)
    logger.info(f"Started bot {user['first_name']} at https://t.me/{user['username']}")
    updater.idle()
