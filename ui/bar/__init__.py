from gi.repository import Gtk, GtkLayerShell
import widget as Widget
from .workspaces import Workspaces
from .clients import Clients
from .clock import Clock
from .tray import Tray
from .kblayout import KbLayout
from .launcherbutton import LauncherButton
from .controlbutton import ControlButton

def Bar(monitor):
    ret = Widget.LayerWindow(
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

    launcher_button = Widget.get_child_by_name(ret, "launcher-button")
    control_button = Widget.get_child_by_name(ret, "control-button")

    def on_launcher_button_clicked(*_):
        ret.get_application().toggle_window("Launcher")

    def on_control_button_clicked(*_):
        ret.get_application().toggle_window("Control-panel")

    launcher_button.connect("clicked", on_launcher_button_clicked)
    control_button.connect("clicked", on_control_button_clicked)

    return ret
