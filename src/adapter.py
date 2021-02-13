import dbus

ADAPTER_INTERFACE = "org.bluez.Adapter1"


class Adapter:
    def __init__(self, bus: dbus.SystemBus, adapter_name: str = "hci0"):
        self._dbus = bus
        self._adapter = dbus.Interface(
            self._dbus.get_object("org.bluez", f"/org/bluez/{adapter_name}"),
            "org.freedesktop.DBus.Properties",
        )

    @property
    def alias(self) -> str:
        return self._adapter.Get(ADAPTER_INTERFACE, "Alias")

    @alias.setter
    def alias(self, value: str):
        self._adapter.Set(ADAPTER_INTERFACE, "Alias", dbus.String(value))

    @property
    def powered(self) -> bool:
        return self._adapter.Get(ADAPTER_INTERFACE, "Powered")

    @powered.setter
    def powered(self, value: bool):
        self._adapter.Set(ADAPTER_INTERFACE, "Powered", value)

    @property
    def discoverable(self) -> bool:
        return self._adapter.Get(ADAPTER_INTERFACE, "Discoverable")

    @discoverable.setter
    def discoverable(self, value: bool):
        self._adapter.Set(ADAPTER_INTERFACE, "Discoverable", value)

    @property
    def discoverable_timeout(self) -> int:
        return self._adapter.Get(ADAPTER_INTERFACE, "DiscoverableTimeout")

    @discoverable_timeout.setter
    def discoverable_timeout(self, value: int):
        self._adapter.Set(ADAPTER_INTERFACE, "DiscoverableTimeout", dbus.UInt32(value))
