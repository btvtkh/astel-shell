import widget as Widget

def ControlButton():
    return Widget.Button(
        name = "control-button",
        visible = True,
        child = Widget.Image(
            visible = True,
            icon_name = "sidebar-show-right-symbolic"
        )
    )
