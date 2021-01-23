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

_whitelist = os.environ["WHITELIST"]
WHITELIST = [int(i.strip()) for i in _whitelist.split(",")]
