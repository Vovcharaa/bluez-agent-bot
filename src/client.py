import redis


cl = redis.Redis("localhost", 6379)
cl.config_set("notify-keyspace-events", "KEA")
sub = cl.pubsub()

response = input()


def get_event_key():
    sub.subscribe(f"__keyspace@0__:response{response}")
    for event in sub.listen():
        print(event)
        if event["data"] == b'set':
            return str(cl.get(f"response{response}"))


print(get_event_key())
