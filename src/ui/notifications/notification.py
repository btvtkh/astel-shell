from datetime import datetime
from gi.repository import Gtk, Pango
import widgets as Widget

URGENCY_MAP = {
    "0": "low",
    "1": "normal",
    "2": "critical"
}

class ActionButton(Widget.Button):
    def __init__(self, n, action):
        def on_setup(self):
            def on_clicked(*_):
                n.invoke(action.id)

            on_clicked_id = self.connect("clicked", on_clicked)

            def on_destroy(*_):
                self.disconnect(on_clicked_id)

            self.connect("destroy", on_destroy)

        super().__init__(
            name = "action-button",
            hexpand = True,
            setup = on_setup,
            child = Widget.Label(
                hexpand = True,
                halign = Gtk.Align.CENTER,
                ellipsize = Pango.EllipsizeMode.END,
                max_width_chars = 10,
                label = action.label
            )
        )

class NotificationWidget(Widget.Box):
    def __init__(self, n):
        def on_setup(w):
            close_button = Widget.get_children_by_name(w, "close-button")[0]

            def on_close_clicked(*_):
                n.dismiss()

            on_close_clicked_id = close_button.connect("clicked", on_close_clicked)

            def on_destroy(*_):
                close_button.disconnect(on_close_clicked_id)

            self.connect("destroy", on_destroy)

        super().__init__(
            name = "notification-box",
            css_classes = [
                URGENCY_MAP[str(n.get_urgency())]
            ],
            setup = on_setup,
            orientation = Gtk.Orientation.VERTICAL,
            children = [
                Widget.Box(
                    name = "header-box",
                    children = [
                        Widget.Label(
                            name = "app-name-label",
                            halign = Gtk.Align.START,
                            ellipsize = Pango.EllipsizeMode.END,
                            label = n.get_app_name() or "Unknown"
                        ),
                        Widget.Label(
                            name = "time-label",
                            hexpand = True,
                            halign = Gtk.Align.END,
                            label = datetime.fromtimestamp(n.get_time()).strftime("%H:%M")
                        ),
                        Widget.Button(
                            name = "close-button",
                            child = Widget.Image(
                                icon_size = Gtk.IconSize.BUTTON,
                                icon_name = "window-close-symbolic"
                            )
                        )
                    ]
                ),
                Widget.Separator(),
                Widget.Box(
                    name = "body-box",
                    orientation = Gtk.Orientation.VERTICAL,
                    children = [
                        Widget.Label(
                            name = "summary-label",
                            halign = Gtk.Align.START,
                            xalign = 0,
                            ellipsize = Pango.EllipsizeMode.END,
                            max_width_chars = 25,
                            label = n.get_summary()
                        ),
                        Widget.Label(
                            name = "body-label",
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
                    name = "actions-box",
                    children = [
                        ActionButton(n, a) for a in n.get_actions()
                    ]
                )
            ]
        )
