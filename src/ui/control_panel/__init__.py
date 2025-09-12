from gi.repository import Gtk, Gdk, GtkLayerShell
import widgets as Widget
from .notification_list import NotificationList

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
                                        homogeneous = False,
                                        children = [
                                            Widget.Box(
                                                name = "main-page",
                                                children = [
                                                    NotificationList()
                                                ]
                                            ),
                                            Widget.Box(
                                                name = "wifi-page",
                                                children = [
                                                    Widget.Label(
                                                        hexpand = True,
                                                        vexpand = True,
                                                        halign = Gtk.Align.CENTER,
                                                        valign = Gtk.Align.CENTER,
                                                        label = "wifi page"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    Widget.Box(
                                        children = [
                                            Widget.Button(
                                                name = "main-page-button",
                                                hexpand = True,
                                                child = Widget.Label(
                                                    label = "main"
                                                )
                                            ),
                                            Widget.Button(
                                                name = "wifi-page-button",
                                                hexpand = True,
                                                child = Widget.Label(
                                                    label = "wifi"
                                                )
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

        pages_stack = Widget.get_children_by_name(self, "pages-stack")[0]
        main_page_button = Widget.get_children_by_name(self, "main-page-button")[0]
        wifi_page_button = Widget.get_children_by_name(self, "wifi-page-button")[0]

        main_page_button.connect("clicked", lambda x: pages_stack.set_visible_child_name("main-page"))
        wifi_page_button.connect("clicked", lambda x: pages_stack.set_visible_child_name("wifi-page"))

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
