import redis

from . import config

client = redis.Redis(
    config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB, config.REDIS_PASSWORD
)
client.config_set("notify-keyspace-events", "KEA")
sub = client.pubsub()


def get_answer(chat_id: int) -> bool:
    client.set(f"response:{chat_id}:timeout", config.TIMEOUT, config.TIMEOUT)
    sub.psubscribe(f"__keyspace@{config.REDIS_DB}__:response:{chat_id}*")
    for event in sub.listen():
        if event["data"] == b"set":
            sub.punsubscribe(f"__keyspace@{config.REDIS_DB}__:response:{chat_id}*")
            answer = client.get(f"response:{chat_id}")
            client.delete(f"response:{chat_id}", f"response:{chat_id}:timeout")
            if answer == b"1":
                return True
            else:
                return False
        elif event["data"] == b"expired":
            sub.punsubscribe(f"__keyspace@{config.REDIS_DB}__:response:{chat_id}*")
            client.delete(f"response:{chat_id}", f"response:{chat_id}:timeout")
            raise TimeoutError
    sub.punsubscribe(f"__keyspace@{config.REDIS_DB}__:response:{chat_id}*")
    return False


def set_answer(chat_id: str, answer: bool):
    return client.set(f"response:{chat_id}", int(answer))


def get_current_user() -> int:
    user = client.get(config.CURRENT_USER_KEY)
    if user:
        return int(user)
    else:
        return config.ADMIN


def set_current_user(chat_id: int):
    return client.set(config.CURRENT_USER_KEY, chat_id, config.DISCOVERABLE_TIMEOUT)


def delete_current_user():
    return client.delete(config.CURRENT_USER_KEY)
