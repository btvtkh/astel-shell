from gi.repository import Gtk
import widget as Widget
from .notificationlist import NotificationList
from .audiosliders import AudioSliders
from .wifibutton import WifiQSB
from .bluetoothbutton import BluetoothQSB

class MainPage(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "main-page",
            orientation = Gtk.Orientation.VERTICAL,
            children = [
                NotificationList(),
                Widget.Separator(),
                AudioSliders(),
                Widget.Box(
                    css_classes = ["qsb-box"],
                    homogeneous = True,
                    children = [
                        WifiQSB(),
                        BluetoothQSB()
                    ]
                )
            ]
        )
