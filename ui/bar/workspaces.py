from gi.repository import AstalHyprland
import widget as Widgets

hyprland = AstalHyprland.get_default()

def WorkspaceButton(ws):
    ret = Widgets.Button(
        child = Widgets.Label(
            label = ws.get_name()
        )
    )

    def on_focused_ws(*_):
        if ws == hyprland.get_focused_workspace():
            ret.add_css_class("focused")
        else:
            ret.remove_css_class("focused")

    def on_clicked(*_):
        if ws != hyprland.get_focused_workspace():
            ws.focus()

    focused_workspace_handler = hyprland.connect("notify::focused-workspace", on_focused_ws)
    clicked_handler = ret.connect("clicked", on_clicked)

    def on_destroy(*_):
        hyprland.disconnect(focused_workspace_handler)
        ret.disconnect(clicked_handler)

    ret.connect("destroy", on_destroy)
    ret.set_css_classes([ws == hyprland.get_focused_workspace() and "focused"])

    return ret

def Workspaces():
    ret = Widgets.Box(name = "workspaces")

    def on_workspaces(*_):
        for child in ret.get_children():
            child.destroy()

        wss = hyprland.get_workspaces()
        wss.sort(key = lambda x: x.get_id())
        for ws in wss:
            if not (ws.get_id() >= -99 and ws.get_id() <= -2):
                ret.add(WorkspaceButton(ws))

    hyprland.connect("notify::workspaces", on_workspaces)
    on_workspaces()

    return ret
