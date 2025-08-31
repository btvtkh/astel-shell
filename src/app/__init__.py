import os
import subprocess
from gi.repository import Gdk
from .application import Application
from ui.bar import Bar
from ui.notifications import Notifications
from ui.launcher import Launcher
from ui.powermenu import Powermenu

class App(Application):
    def do_activate(self):
        self.hold()

        scss = os.path.expanduser("~/.config/astel-shell/index.scss")
        css = "/tmp/style.css"
        subprocess.run(["sass", scss, css])
        self.apply_css(css, False)

        display = Gdk.Display.get_default()
        for i in range(display.get_n_monitors()):
            self.add_window(Bar(display.get_monitor(i)))

        self.add_window(Notifications())

        launcher = Launcher()
        powermenu = Powermenu()

        def on_launcher_visible(*_):
            if launcher.get_visible():
                powermenu.hide()

        def on_powermenu_visible(*_):
            if powermenu.get_visible():
                launcher.hide()

        launcher.connect("notify::visible", on_launcher_visible)
        powermenu.connect("notify::visible", on_powermenu_visible)

        self.add_window(launcher)
        self.add_window(powermenu)
