import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

class IpcService(dbus.service.Object):
    def __init__(self, app):
        self._app = app
        DBusGMainLoop(set_as_default = True)

        bus_name = dbus.service.BusName(
            "com.github.btvtkh.AstelShell",
            bus = dbus.SessionBus()
        )

        super().__init__(
            bus_name,
            "/com/github/btvtkh/AstelShell"
        )

    @dbus.service.method(
        "com.github.btvtkh.AstelShell.Application",
        in_signature = "s"
    )
    def ToggleWindow(self, name):
        self._app.toggle_window(name)
