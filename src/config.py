import os

from dotenv import load_dotenv

load_dotenv()

allowed_updaters = ["webserver", "polling"]

TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_PORT = 8080
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
UPDATER_TYPE = os.getenv("UPDATER_TYPE", "polling")
if UPDATER_TYPE not in allowed_updaters:
    raise TypeError(
        f"No such updater.\n Available options: {', '.join(allowed_updaters)}"
    )

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB = int(os.getenv("REDIS_DB", 0))

_whitelist = os.environ["WHITELIST"]
WHITELIST = [int(i.strip()) for i in _whitelist.split(",")]

CURRENT_USER_KEY = "CURRENT_USER_KEY"

ADMIN = int(os.environ["ADMIN"])
