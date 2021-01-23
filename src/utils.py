import logging
from functools import wraps

from telegram.ext import Updater

from . import config

logger = logging.getLogger(__name__)


def setup_updater(updater: Updater):
    updaters = {
        "webserver": setup_webserver,
        "polling": setup_polling
    }
    updaters[config.UPDATER_TYPE](updater)


def setup_webserver(updater: Updater):
    """
    Setups webserver and set telegram webhook on it
    Provide WEBHOOK_DOMAIN for this type of receiving updates
    """
    if config.WEBHOOK_DOMAIN:
        logger.info("Starting webserver for webhook")
        updater.start_webhook(
            listen="0.0.0.0", port=config.WEBHOOK_PORT, url_path=config.TOKEN
        )
        logger.debug("Setting webhook")
        updater.bot.set_webhook(f"{config.WEBHOOK_DOMAIN}/{config.TOKEN}")
    else:
        raise TypeError("WEBHOOK_DOMAIN env variable is not provided")


def setup_polling(updater: Updater):
    """
    Polling type of receiving updates
    """
    updater.start_polling()


def whitelist(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in config.WHITELIST:
            logger.warning(f"Unauthorized access denied for {user_id}.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped
