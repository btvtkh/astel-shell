from gi.repository import Gdk, Gtk, GtkLayerShell, AstalHyprland
import widgets as Widget

class Powermenu(Widget.Window):
    def __init__(self):
        def on_setup(self):
            hyprland = AstalHyprland.get_default()
            power_button = Widget.get_children_by_name(self, "power-button")[0]
            reboot_button = Widget.get_children_by_name(self, "reboot-button")[0]
            exit_button = Widget.get_children_by_name(self, "exit-button")[0]

            def on_outside_click(*_):
                self.hide()

            def on_power_button_clicked(*_):
                self.hide()
                hyprland.dispatch("exec", "poweroff")

            def on_power_button_key_press(x, event):
                 if event.keyval == Gdk.KEY_Return:
                    on_power_button_clicked()

            def on_reboot_button_clicked(*_):
                self.hide()
                hyprland.dispatch("exec", "reboot")

            def on_reboot_button_key_press(x, event):
                 if event.keyval == Gdk.KEY_Return:
                    on_reboot_button_clicked()

            def on_exit_button_clicked(*_):
                self.hide()
                hyprland.dispatch("exit", "")

            def on_exit_button_key_press(x, event):
                 if event.keyval == Gdk.KEY_Return:
                    on_exit_button_clicked()

            def on_visible(*_):
                if self.get_visible():
                    power_button.grab_focus()

            def on_key_press(x, event):
                if event.keyval == Gdk.KEY_Escape:
                    self.hide()

            power_button.connect("clicked", on_power_button_clicked)
            power_button.connect("key-press-event", on_power_button_key_press)
            reboot_button.connect("clicked", on_reboot_button_clicked)
            reboot_button.connect("key-press-event", on_reboot_button_key_press)
            exit_button.connect("clicked", on_exit_button_clicked)
            exit_button.connect("key-press-event", on_exit_button_key_press)
            self.connect("key-press-event", on_key_press)
            self.connect("notify::visible", on_visible)

            for i in Widget.get_children_by_name(self, "outside-eventbox"):
                i.connect("button-press-event", on_outside_click)

        super().__init__(
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
            setup = on_setup,
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
                                name = "main-box",
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

