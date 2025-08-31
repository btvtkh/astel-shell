import gi
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version('GtkLayerShell', '0.1')
gi.require_version("AstalHyprland", "0.1")
gi.require_version("AstalNotifd", "0.1")
gi.require_version("AstalTray", "0.1")

from gi.repository import GLib
from app import ShellApp

if __name__ == "__main__":
    app = ShellApp()
    GLib.set_prgname("Astel-Shell")
    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()
