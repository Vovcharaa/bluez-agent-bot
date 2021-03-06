import logging
import threading

import dbus
import dbus.service
from gi.repository import GLib

from .notify import Notify

AGENT_INTERFACE = "org.bluez.Agent1"
DEVICE_INTERFACE = "org.bluez.Device1"


class Device:
    def __init__(self, bus: dbus.SystemBus, device):
        self._device = dbus.Interface(
            bus.get_object("org.bluez", device), "org.freedesktop.DBus.Properties"
        )

    @property
    def trusted(self) -> bool:
        return self._device.Get(DEVICE_INTERFACE, "Trusted")

    @trusted.setter
    def trusted(self, trust: bool):
        self._device.Set(DEVICE_INTERFACE, "Trusted", trust)

    @property
    def alias(self) -> str:
        return self._device.Get(DEVICE_INTERFACE, "Alias")


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class Agent(dbus.service.Object):
    def __init__(
        self,
        bus: dbus.SystemBus,
        path: str = "/bot/agent",
        capability: str = "DisplayOnly",
    ):
        self._bus = bus
        self._path = path
        self._blocking_io = None
        self._mainloop = None
        self._capability = capability
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        super().__init__(self._bus, path)

    def start(self, blocking_io: Notify):
        self._blocking_io = blocking_io
        self._mainloop = GLib.MainLoop()
        manager = dbus.Interface(
            self._bus.get_object("org.bluez", "/org/bluez"), "org.bluez.AgentManager1"
        )
        manager.RegisterAgent(self._path, self._capability)
        self._logger.info("Agent registered")
        manager.RequestDefaultAgent(self._path)
        manager_thread = threading.Thread(target=self._mainloop.run)
        manager_thread.start()

    def stop(self):
        self._mainloop.quit()

    exit_on_release = True

    @property
    def set_exit_on_release(self):
        return self.exit_on_release

    @set_exit_on_release.setter
    def set_exit_on_release(self, exit_on_release):
        self.exit_on_release = exit_on_release

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        self._logger.info("Release")
        if self.exit_on_release:
            self._mainloop.quit()

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        device = Device(self._bus, device)
        print(f"AuthorizeService ({device.alias}, {uuid})")
        authorize = input("Authorize connection (yes/no): ")
        if authorize == "yes":
            return
        raise Rejected("Connection rejected by user")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        device = Device(self._bus, device)
        print(f"RequestPinCode {device.alias}")
        device.trusted = True
        return input("Enter PIN Code: ")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        device = Device(self._bus, device)
        print(f"RequestPasskey {device.alias}")
        device.trusted = True
        passkey = input("Enter passkey: ")
        return dbus.UInt32(passkey)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        device = Device(self._bus, device)
        self._logger.info(
            f"DisplayPasskey ({device.alias}, {passkey} entered {entered})"
        )

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        device = Device(self._bus, device)
        self._logger.info(f"DisplayPinCode {device.alias} {pincode}")

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, pin):
        device = Device(self._bus, device)
        confirm = self._blocking_io.confirm_message(device.alias)
        if confirm:
            device.trusted = True
            self._blocking_io.accepted(device.alias)
            return
        self._blocking_io.rejected(device.alias)
        raise Rejected("Passkey doesn't match")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        device = Device(self._bus, device)
        print(f"RequestAuthorization {device.alias}")
        auth = input("Authorize? (yes/no): ")
        if auth == "yes":
            return
        raise Rejected("Pairing rejected")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        self._logger.info("Cancel")
