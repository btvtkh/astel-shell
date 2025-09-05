from gi.repository import Gtk

class LauncherButtonWidget(Gtk.Button):
    def __init__(self, window):
        super().__init__(
            visible = True,
            child = Gtk.Image(
                visible = True,
                icon_name = "system-search-symbolic"
            )
        )

        self.get_style_context().add_class("launcher-button")

        def on_clicked(*_):
            window.get_application().toggle_window("Launcher")

        self.connect("clicked", on_clicked)
