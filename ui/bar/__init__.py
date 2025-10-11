from gi.repository import Gtk, GtkLayerShell
import widget as Widget
from .workspaces import Workspaces
from .clients import Clients
from .clock import Clock
from .tray import Tray
from .kblayout import KbLayout
from .launcherbutton import LauncherButton
from .controlbutton import ControlButton

class Bar(Widget.LayerWindow):
    def __init__(self, monitor):
        super().__init__(
            name = "Bar",
            namespace = "Astel-Bar",
            monitor = monitor,
            auto_exclusive_zone = True,
            layer = GtkLayerShell.Layer.TOP,
            anchors = [
                GtkLayerShell.Edge.BOTTOM,
                GtkLayerShell.Edge.LEFT,
                GtkLayerShell.Edge.RIGHT
            ],
            visible = True,
            child = Widget.Box(
                css_classes = ["main-box"],
                children = [
                    Widget.Box(
                        hexpand = True,
                        children = [
                            LauncherButton(),
                            Workspaces(),
                            Clients()
                        ]
                    ),
                    Widget.Box(
                        halign = Gtk.Align.END,
                        children = [
                            Tray(),
                            KbLayout(),
                            Clock(),
                            ControlButton()
                        ]
                    )
                ]
            )
        )

        launcher_button = Widget.get_child_by_name(self, "launcher-button")
        control_button = Widget.get_child_by_name(self, "control-button")

        def on_launcher_button_clicked(*_):
            self.get_application().toggle_window("Launcher")

        def on_control_button_clicked(*_):
            self.get_application().toggle_window("Control-panel")

        launcher_button.connect("clicked", on_launcher_button_clicked)
        control_button.connect("clicked", on_control_button_clicked)
