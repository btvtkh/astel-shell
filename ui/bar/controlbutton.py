import widget as Widget

class ControlButton(Widget.Button):
    def __init__(self):
        super().__init__(
            name = "control-button",
            visible = True,
            child = Widget.Image(
                visible = True,
                icon_name = "sidebar-show-right-symbolic"
            )
        )
