import widgets as Widget

class LauncherButtonWidget(Widget.Button):
    def __init__(self, window):
        super().__init__(
            name = "launcher-button",
            visible = True,
            child = Widget.Image(
                visible = True,
                icon_name = "system-search-symbolic"
            )
        )

        def on_clicked(*_):
            window.get_application().toggle_window("Launcher")

        self.connect("clicked", on_clicked)
