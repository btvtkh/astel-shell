from gi.repository import Gtk, AstalNetwork
import widget as Widget

network = AstalNetwork.get_default()
wifi = network.get_wifi()

class WifiQSB(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes = ["qsb"],
            hexpand = True,
            children = [
                Widget.Button(
                    name = "wifi-qsb-toggle-button",
                    css_classes = ["toggle-button"],
                    hexpand = True,
                    child = Widget.Box(
                        children = [
                            Widget.Image(
                                name = "wifi-qsb-status-icon",
                                css_classes = ["status-icon"],
                                icon_name = "network-wireless-symbolic"
                            ),
                            Widget.Box(
                                orientation = Gtk.Orientation.VERTICAL,
                                hexpand = True,
                                children = [
                                    Widget.Label(
                                        css_classes = ["title-label"],
                                        halign = Gtk.Align.START,
                                        xalign = 0,
                                        label = "Wifi"
                                    ),
                                    Widget.Label(
                                        name = "wifi-qsb-status-label",
                                        css_classes = ["status-label"],
                                        halign = Gtk.Align.START,
                                        xalign = 0,
                                        label = "Disabled"
                                    )
                                ]
                            ),
                            Widget.Separator(
                                name = "wifi-qsb-separator"
                            )
                        ]
                    )
                ),
                Widget.Button(
                    name = "wifi-qsb-reveal-button",
                    css_classes = ["reveal-button"],
                    child = Widget.Image(
                        icon_name = "pan-end-symbolic"
                    )
                )
            ]
        )

        toggle_button = Widget.get_child_by_name(self, "wifi-qsb-toggle-button")
        reveal_button = Widget.get_child_by_name(self, "wifi-qsb-reveal-button")
        status_label = Widget.get_child_by_name(self, "wifi-qsb-status-label")
        separator = Widget.get_child_by_name(self, "wifi-qsb-separator")

        def on_wifi_enabled(*_):
            if wifi and wifi.get_enabled():
                status_label.set_label("Enabled")
                self.add_css_class("toggled")
            else:
                status_label.set_label("Disabled")
                self.remove_css_class("toggled")

        def on_toggle_button_clicked(*_):
            if wifi: wifi.set_enabled(not wifi.get_enabled())

        def on_button_enter(*_):
            separator.add_css_class("hovered")

        def on_button_leave(*_):
            separator.remove_css_class("hovered")

        for i in [toggle_button, reveal_button]:
            i.connect("leave-notify-event", on_button_leave)
            i.connect("enter-notify-event", on_button_enter)

        toggle_button.connect("clicked", on_toggle_button_clicked)
        if wifi: wifi.connect("notify::enabled", on_wifi_enabled)

