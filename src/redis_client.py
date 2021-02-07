import redis
from . import config


client = redis.Redis(
    config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB, config.REDIS_PASSWORD
)
client.config_set("notify-keyspace-events", "KEA")
sub = client.pubsub()


def get_answer(chat_id: int) -> bool:
    sub.subscribe(f"__keyspace@{config.REDIS_DB}__:response:{chat_id}")
    for event in sub.listen():
        if event["data"] == b"set":
            answer = client.get(f"response:{chat_id}")
            if answer:
                return bool(answer)
            else:
                return False
    return False


def set_answer(chat_id: int, answer: bool):
    return client.set(f"response:{chat_id}", int(answer))


def get_current_user() -> int:
    user = client.get(config.CURRENT_USER_KEY)
    if user:
        return int(user)
    else:
        return config.ADMIN
