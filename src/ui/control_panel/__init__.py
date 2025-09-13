from gi.repository import Gtk, Gdk, GtkLayerShell
import widgets as Widget
from .notification_list import NotificationList
from .audio_sliders import AudioSliders

class ControlPanel(Widget.Window):
    def __init__(self):
        super().__init__(
            name = "Control-panel",
            namespace = "Astel-Control-Panel",
            layer = GtkLayerShell.Layer.TOP,
            anchors = [
                GtkLayerShell.Edge.TOP,
                GtkLayerShell.Edge.BOTTOM,
                GtkLayerShell.Edge.RIGHT,
                GtkLayerShell.Edge.LEFT
            ],
            keyboard_mode = GtkLayerShell.KeyboardMode.ON_DEMAND,
            child = Widget.Box(
                children = [
                    Widget.EventBox(
                        name = "outside-eventbox",
                        hexpand = True
                    ),
                    Widget.Box(
                        hexpand = False,
                        orientation = Gtk.Orientation.VERTICAL,
                        children = [
                            Widget.EventBox(
                                name = "outside-eventbox",
                                vexpand = True
                            ),
                            Widget.Box(
                                name = "main-box",
                                orientation = Gtk.Orientation.VERTICAL,
                                children = [
                                    Widget.Stack(
                                        name = "pages-stack",
                                        transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
                                        hexpand = False,
                                        vexpand = False,
                                        vhomogeneous = False,
                                        children = [
                                            Widget.Box(
                                                name = "main-page",
                                                orientation = Gtk.Orientation.VERTICAL,
                                                children = [
                                                    NotificationList(),
                                                    Widget.Separator(),
                                                    AudioSliders()
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        def on_outside_click(*_):
            self.hide()

        def on_window_key_press(x, event):
            if event.keyval == Gdk.KEY_Escape:
                self.hide()

        def on_visible(*_):
            if self.get_visible():
                self.show_all()

        self.connect("key-press-event", on_window_key_press)
        self.connect("notify::visible", on_visible)

        for i in Widget.get_children_by_name(self, "outside-eventbox"):
            i.connect("button-press-event", on_outside_click)
