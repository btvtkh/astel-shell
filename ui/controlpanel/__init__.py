from gi.repository import Gtk, Gdk, GtkLayerShell
import widget as Widget
from .mainpage import MainPage
from .wifipage import WifiPage
from .bluetoothpage import BluetoothPage

def ControlPanel():
    ret = Widget.LayerWindow(
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
                            css_classes = ["main-box"],
                            orientation = Gtk.Orientation.VERTICAL,
                            children = [
                                Widget.Stack(
                                    name = "pages-stack",
                                    transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
                                    hexpand = False,
                                    vexpand = False,
                                    vhomogeneous = False,
                                    children = [
                                        MainPage(),
                                        WifiPage(),
                                        BluetoothPage()
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    )

    pages_stack = Widget.get_child_by_name(ret, "pages-stack")
    wifi_qsb_reveal_button = Widget.get_child_by_name(ret, "wifi-qsb-reveal-button")
    wifi_page_close_button = Widget.get_child_by_name(ret, "wifi-page-close-button")
    wifi_page_ap_stack = Widget.get_child_by_name(ret, "access-points-stack")
    bluetooth_qsb_reveal_button = Widget.get_child_by_name(ret, "bluetooth-qsb-reveal-button")
    bluetooth_page_close_button = Widget.get_child_by_name(ret, "bluetooth-page-close-button")

    def on_wifi_qsb_reveal_button_clicked(*_):
        pages_stack.reveal_child("wifi-page")
        wifi_page_ap_stack.destroy_named("access-point-menu")
        wifi_page_ap_stack.reveal_child("access-points-list-scrolled-window")

    def on_bluetooth_qsb_reveal_button_clicked(*_):
        pages_stack.reveal_child("bluetooth-page")

    def on_page_close_button_clicked(*_):
        pages_stack.reveal_child("main-page")

    def on_outside_click(*_):
        ret.hide()

    def on_window_key_press(x, event):
        if event.keyval == Gdk.KEY_Escape:
            ret.hide()

    def on_visible(*_):
        pages_stack.reveal_child("main-page")

    wifi_qsb_reveal_button.connect("clicked", on_wifi_qsb_reveal_button_clicked)
    wifi_page_close_button.connect("clicked", on_page_close_button_clicked)
    bluetooth_qsb_reveal_button.connect("clicked", on_bluetooth_qsb_reveal_button_clicked)
    bluetooth_page_close_button.connect("clicked", on_page_close_button_clicked)
    ret.connect("key-press-event", on_window_key_press)
    ret.connect("notify::visible", on_visible)

    for i in Widget.get_children_by_name(ret, "outside-eventbox"):
        i.connect("button-press-event", on_outside_click)

    return ret
