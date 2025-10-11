from gi.repository import Gtk, AstalBluetooth
import widget as Widget

bluetooth = AstalBluetooth.get_default()
adapter = bluetooth.get_adapter()

class BluetoothQSB(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes = ["qsb"],
            hexpand = True,
            children = [
                Widget.Button(
                    name = "bluetooth-qsb-toggle-button",
                    css_classes = ["toggle-button"],
                    hexpand = True,
                    child = Widget.Box(
                        children = [
                            Widget.Image(
                                name = "bluetooth-qsb-status-icon",
                                css_classes = ["status-icon"],
                                icon_name = "bluetooth-active-symbolic"
                            ),
                            Widget.Box(
                                orientation = Gtk.Orientation.VERTICAL,
                                hexpand = True,
                                children = [
                                    Widget.Label(
                                        css_classes = ["title-label"],
                                        halign = Gtk.Align.START,
                                        xalign = 0,
                                        label = "Bluetooth"
                                    ),
                                    Widget.Label(
                                        name = "bluetooth-qsb-status-label",
                                        css_classes = ["status-label"],
                                        halign = Gtk.Align.START,
                                        xalign = 0,
                                        label = "Disabled"
                                    )
                                ]
                            ),
                            Widget.Separator(
                                name = "bluetooth-qsb-separator"
                            )
                        ]
                    )
                ),
                Widget.Button(
                    name = "bluetooth-qsb-reveal-button",
                    css_classes = ["reveal-button"],
                    child = Widget.Image(
                        icon_name = "pan-end-symbolic"
                    )
                )
            ]
        )

        toggle_button = Widget.get_child_by_name(self, "bluetooth-qsb-toggle-button")
        reveal_button = Widget.get_child_by_name(self, "bluetooth-qsb-reveal-button")
        status_label = Widget.get_child_by_name(self, "bluetooth-qsb-status-label")
        separator = Widget.get_child_by_name(self, "bluetooth-qsb-separator")

        def on_adapter_powered(*_):
            if adapter and adapter.get_powered():
                status_label.set_label("Enabled")
                self.add_css_class("toggled")
            else:
                status_label.set_label("Disabled")
                self.remove_css_class("toggled")

        def on_toggle_button_clicked(*_):
            if adapter: adapter.set_powered(not adapter.get_powered())

        def on_button_enter(*_):
            separator.add_css_class("hovered")

        def on_button_leave(*_):
            separator.remove_css_class("hovered")

        for i in [toggle_button, reveal_button]:
            i.connect("leave-notify-event", on_button_leave)
            i.connect("enter-notify-event", on_button_enter)

        toggle_button.connect("clicked", on_toggle_button_clicked)
        if adapter: adapter.connect("notify::powered", on_adapter_powered)

        on_adapter_powered()
