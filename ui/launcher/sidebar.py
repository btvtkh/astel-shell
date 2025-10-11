from gi.repository import Gtk
import widget as Widget

def Sidebar():
    return Widget.Box(
        name = "sidebar",
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
