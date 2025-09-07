import widgets as Widget

class LauncherButtonWidget(Widget.Button):
    def __init__(self, window):
        def on_setup(self):
            def on_clicked(*_):
                window.get_application().toggle_window("Launcher")

            self.connect("clicked", on_clicked)

        super().__init__(
            name = "launcher-button",
            visible = True,
            setup = on_setup,
            child = Widget.Image(
                visible = True,
                icon_name = "system-search-symbolic"
            )
        )
