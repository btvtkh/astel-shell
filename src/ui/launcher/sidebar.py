from gi.repository import Gtk
import widgets as Widgets

class SidebarWidget(Widgets.Box):
    def __init__(self, window):
        super().__init__(
            visible = True,
            orientation = Gtk.Orientation.VERTICAL,
            children = [
                Gtk.Button(
                    visible = True,
                    child = Gtk.Image(
                        visible = True,
                        icon_name = "system-shutdown-symbolic"
                    )
                ),
                Gtk.Button(
                    visible = True,
                    child = Gtk.Image(
                        visible = True,
                        icon_name = "image-x-generic-symbolic"
                    )
                ),
                Gtk.Button(
                    visible = True,
                    child = Gtk.Image(
                        visible = True,
                        icon_name = "user-home-symbolic"
                    )
                )
            ]
        )
