import logging

import telegram
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater

from . import config, menus, redis_client, utils
from .agent import Agent
from .notify import Notify


@utils.whitelist
def start(update: telegram.Update, context: CallbackContext):
    text = menus.menu()
    update.message.reply_text(text, reply_markup=telegram.ReplyKeyboardRemove())


# @utils.whitelist
# def started_menu_command(update: telegram.Update, context: CallbackContext):
#     torrent_list, keyboard = menus.started_menu("adf")
#     update.message.reply_text(
#         torrent_list, reply_markup=keyboard, parse_mode="MarkdownV2"
#     )


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
    updater.dispatcher.add_handler(CommandHandler("menu", start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(approve_action, pattern="approve\\_*")
    )
    updater.bot.set_my_commands(
        [("start", "Open menu with commands"), ("menu", "Open menu with commands")]
    )
    user = updater.bot.get_me()
    notifier = Notify(updater.bot)
    agent = Agent(notifier)
    agent.start()
    logger.info(f"Started bot {user['first_name']} at https://t.me/{user['username']}")
    updater.idle()
