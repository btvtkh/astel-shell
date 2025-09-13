import gi
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version('GtkLayerShell', '0.1')
gi.require_version("AstalHyprland", "0.1")
gi.require_version("AstalNotifd", "0.1")
gi.require_version("AstalTray", "0.1")
gi.require_version("AstalWp", "0.1")

import os
import subprocess
from gi.repository import GLib, Gdk
from application import Application
from ui.bar import Bar
from ui.notifications import Notifications
from ui.launcher import Launcher
from ui.powermenu import Powermenu
from ui.control_panel import ControlPanel

class ShellApp(Application):
    def do_activate(self):
        self.hold()

        scss = os.path.expanduser("~/.config/astel-shell/style/index.scss")
        css = "/tmp/style.css"
        subprocess.run(["sass", scss, css])
        self.apply_css(css, False)

        display = Gdk.Display.get_default()
        for i in range(display.get_n_monitors()):
            monitor = display.get_monitor(i)
            self.add_window(Bar(monitor))

        self.add_window(Notifications())

        launcher = Launcher()
        powermenu = Powermenu()
        control_panel = ControlPanel()

        def on_launcher_visible(*_):
            if launcher.get_visible():
                powermenu.hide()

        def on_control_panel_visible(*_):
            if control_panel.get_visible():
                powermenu.hide()

        def on_powermenu_visible(*_):
            if powermenu.get_visible():
                launcher.hide()
                control_panel.hide()

        launcher.connect("notify::visible", on_launcher_visible)
        control_panel.connect("notify::visible", on_control_panel_visible)
        powermenu.connect("notify::visible", on_powermenu_visible)

        self.add_window(launcher)
        self.add_window(control_panel)
        self.add_window(powermenu)

if __name__ == "__main__":
    shell_app = ShellApp()
    GLib.set_prgname("Astel-Shell")
    try:
        shell_app.run()
    except KeyboardInterrupt:
        shell_app.quit()
