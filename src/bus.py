import dbus
import dbus.mainloop.glib

from . import config
from .adapter import Adapter
from .agent import Agent


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

agent = Agent(bus)
adapter = Adapter(bus)
adapter.alias = config.ADAPTER_NAME
adapter.discoverable_timeout = config.DISCOVERABLE_TIMEOUT
