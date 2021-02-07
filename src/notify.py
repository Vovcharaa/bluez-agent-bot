import telegram

from . import menus, redis_client


class Notify:
    def __init__(self, bot: telegram.Bot):
        self._bot: telegram.Bot = bot

    def confirm_message(self, device_name: str) -> bool:
        text, reply_markup = menus.approve(device_name)
        user = redis_client.get_current_user()
        self._bot.send_message(chat_id=user, text=text, reply_markup=reply_markup)
        return redis_client.get_answer(user)

    def accepted(self):
        text = menus.successful()
        user = redis_client.get_current_user()
        self._bot.send_message(chat_id=user, text=text)

    def rejected(self):
        text = menus.rejected()
        user = redis_client.get_current_user()
        self._bot.send_message(chat_id=user, text=text)
