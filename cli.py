import sys
from gi.repository import GLib, Gio

session_bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
application_proxy = Gio.DBusProxy.new_sync(
    session_bus,
    Gio.DBusProxyFlags.NONE,
    None,
    "com.github.btvtkh.Astel",
    "/com/github/btvtkh/Astel",
    "com.github.btvtkh.Astel.Application",
    None
)

def is_active():
    try:
        result = session_bus.call_sync(
            "org.freedesktop.DBus",
            "/org/freedesktop/DBus",
            "org.freedesktop.DBus",
            "NameHasOwner",
            GLib.Variant("(s)", ("com.github.btvtkh.Astel",)),
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None
        )

        return result.unpack()[0]
    except Exception as e:
        print(f"Error on checking dbus name: {e}")
        return False

def on_call_finish(obj, res):
    obj.call_finish(res)
    sys.exit()

def quit():
    try:
        application_proxy.call(
            "Quit",
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            on_call_finish
        )
    except Exception as e:
        print(f"Error on quit: {e}")

def toggle_window(window_name):
    try:
        application_proxy.call(
            "ToggleWindow",
            GLib.Variant("(s)", (window_name,)),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            on_call_finish
        )
    except Exception as e:
        print(f"Error on window toggle: {e}")

def main():
    if not is_active():
        print("No instance running.")
        sys.exit()

    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "-q":
                quit()
            case "-t":
                toggle_window(sys.argv[2])
    else:
        print("No arguments passed.")
        sys.exit()

main()
