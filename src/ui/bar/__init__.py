from gi.repository import Gtk, GtkLayerShell
import widget as Widget
from .workspaces import Workspaces
from .clients import Clients
from .clock import Clock
from .tray import Tray
from .kb_layout import KbLayout
from .launcher_button import LauncherButton
from .control_button import ControlButton

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
                            LauncherButton(self),
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
                            ControlButton(self)
                        ]
                    )
                ]
            )
        )
