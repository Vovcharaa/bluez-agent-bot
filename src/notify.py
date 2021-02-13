import telegram

from . import menus, redis_client


class Notify:
    def __init__(self, bot: telegram.Bot):
        self._bot: telegram.Bot = bot

    def confirm_message(self, device_name: str) -> bool:
        user = redis_client.get_current_user()
        text, reply_markup = menus.approve(device_name)
        message = self._bot.send_message(
            chat_id=user, text=text, reply_markup=reply_markup
        )
        try:
            return redis_client.get_answer(user)
        except TimeoutError:
            text = menus.timeout()
            message.edit_text(text=text)
            return False

    def accepted(self, device_name: str):
        user = redis_client.get_current_user()
        text = menus.successful(device_name)
        self._bot.send_message(chat_id=user, text=text)

    def rejected(self, device_name: str):
        user = redis_client.get_current_user()
        text = menus.rejected(device_name)
        self._bot.send_message(chat_id=user, text=text)
