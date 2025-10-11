from datetime import datetime
from gi.repository import Gtk, Pango
import widget as Widget

URGENCY_MAP = {
    "0": "low",
    "1": "normal",
    "2": "critical"
}

def ActionButton(n, action):
    ret = Widget.Button(
        css_classes = ["action-button"],
        hexpand = True,
        child = Widget.Label(
            hexpand = True,
            halign = Gtk.Align.CENTER,
            ellipsize = Pango.EllipsizeMode.END,
            max_width_chars = 10,
            label = action.label
        )
    )

    def on_clicked(*_):
        n.invoke(action.id)

    clicked_handler = ret.connect("clicked", on_clicked)

    def on_destroy(*_):
        ret.disconnect(clicked_handler)

    ret.connect("destroy", on_destroy)

    return ret

def Notification(n):
    ret = Widget.Box(
        css_classes = [
            "notification-box",
            URGENCY_MAP[str(n.get_urgency())]
        ],
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Box(
                css_classes = ["header-box"],
                children = [
                    Widget.Label(
                        css_classes = ["app-name-label"],
                        halign = Gtk.Align.START,
                        ellipsize = Pango.EllipsizeMode.END,
                        label = n.get_app_name() or "Unknown"
                    ),
                    Widget.Label(
                        css_classes = ["time-label"],
                        hexpand = True,
                        halign = Gtk.Align.END,
                        label = datetime.fromtimestamp(n.get_time()).strftime("%H:%M")
                    ),
                    Widget.Button(
                        name = "close-button",
                        css_classes = ["close-button"],
                        child = Widget.Image(
                            icon_size = Gtk.IconSize.BUTTON,
                            icon_name = "window-close-symbolic"
                        )
                    )
                ]
            ),
            Widget.Separator(),
            Widget.Box(
                css_classes = ["body-box"],
                orientation = Gtk.Orientation.VERTICAL,
                children = [
                    Widget.Label(
                        css_classes = ["summary-label"],
                        halign = Gtk.Align.START,
                        xalign = 0,
                        ellipsize = Pango.EllipsizeMode.END,
                        max_width_chars = 25,
                        label = n.get_summary()
                    ),
                    Widget.Label(
                        css_classes = ["body-label"],
                        use_markup = True,
                        halign = Gtk.Align.START,
                        xalign = 0,
                        ellipsize = Pango.EllipsizeMode.END,
                        max_width_chars = 30,
                        label = n.get_body()
                    )
                ]
            ),
            n.get_actions() and Widget.Box(
                css_classes = ["actions-box"],
                homogeneous = True,
                children = [
                    ActionButton(n, a) for a in n.get_actions()
                ]
            )
        ]
    )

    close_button = Widget.get_child_by_name(ret, "close-button")

    def on_close_clicked(*_):
        n.dismiss()

    close_clicked_handler = close_button.connect("clicked", on_close_clicked)

    def on_destroy(*_):
        close_button.disconnect(close_clicked_handler)

    ret.connect("destroy", on_destroy)

    return ret
