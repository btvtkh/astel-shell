import widget as Widget

class LauncherButton(Widget.Button):
    def __init__(self):
        super().__init__(
            name = "launcher-button",
            visible = True,
            child = Widget.Image(
                visible = True,
                icon_name = "system-search-symbolic"
            )
        )
