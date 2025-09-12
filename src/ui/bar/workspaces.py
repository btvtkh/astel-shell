from gi.repository import AstalHyprland
import widgets as Widgets

class WorkspaceButton(Widgets.Button):
    def __init__(self, ws):
        super().__init__(
            name = "workspace-button",
            child = Widgets.Label(
                label = ws.get_name()
            )
        )

        hyprland = AstalHyprland.get_default()

        def on_focused_ws(*_):
            if ws == hyprland.get_focused_workspace():
                self.add_css_class("focused")
            else:
                self.remove_css_class("focused")

        def on_clicked(*_):
            if ws != hyprland.get_focused_workspace():
                ws.focus()

        on_focused_ws_id = hyprland.connect("notify::focused-workspace", on_focused_ws)
        on_clicked_id = self.connect("clicked", on_clicked)

        def on_destroy(*_):
            hyprland.disconnect(on_focused_ws_id)
            self.disconnect(on_clicked_id)

        self.connect("destroy", on_destroy)
        self.set_css_classes([ws == hyprland.get_focused_workspace() and "focused"])

class Workspaces(Widgets.Box):
    def __init__(self):
        super().__init__(
            name = "workspaces-box"
        )

        hyprland = AstalHyprland.get_default()

        def on_workspaces(*_):
            for child in self.get_children():
                child.destroy()

            wss = hyprland.get_workspaces()
            wss.sort(key = lambda x: x.get_id())
            for ws in wss:
                if not (ws.get_id() >= -99 and ws.get_id() <= -2):
                    self.add(WorkspaceButton(ws))

        hyprland.connect("notify::workspaces", on_workspaces)
        on_workspaces()
