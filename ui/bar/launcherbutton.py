import widget as Widget

def LauncherButton():
    return Widget.Button(
        name = "launcher-button",
        visible = True,
        child = Widget.Image(
            visible = True,
            icon_name = "system-search-symbolic"
        )
    )
