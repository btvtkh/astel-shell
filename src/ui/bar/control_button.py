import widgets as Widget

class ControlButton(Widget.Button):
    def __init__(self, window):
        super().__init__(
            name = "control-button",
            visible = True,
            child = Widget.Image(
                visible = True,
                icon_name = "preferences-system-symbolic"
            )
        )

        def on_clicked(*_):
            window.get_application().toggle_window("Control-panel")

        self.connect("clicked", on_clicked)
