from gi.repository import Gtk, Gdk, GtkLayerShell, AstalHyprland
import widget as Widget

hyprland = AstalHyprland.get_default()

def Powermenu():
    ret = Widget.LayerWindow(
        name = "Powermenu",
        namespace = "Astel-Powermenu",
        layer = GtkLayerShell.Layer.TOP,
        anchors = [
            GtkLayerShell.Edge.TOP,
            GtkLayerShell.Edge.BOTTOM,
            GtkLayerShell.Edge.LEFT,
            GtkLayerShell.Edge.RIGHT
        ],
        keyboard_mode = GtkLayerShell.KeyboardMode.ON_DEMAND,
        child = Widget.Box(
            children = [
                Widget.EventBox(
                    name = "outside-eventbox",
                    hexpand = True
                ),
                Widget.Box(
                    orientation = Gtk.Orientation.VERTICAL,
                    hexpand = False,
                    children = [
                        Widget.EventBox(
                            name = "outside-eventbox",
                            vexpand = True
                        ),
                        Widget.Box(
                            css_classes = ["main-box"],
                            children = [
                                Widget.Button(
                                    name = "power-button",
                                    child = Widget.Image(
                                        icon_name = "system-shutdown-symbolic",
                                        pixel_size = 32
                                    )
                                ),
                                Widget.Button(
                                    name = "reboot-button",
                                    child = Widget.Image(
                                        icon_name = "system-reboot-symbolic",
                                        pixel_size = 32
                                    )
                                ),
                                Widget.Button(
                                    name = "exit-button",
                                    child = Widget.Image(
                                        icon_name = "system-log-out-symbolic",
                                        pixel_size = 32
                                    )
                                )
                            ]
                        ),
                        Widget.EventBox(
                            name = "outside-eventbox",
                            vexpand = True
                        )
                    ]
                ),
                Widget.EventBox(
                    name = "outside-eventbox",
                    hexpand = True
                )
            ]
        )
    )

    power_button = Widget.get_child_by_name(ret, "power-button")
    reboot_button = Widget.get_child_by_name(ret, "reboot-button")
    exit_button = Widget.get_child_by_name(ret, "exit-button")

    def on_outside_click(*_):
        ret.hide()

    def on_power_button_clicked(*_):
        ret.hide()
        hyprland.dispatch("exec", "poweroff")

    def on_power_button_key_press(x, event):
         if event.keyval == Gdk.KEY_Return:
            on_power_button_clicked()

    def on_reboot_button_clicked(*_):
        ret.hide()
        hyprland.dispatch("exec", "reboot")

    def on_reboot_button_key_press(x, event):
         if event.keyval == Gdk.KEY_Return:
            on_reboot_button_clicked()

    def on_exit_button_clicked(*_):
        ret.hide()
        hyprland.dispatch("exit", "")

    def on_exit_button_key_press(x, event):
         if event.keyval == Gdk.KEY_Return:
            on_exit_button_clicked()

    def on_visible(*_):
        if ret.get_visible():
            power_button.grab_focus()

    def on_key_press(x, event):
        if event.keyval == Gdk.KEY_Escape:
            ret.hide()

    power_button.connect("clicked", on_power_button_clicked)
    power_button.connect("key-press-event", on_power_button_key_press)
    reboot_button.connect("clicked", on_reboot_button_clicked)
    reboot_button.connect("key-press-event", on_reboot_button_key_press)
    exit_button.connect("clicked", on_exit_button_clicked)
    exit_button.connect("key-press-event", on_exit_button_key_press)
    ret.connect("key-press-event", on_key_press)
    ret.connect("notify::visible", on_visible)

    for i in Widget.get_children_by_name(ret, "outside-eventbox"):
        i.connect("button-press-event", on_outside_click)

    return ret
