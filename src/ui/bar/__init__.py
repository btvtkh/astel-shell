from gi.repository import Gtk, GtkLayerShell
import widgets as Widgets
from .workspaces import WorkspacesWidget
from .clients import ClientsWidget
from .date_time import DateTimeWidget
from .tray import TrayWidget
from .kb_layout import KbLayoutWidget
from .launcher_button import LauncherButtonWidget

class Bar(Widgets.Window):
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
            child = Widgets.Box(
                name = "main-box",
                children = [
                    Widgets.Box(
                        hexpand = True,
                        children = [
                            LauncherButtonWidget(self),
                            WorkspacesWidget(),
                            ClientsWidget()
                        ]
                    ),
                    Widgets.Box(
                        halign = Gtk.Align.END,
                        children = [
                            TrayWidget(),
                            KbLayoutWidget(),
                            DateTimeWidget()
                        ]
                    )
                ]
            )
        )
