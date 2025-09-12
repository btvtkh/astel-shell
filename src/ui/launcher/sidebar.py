from gi.repository import Gtk
import widgets as Widget

class Sidebar(Widget.Box):
    def __init__(self, window):
        super().__init__(
            name = "sidebar-box",
            visible = True,
            orientation = Gtk.Orientation.VERTICAL,
            vexpand = False,
            children = [
                Widget.Button(
                    name = "power-button",
                    visible = True,
                    child = Widget.Image(
                        visible = True,
                        icon_name = "system-shutdown-symbolic"
                    )
                ),
                Widget.Box(
                    orientation = Gtk.Orientation.VERTICAL,
                    valign = Gtk.Align.END,
                    vexpand = True,
                    children = [
                        Widget.Button(
                            visible = True,
                            child = Widget.Image(
                                visible = True,
                                icon_name = "image-x-generic-symbolic"
                            )
                        ),
                        Widget.Separator(),
                        Widget.Button(
                            visible = True,
                            child = Widget.Image(
                                visible = True,
                                icon_name = "user-home-symbolic"
                            )
                        )
                    ]
                )
            ]
        )

        power_button = Widget.get_children_by_name(self, "power-button")[0]

        def on_power_button_clicked(*_):
            window.get_application().toggle_window("Powermenu")

        power_button.connect("clicked", on_power_button_clicked)
