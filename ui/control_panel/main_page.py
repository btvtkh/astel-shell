from gi.repository import Gtk
import widget as Widget
from .notification_list import NotificationList
from .audio_sliders import AudioSliders
from .wifi_button import WifiQSB
from .bluetooth_button import BluetoothQSB

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
